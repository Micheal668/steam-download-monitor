# Steam 下载监控脚本（Windows）

## 目的
在 Windows 系统上监控 Steam 游戏下载过程，判断是否存在游戏下载任务，识别正在下载的游戏名称，并计算下载速度。

## 核心思路
脚本通过 Windows 注册表获取 Steam 客户端安装路径；解析 steamapps/libraryfolders.vdf 文件以支持位于 D、E 等不同硬盘的 Steam 游戏库；扫描各库中的 steamapps/appmanifest_<appid>.acf 文件，根据其中的状态字段判断是否存在正在下载的游戏；当检测到游戏下载时，使用系统网络统计（`psutil`）计算下载速度。

## 数据来源
- Windows 注册表  
- steamapps/libraryfolders.vdf  
- steamapps/appmanifest_<appid>.acf  
- 系统网络接收计数器（psutil）

## 运行方式
在 PowerShell 中执行：
```powershell
.\run_script.ps1
输出示例
无游戏下载：

[20:00:14] None
有游戏下载：

[20:05:10] Palworld | Downloading | 18.42 MB/s
运行环境
Windows 操作系统

Python 3.8 及以上

已安装 Steam 客户端

至少一个 Steam 游戏库

说明
脚本默认忽略 Steam 公共运行库（appid 228980），仅在检测到游戏下载时才计算下载速度，设计目标为稳定、可解释，并且不依赖 Steam 图形界面。


**# Скрипт мониторинга загрузки Steam (Windows)**

**## Назначение**  
Мониторинг процесса загрузки игр в Steam на ОС Windows: определение наличия активных задач загрузки, идентификация названия скачиваемой игры и расчёт скорости загрузки.

**## Основная логика**  
Скрипт получает путь установки клиента Steam через реестр Windows; анализирует файл `steamapps/libraryfolders.vdf` для поддержки библиотек игр Steam на разных дисках (D, E и т.д.); сканирует файлы `steamapps/appmanifest_<appid>.acf` в каждой библиотеке и определяет наличие активно скачиваемой игры по полю состояния; при обнаружении загрузки использует системную сетевую статистику (`psutil`) для расчёта скорости скачивания.

**## Источники данных**  
- Реестр Windows  
- `steamapps/libraryfolders.vdf`  
- `steamapps/appmanifest_<appid>.acf`  
- Счётчик полученных сетевых данных системы (`psutil`)

**## Способ запуска**  
Выполнить в PowerShell:  
```powershell
.\run_script.ps1
```

**## Пример вывода**  
*Нет активной загрузки:*  
`[20:00:14] None`  

*Идёт загрузка игры:*  
`[20:05:10] Palworld | Downloading | 18.42 MB/s`

**## Требования**  
- ОС Windows  
- Python 3.8 или выше  
- Установленный клиент Steam  
- Хотя бы одна библиотека игр Steam  

**## Примечания**  
Скрипт по умолчанию игнорирует загрузку общих компонентов Steam (appid 228980). Расчёт скорости выполняется только при обнаружении загрузки игры. Цели разработки: стабильность, понятность логики, независимость от графического интерфейса Steam.

"# Steam Download Monitoring Script (Windows)

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