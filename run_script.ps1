# run_script.ps1 (Windows PowerShell 5.1 compatible)
$ErrorActionPreference = "Stop"

$VenvDir = ".venv"
$EntryScript = "script.py"
$Requirements = "requirements.txt"

function CmdExists($n){ return [bool](Get-Command $n -ErrorAction SilentlyContinue) }

if (-not (CmdExists "python") -and -not (CmdExists "py")) {
    throw "Python not found. Install Python 3.8+ and add it to PATH."
}

if (CmdExists "python") { $Py = "python" } else { $Py = "py" }

try { & $Py -m pip --version | Out-Null }
catch { & $Py -m ensurepip --upgrade | Out-Null; & $Py -m pip install --upgrade pip | Out-Null }

if (-not (Test-Path $VenvDir)) { & $Py -m venv $VenvDir | Out-Null }
$Activate = Join-Path $VenvDir "Scripts\Activate.ps1"
if (-not (Test-Path $Activate)) { throw "Activate.ps1 not found in virtual environment." }
. $Activate

python -m pip install --upgrade pip | Out-Null
if (Test-Path $Requirements) { python -m pip install -r $Requirements } else { python -m pip install psutil }

if (-not (Test-Path $EntryScript)) { throw "Entry script not found: $EntryScript" }
python $EntryScript