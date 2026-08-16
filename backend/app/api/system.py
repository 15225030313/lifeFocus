"""系统管理接口：上传 / 站点配置 / 修改密码 / 仪表盘"""
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.models import Admin, SiteConfig, Article, Category
from app.schemas.schemas import SiteConfigUpdate, PasswordChange, SiteConfigOut
from app.utils.response import success, fail
from app.utils.security import verify_password, hash_password
from app.utils.file import save_upload
from app.api.deps import get_current_admin

router = APIRouter(tags=["system"])


# 图片上传
@router.post("/api/admin/upload", response_model=None)
def upload(file: UploadFile = File(...), _: str = Depends(get_current_admin)):
    url = save_upload(file)
    return success({"url": url}, message="上传成功")


# 站点配置（公开）
@router.get("/api/site", response_model=None)
def get_site(db: Session = Depends(get_db)):
    cfg = db.query(SiteConfig).first()
    if not cfg:
        cfg = SiteConfig()
        db.add(cfg)
        db.commit()
    return success(SiteConfigOut.from_orm(cfg).dict())


# 站点配置（后台）
@router.get("/api/admin/site", response_model=None)
def get_site_admin(db: Session = Depends(get_db), _: str = Depends(get_current_admin)):
    cfg = db.query(SiteConfig).first()
    return success(SiteConfigOut.from_orm(cfg).dict())


@router.put("/api/admin/site", response_model=None)
def update_site(body: SiteConfigUpdate, db: Session = Depends(get_db),
                _: str = Depends(get_current_admin)):
    cfg = db.query(SiteConfig).first()
    if not cfg:
        cfg = SiteConfig()
        db.add(cfg)
        db.flush()
    for k, v in body.dict(exclude_unset=True).items():
        setattr(cfg, k, v)
    db.commit()
    return success(SiteConfigOut.from_orm(cfg).dict(), message="站点配置已更新")


# 修改密码
@router.put("/api/admin/password", response_model=None)
def change_password(body: PasswordChange, db: Session = Depends(get_db),
                   username: str = Depends(get_current_admin)):
    admin = db.query(Admin).filter(Admin.username == username).first()
    if not admin or not verify_password(body.old_password, admin.password):
        return fail(code=400, message="原密码错误")
    if len(body.new_password) < 6:
        return fail(code=400, message="新密码至少 6 位")
    admin.password = hash_password(body.new_password)
    db.commit()
    return success(message="密码修改成功")


# 仪表盘统计
@router.get("/api/admin/dashboard", response_model=None)
def dashboard(db: Session = Depends(get_db), _: str = Depends(get_current_admin)):
    total = db.query(Article).count()
    life = db.query(Article).filter(Article.plate_type == 1).count()
    wonder = db.query(Article).filter(Article.plate_type == 2).count()
    views = db.query(Article).with_entities(Article.view_count).all()
    total_views = sum(v[0] for v in views)
    latest = db.query(Article).order_by(Article.id.desc()).limit(10).all()
    latest_data = [{
        "id": a.id, "title": a.title,
        "plate_type": a.plate_type, "view_count": a.view_count,
        "status": a.status, "create_time": a.create_time,
    } for a in latest]
    return success({
        "total_articles": total,
        "life_articles": life,
        "wonder_articles": wonder,
        "total_views": total_views,
        "latest": latest_data,
    })
