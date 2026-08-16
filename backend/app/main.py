"""FastAPI 应用入口"""
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.database.database import BASE_DIR
from app.database.init_db import init_db
from app.api import auth, category, article, banner, system

app = FastAPI(title="生活奇观资讯站 API", version="1.0.0", description="前后端分离资讯网站后端")

# 全局跨域（本地开发演示）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router)
app.include_router(category.router)
app.include_router(article.router)
app.include_router(banner.router)
app.include_router(system.router)

# 静态资源（上传图片）
STATIC_DIR = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# 前端构建产物（由 vite build 生成），用于单地址统一托管
DIST_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend", "dist"))
INDEX_FILE = os.path.join(DIST_DIR, "index.html")


@app.on_event("startup")
def on_startup():
    # 首次启动自动建库建表 + 默认数据
    init_db()


@app.get("/")
def root():
    if os.path.isfile(INDEX_FILE):
        return FileResponse(INDEX_FILE)
    return {"code": 200, "message": "生活奇观资讯站 API 运行中", "docs": "/docs"}


@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    # 未匹配到的前端路由兜底返回 index.html；API/文档类路径返回 404
    if full_path.startswith(("api", "docs", "openapi", "redoc")):
        raise HTTPException(status_code=404, detail="Not Found")
    file_path = os.path.join(DIST_DIR, full_path)
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    if os.path.isfile(INDEX_FILE):
        return FileResponse(INDEX_FILE)
    raise HTTPException(status_code=404, detail="前端未构建，请先执行前端构建（npm run build）")
