; Упрощённый скрипт для Inno Setup
[Setup]
AppName=Code Snippet Manager
AppVersion=1.0
AppPublisher=DeserHermit
AppPublisherURL=https://github.com/DeserHermit/CodeSnippetManager
DefaultDirName={autopf}\CodeSnippetManager
DefaultGroupName=Code Snippet Manager
OutputDir=installer
OutputBaseFilename=CodeSnippetManager_Setup
Compression=lzma2
SolidCompression=yes
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\CodeSnippetManager.exe
PrivilegesRequired=lowest

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[Tasks]
; Убираем флаги, оставляем только описание
Name: "desktopicon"; Description: "Создать ярлык на рабочем столе"; GroupDescription: "Дополнительные задачи:"
Name: "quicklaunchicon"; Description: "Создать ярлык в панели быстрого запуска"; GroupDescription: "Дополнительные задачи:"

[Files]
Source: "dist\CodeSnippetManager\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Code Snippet Manager"; Filename: "{app}\CodeSnippetManager.exe"
Name: "{group}\Удалить программу"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Code Snippet Manager"; Filename: "{app}\CodeSnippetManager.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\CodeSnippetManager.exe"; Description: "Запустить Code Snippet Manager"; Flags: postinstall nowait skipifsilent