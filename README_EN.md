# Steam Download Monitoring Script (Windows)

## Purpose  
To monitor the Steam game download process on Windows, determine if any game download tasks are present, identify the names of games currently being downloaded, and calculate the download speed.

## Core Idea  
The script retrieves the Steam client installation path via the Windows registry; parses the steamapps/libraryfolders.vdf file to support Steam game libraries located on different drives such as D, E, etc.; scans the steamapps/appmanifest_<appid>.acf files in each library, and determines if any game is being downloaded based on the status field within these files; when a game download is detected, the system network statistics (`psutil`) are used to calculate the download speed.

## Data Sources  
- Windows registry  
- steamapps/libraryfolders.vdf  
- steamapps/appmanifest_<appid>.acf  
- System network receive counter (psutil)

## Execution Method  
Run in PowerShell:  
```powershell
.\run_script.ps1
```

## Output Example  
No game downloading:  

[20:00:14] None  

Game downloading:  

[20:05:10] Palworld | Downloading | 18.42 MB/s

## Runtime Environment  
- Windows operating system  
- Python 3.8 or higher  
- Steam client installed  
- At least one Steam game library  

## Notes  
The script ignores the Steam Common Redistributables (appid 228980) by default. Download speed is calculated only when a game download is detected. The design goals are stability, interpretability, and independence from the Steam graphical interface.