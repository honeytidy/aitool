@echo off
chcp 65001

:: ɾ���ɵ� build �� dist �ļ��У���ѯ��ֱ��ɾ����
if exist build rd /s /q build
if exist dist rd /s /q dist
rem if exist main.spec del /q main.spec

:: ����Ƿ���й���ԱȨ��
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ��ǰ�ű�û�й���ԱȨ�ޣ����ڳ����Թ���ԱȨ����������...
    powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    rem exit /b
)

:: ���� PyInstaller
pyinstaller -i aitool.ico -w --clean main.py