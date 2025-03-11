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

reg add "HKEY_CLASSES_ROOT\*\shell\aitool" /ve /d "AI工具箱" /f
reg add "HKEY_CLASSES_ROOT\*\shell\aitool" /v "Icon" /d "%~dp0_internal\aitool.ico" /f
reg add "HKEY_CLASSES_ROOT\*\shell\aitool\command" /ve /d "\"%SCRIPT_PATH%\" \"%%1\"" /f


:: 为所有文件夹添加右键菜单
reg add "HKEY_CLASSES_ROOT\Directory\shell\aitool" /ve /d "AI工具箱" /f
reg add "HKEY_CLASSES_ROOT\Directory\shell\aitool" /v "Icon" /d "%~dp0_internal\aitool.ico" /f
reg add "HKEY_CLASSES_ROOT\Directory\shell\aitool\command" /ve /d "\"%SCRIPT_PATH%\" \"%%1\"" /f

:: 为文件夹背景添加右键菜单
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\aitool" /ve /d "AI工具箱" /f
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\aitool" /v "Icon" /d "%~dp0_internal\aitool.ico" /f
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\aitool\command" /ve /d "\"%SCRIPT_PATH%\" \"%%V\"" /f

echo 右键菜单添加成功！
pause