@echo off
chcp 65001

:: 删除旧的 build 和 dist 文件夹（不询问直接删除）
if exist build rd /s /q build
if exist dist rd /s /q dist
if exist main.spec del /q main.spec

:: 检查是否具有管理员权限
rem net session >nul 2>&1
rem if %errorlevel% neq 0 (
rem     echo 当前脚本没有管理员权限，正在尝试以管理员权限重新启动...
rem     powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
rem     rem exit /b
rem )

:: 调用 PyInstaller
pyinstaller -i aitool.ico -w --add-data "aitool.ico;." main.py
xcopy /q "setup.bat" "dist/main"
echo 打包完成！

pause