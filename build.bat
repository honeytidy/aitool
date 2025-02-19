@echo off
chcp 65001

:: 删除旧的 build 和 dist 文件夹（不询问直接删除）
if exist build rd /s /q build
if exist dist rd /s /q dist
rem if exist main.spec del /q main.spec

:: 检查是否具有管理员权限
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo 当前脚本没有管理员权限，正在尝试以管理员权限重新启动...
    powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    rem exit /b
)

:: 调用 PyInstaller
pyinstaller -i aitool.ico -w --clean main.py