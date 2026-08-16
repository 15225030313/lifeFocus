@echo off
chcp 65001 >nul
cd /d %~dp0
if not exist ".venv\Scripts\python.exe" (
  python -m venv .venv
  call .venv\Scripts\pip.exe install -r requirements.txt
)
.venv\Scripts\activate.bat
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
