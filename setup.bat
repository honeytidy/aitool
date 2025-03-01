@echo off
chcp 65001

:: 检查是否具有管理员权限
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo 当前脚本没有管理员权限，正在尝试以管理员权限重新启动...
    powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

set SCRIPT_PATH="%~dp0main.exe"

reg add "HKEY_CLASSES_ROOT\*\shell\MyPythonAction" /ve /d "AI工具箱" /f
reg add "HKEY_CLASSES_ROOT\*\shell\MyPythonAction" /v "Icon" /d "%~dp0_internal\aitool.ico" /f
reg add "HKEY_CLASSES_ROOT\*\shell\MyPythonAction\command" /ve /d "\"%SCRIPT_PATH%\" \"%%1\"" /f


:: 为所有文件夹添加右键菜单
reg add "HKEY_CLASSES_ROOT\Directory\shell\MyPythonAction" /ve /d "AI工具箱" /f
reg add "HKEY_CLASSES_ROOT\Directory\shell\MyPythonAction" /v "Icon" /d "%~dp0_internal\aitool.ico" /f
reg add "HKEY_CLASSES_ROOT\Directory\shell\MyPythonAction\command" /ve /d "\"%SCRIPT_PATH%\" \"%%1\"" /f

:: 为文件夹背景添加右键菜单
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\MyPythonAction" /ve /d "AI工具箱" /f
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\MyPythonAction" /v "Icon" /d "%~dp0_internal\aitool.ico" /f
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\MyPythonAction\command" /ve /d "\"%SCRIPT_PATH%\" \"%%V\"" /f

echo 右键菜单添加成功！
pause