import winreg
import time, re, os
from pathlib import Path
import psutil

# -----------------------------
# find steam path from registry
# -----------------------------
def safe_get_path_from_regedit(key,sub_key,name):
    try:
        key = winreg.OpenKeyEx(key, sub_key, reserved=0, access=winreg.KEY_QUERY_VALUE)
        value, val_type = winreg.QueryValueEx(key,name)
        # print(f"successful open: {key} {sub_key}")
        return value, val_type
    
    except FileNotFoundError:
        print(f"Cannot find value: subpath: {sub_key}, name: {name}")
    except PermissionError:
        print(f"Insufficient permissions, please run as administrator: {sub_key}")
    except WindowsError as e:
        print(f"Error: {sub_key} \\ {name}: {e}")
    finally:
        winreg.CloseKey(key)
    return None


# get library root path
def get_library_roots(steam_path):
    vdf = steam_path / "steamapps" / "libraryfolders.vdf"
    libs = [steam_path]

    if vdf.exists():
        text = vdf.read_text(encoding="utf-8", errors="ignore")

        # new firmat： "path" "D:\\SteamLibrary"
        for m in re.finditer(r'"path"\s*"([^"]+)"', text):
            libs.append(Path(m.group(1)))

        # old format backup： "1" "D:\\SteamLibrary"
        if len(libs) == 1:
            for m in re.finditer(r'"\d+"\s*"([^"]+)"', text):
                p = m.group(1)
                if ":\\" in p or p.startswith("\\\\"):
                    libs.append(Path(p))

    # return each database from steamapps
    steamapps_dirs = []
    for lib in dict.fromkeys([p.resolve() for p in libs]):  
        sp = lib / "steamapps"
        if sp.exists():
            steamapps_dirs.append(sp)

    return steamapps_dirs

# -----------------------------
# minimal ACF parse for flat keys
# -----------------------------
_acf_kv = re.compile(r'"([^"]+)"\s+"([^"]*)"')

def parse_acf_flat(path: Path) -> dict:
    d = {}
    try:
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            m = _acf_kv.search(line)
            if m:
                d[m.group(1)] = m.group(2)
    except Exception:
        pass
    return d


# -----------------------------
# find currently downloading app by scanning manifests (works on D/E)
# -----------------------------
def find_downloading_app(steamapps_dirs):
    """
    Return (appid, name, status)
    status: Downloading / Idle
    """
    for steamapps in steamapps_dirs:
        for f in steamapps.glob("appmanifest_*.acf"):
            kv = parse_acf_flat(f)
            appid = kv.get("appid")
            name = kv.get("name")
            flags = kv.get("StateFlags")

            if not appid or not name or not flags:
                continue

            # ignore redistributables noise
            if appid == "228980":
                continue

            try:
                if int(flags) & DOWNLOADING_BIT:
                    return appid, name, "Downloading"
            except ValueError:
                continue

    return None, None, "Idle"

# -----------------------------
# optional: parse logs to refine status (Paused/Downloading)
# logs exist only in C:\Steam\logs, not in libraries
# -----------------------------
def current_appid_and_status(logs):
    for name in ["download_log.txt", "content_log.txt"]:
        p = logs / name
        if not p.exists():
            continue
        for line in reversed(p.read_text(errors="ignore").splitlines()[-300:]):
            if "appid" in line.lower():
                m = re.search(r"appid[ :=]+(\d+)", line, re.I)
                if m:
                    status = "Paused" if "pause" in line.lower() else "Downloading"
                    return m.group(1), status
    return None, "Idle"


##################
# ---- main ---- #
##################

if __name__ == "__main__":
    ROOTKEY = winreg.HKEY_CURRENT_USER
    SUBKEY = r"Software\Valve\Steam"
    NAME = "SteamPath"
    STEAM_ROOT_PATH = Path(safe_get_path_from_regedit(ROOTKEY, SUBKEY, NAME)[0])

    STEAM_LOGS = STEAM_ROOT_PATH / "logs"
    steamapps_dirs = get_library_roots(STEAM_ROOT_PATH)

    WAIT_TIME = 60
    RANGE_TIME = 5
    DOWNLOADING_BIT = 1024
    prev_rx = psutil.net_io_counters().bytes_recv


    print(f"[time] name | status | speed MB/s")
    for _ in range(RANGE_TIME):
        time.sleep(WAIT_TIME)
        ts = time.strftime("%H:%M:%S")

        # 1) decide if there is a downloading game (from manifests across all disks)
        appid, game_name, status = find_downloading_app(steamapps_dirs)

        # 2) If no downloading game: output only time + None, reset baseline
        if not appid:
            prev_rx = None
            print(f"[{ts}] None")
            continue

        # 3) Optional: use logs to refine status (paused vs downloading)
        log_appid, log_status = current_appid_and_status(STEAM_LOGS)
        if log_appid == appid and log_status in ("Paused", "Downloading"):
            status = log_status

        # 4) speed only when downloading detected
        now_rx = psutil.net_io_counters().bytes_recv
        if prev_rx is None:
            prev_rx = now_rx
            speed_mb = 0.0
        else:
            speed_mb = (now_rx - prev_rx) / WAIT_TIME / 1024 / 1024
            prev_rx = now_rx

        # if status says downloading but speed ~0, treat as paused
        if status == "Downloading" and speed_mb <= 0.01:
            status = "Paused"

        print(f"[{ts}] {game_name} | {status} | {speed_mb:.2f} MB/s")