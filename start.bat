@echo off
chcp 65001 >nul
setlocal
set ROOT=%~dp0
set BACKEND=%ROOT%backend
set FRONTEND=%ROOT%frontend

echo ============================================
echo   生活奇观资讯站 - 一键启动
echo ============================================

REM 1. 后端虚拟环境与依赖
if not exist "%BACKEND%\.venv\Scripts\python.exe" (
  echo [1/4] 创建 Python 虚拟环境并安装依赖...
  python -m venv "%BACKEND%\.venv"
  call "%BACKEND%\.venv\Scripts\pip.exe" install -r "%BACKEND%\requirements.txt"
)

REM 2. 启动后端（首次自动建库建表、生成默认数据）
echo [2/4] 启动后端服务（托管前端 + 接口）...
start "lifeFocus-backend" /min cmd /k "cd /d %BACKEND% && call .venv\Scripts\activate.bat && uvicorn app.main:app --host 0.0.0.0 --port 8000"

REM 3. 前端依赖
if not exist "%FRONTEND%\node_modules" (
  echo [3/4] 安装前端依赖（首次较慢，请耐心等待）...
  cd /d %FRONTEND% && call npm install
)

REM 4. 构建前端（由后端统一托管）
echo [4/4] 构建前端...
cd /d %FRONTEND% && call npm run build

timeout /t 3 >nul
echo ============================================
echo   启动完成！
echo   前台首页 : http://localhost:8000
echo   后台管理 : http://localhost:8000/admin/login
echo   Swagger  : http://localhost:8000/docs
echo   默认账号 : admin / admin123
echo ============================================
start "" http://localhost:8000
pause
endlocal
