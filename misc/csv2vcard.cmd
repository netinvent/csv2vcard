@echo off

setlocal

if exist "%~dp0..\python.exe" (
"%~dp0..\python" -m csv2vcard %*
) else if exist "%~dp0python.exe" (
"%~dp0python" -m csv2vcard %*
) else (
"python" -m csv2vcard %*
)

endlocal
