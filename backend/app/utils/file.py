"""图片上传工具：保存文件并返回可访问 URL"""
import os
import uuid

from fastapi import UploadFile, HTTPException

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPLOAD_DIR = os.path.join(BASE_DIR, "static", "uploads")

ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp"}
MAX_SIZE = 2 * 1024 * 1024  # 2MB


def save_upload(file: UploadFile) -> str:
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(status_code=400, detail="不支持的图片格式，仅支持 jpg/png/webp")
    content = file.file.read()
    if len(content) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="图片大小不能超过 2MB")
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    filename = f"{uuid.uuid4().hex}{ext}"
    with open(os.path.join(UPLOAD_DIR, filename), "wb") as f:
        f.write(content)
    return f"/static/uploads/{filename}"
