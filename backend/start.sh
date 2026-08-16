#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
if [ ! -x .venv/bin/python ]; then
  python3 -m venv .venv
  .venv/bin/pip install -r requirements.txt
fi
# 首次启动自动建库建表、生成默认数据
.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
