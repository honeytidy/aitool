@echo off
chcp 65001

:: 检查是否具有管理员权限
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo 当前脚本没有管理员权限，正在尝试以管理员权限重新启动...
    powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

REM 删除所有文件的右键菜单项
reg delete "HKEY_CLASSES_ROOT\*\shell\aitool" /f

REM 删除所有文件夹的右键菜单项
reg delete "HKEY_CLASSES_ROOT\Directory\shell\aitool" /f

REM 删除文件夹背景的右键菜单项
reg delete "HKEY_CLASSES_ROOT\Directory\Background\shell\aitool" /f

echo 注册表项已成功删除！
pause