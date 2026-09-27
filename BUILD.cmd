@echo off
cd /d "%~dp0"
py -3 -m unittest discover -s tests -v
if errorlevel 1 goto failed
py -3 build.py
if errorlevel 1 goto failed
echo Package created in dist.
pause
exit /b 0
:failed
echo Build failed. Check the error above.
pause
exit /b 1
