; aitoolSetup.iss - 包含右键菜单和启动程序选项的 Inno Setup 脚本示例

[Setup]
; 程序名称和版本号
AppName=aitool
AppVersion=1.0

; 默认安装目录为 "Program Files\aitool"
DefaultDirName={commonpf}\aitool

; 设置开始菜单默认快捷方式组名称为“aitool”
DefaultGroupName=aitool

; 显式允许用户选择安装目录（默认是允许，不设置或设置为 no 均可）
DisableDirPage=no

; 安装程序输出文件名
OutputBaseFilename=aitoolSetup

; 启用 LZMA 压缩以及固实压缩
Compression=zip
SolidCompression=yes

; 指定安装程序的图标
SetupIconFile=aitool.ico

[Files]
; 将位于脚本同一目录下的 aitool.exe 复制到安装目录中
Source: "aitool.exe"; DestDir: "{app}"; Flags: ignoreversion
; 复制当前目录下 _internal 文件夹中的所有内容到安装目录下的 _internal 文件夹
Source: "_internal\*"; DestDir: "{app}\_internal"; Flags: recursesubdirs createallsubdirs

[Icons]
; 在开始菜单创建程序图标
Name: "{group}\aitool"; Filename: "{app}\aitool.exe"

[Registry]
; --- 添加文件右键菜单 ---
; 在所有文件上鼠标右键时显示 "AI工具箱" 选项
Root: HKCR; Subkey: "*\shell\aitool"; ValueType: string; ValueName: ""; ValueData: "AI工具箱"; Flags: uninsdeletekey
Root: HKCR; Subkey: "*\shell\aitool\command"; ValueType: string; ValueName: ""; ValueData: """{app}\aitool.exe"" ""%1"""; Flags: uninsdeletekey
; 添加图标字段，使右键菜单项显示指定图标（如使用 aitool.exe 内嵌图标）
Root: HKCR; Subkey: "*\shell\aitool"; ValueType: string; ValueName: "Icon"; ValueData: """{app}\aitool.exe"""; Flags: uninsdeletevalue
Root: HKCR; Subkey: "*\shell\aitool\command"; ValueType: string; ValueName: ""; ValueData: """{app}\aitool.exe"" ""%1"""; Flags: uninsdeletekey

; --- 添加文件夹右键菜单 ---
; 在所有文件夹上鼠标右键时显示 "AI工具箱" 选项
Root: HKCR; Subkey: "Directory\shell\aitool"; ValueType: string; ValueName: ""; ValueData: "AI工具箱"; Flags: uninsdeletekey
Root: HKCR; Subkey: "Directory\shell\aitool\command"; ValueType: string; ValueName: ""; ValueData: """{app}\aitool.exe"" ""%1"""; Flags: uninsdeletekey
; 添加右键菜单图标
Root: HKCR; Subkey: "Directory\shell\aitool"; ValueType: string; ValueName: "Icon"; ValueData: """{app}\aitool.exe"""; Flags: uninsdeletevalue
Root: HKCR; Subkey: "Directory\shell\aitool\command"; ValueType: string; ValueName: ""; ValueData: """{app}\aitool.exe"" ""%1"""; Flags: uninsdeletekey

; --- 当前路径（文件夹背景）右键菜单 ---
; 在文件夹空白处鼠标右键时显示 "AI工具箱" 选项
Root: HKCR; Subkey: "Directory\Background\shell\aitool"; ValueType: string; ValueName: ""; ValueData: "AI工具箱"; Flags: uninsdeletekey
; 为当前路径右键菜单添加图标
Root: HKCR; Subkey: "Directory\Background\shell\aitool"; ValueType: string; ValueName: "Icon"; ValueData: """{app}\aitool.exe"""; Flags: uninsdeletevalue
; 此处使用 %V 代表当前背景所在的路径
Root: HKCR; Subkey: "Directory\Background\shell\aitool\command"; ValueType: string; ValueName: ""; ValueData: """{app}\aitool.exe"" ""%V"""; Flags: uninsdeletekey

[Run]
; 在安装完成后，提供复选框让用户选择是否启动程序
Filename: "{app}\aitool.exe"; Description: "启动 aitool"; Flags: nowait postinstall skipifsilent