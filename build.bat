@echo off
chcp 65001

:: 删除旧的 build 和 dist 文件夹（不询问直接删除）
if exist build rd /s /q build
if exist dist rd /s /q dist
if exist main.spec del /q main.spec

:: 调用 PyInstaller
pyinstaller -i aitool.ico -w --add-data "aitool.ico;." --clean main.py
xcopy /q "setup.bat" "dist/main"
echo 打包完成！

pause