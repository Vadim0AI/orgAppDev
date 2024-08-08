@echo off
echo Starting script...
set PYTHONPATH=C:\Code\orgApp Dev
cd /d "C:\Code\orgApp Dev"
echo Current directory: %cd%
echo Running pythonw.exe...
start "" /b "venv\Scripts\pythonw.exe" "."
echo Script started
pause