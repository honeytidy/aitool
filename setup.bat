@echo off
chcp 65001

:: ����Ƿ���й���ԱȨ��
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ��ǰ�ű�û�й���ԱȨ�ޣ����ڳ����Թ���ԱȨ����������...
    powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

set SCRIPT_PATH="%~dp0dist\main\main.exe"

reg add "HKEY_CLASSES_ROOT\*\shell\MyPythonAction" /ve /d "AI������" /f
reg add "HKEY_CLASSES_ROOT\*\shell\MyPythonAction" /v "Icon" /d "%~dp0aitool.ico" /f
reg add "HKEY_CLASSES_ROOT\*\shell\MyPythonAction\command" /ve /d "%SCRIPT_PATH% \"%%1\"" /f

:: Ϊ�����ļ�������Ҽ��˵�
reg add "HKEY_CLASSES_ROOT\Directory\shell\MyPythonAction" /ve /d "AI������" /f
reg add "HKEY_CLASSES_ROOT\Directory\shell\MyPythonAction" /v "Icon" /d "%~dp0aitool.ico" /f
reg add "HKEY_CLASSES_ROOT\Directory\shell\MyPythonAction\command" /ve /d "%SCRIPT_PATH% \"%%1\"" /f

echo �Ҽ��˵���ӳɹ���
pause