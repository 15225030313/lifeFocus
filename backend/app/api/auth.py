"""管理员登录与鉴权接口"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.models import Admin
from app.schemas.schemas import AdminLogin
from app.utils.response import success, fail
from app.utils.security import verify_password, create_token
from app.api.deps import get_current_admin

router = APIRouter(prefix="/api/admin", tags=["auth"])


@router.post("/login")
def login(body: AdminLogin, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.username == body.username).first()
    if not admin or not verify_password(body.password, admin.password):
        return fail(code=401, message="用户名或密码错误")
    token = create_token(admin.username)
    return success({"token": token, "username": admin.username}, message="登录成功")


@router.get("/me")
def me(username: str = Depends(get_current_admin)):
    return success({"username": username})
