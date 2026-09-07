Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
WshShell.CurrentDirectory = scriptDir
' Run python server.py silently in the background (0 = hidden window)
WshShell.Run "python server.py --no-browser", 0, False
