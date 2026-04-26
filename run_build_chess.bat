@echo off
cd /d "%~dp0"

REM Try Python launchers in order of preference.
REM 'py' is the Windows Python Launcher, installed with standard Python installers
REM and placed in C:\Windows so it's on PATH even when 'python' isn't.
where /q py      && (py      "%~dp0build_chess.py" & goto :end)
where /q python  && (python  "%~dp0build_chess.py" & goto :end)
where /q python3 && (python3 "%~dp0build_chess.py" & goto :end)

echo.
echo ERROR: No Python installation was found on PATH.
echo.
echo To fix, do one of:
echo   1. Install Python from https://www.python.org/downloads/
echo      (during install, tick "Add python.exe to PATH"), OR
echo   2. If Python is already installed, reinstall with "Add to PATH" checked, OR
echo   3. Run manually:   py "%~dp0build_chess.py"
echo.

:end
pause
