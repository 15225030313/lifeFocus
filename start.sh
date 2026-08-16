#!/usr/bin/env bash
set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
BACKEND="$ROOT/backend"
FRONTEND="$ROOT/frontend"

echo "============================================"
echo "  生活奇观资讯站 - 一键启动"
echo "============================================"

# 1. 后端虚拟环境与依赖
if [ ! -x "$BACKEND/.venv/bin/python" ]; then
  echo "[1/4] 创建 Python 虚拟环境并安装依赖..."
  python3 -m venv "$BACKEND/.venv"
  "$BACKEND/.venv/bin/pip" install -r "$BACKEND/requirements.txt"
fi

# 2. 启动后端（后台运行）
echo "[2/4] 启动后端服务（托管前端 + 接口）..."
"$BACKEND/.venv/bin/uvicorn" app.main:app --host 0.0.0.0 --port 8000 \
  > "$BACKEND/backend.log" 2>&1 &
echo "      后端 PID: $!"

# 3. 前端依赖
if [ ! -d "$FRONTEND/node_modules" ]; then
  echo "[3/4] 安装前端依赖（首次较慢）..."
  (cd "$FRONTEND" && npm install)
fi

# 4. 构建前端
echo "[4/4] 构建前端..."
(cd "$FRONTEND" && npm run build)

sleep 2
echo "============================================"
echo "  启动完成！"
echo "  前台首页 : http://localhost:8000"
echo "  后台管理 : http://localhost:8000/admin/login"
echo "  Swagger  : http://localhost:8000/docs"
echo "  默认账号 : admin / admin123"
echo "============================================"
