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