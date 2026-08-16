"""轮播图接口：前台公开 + 后台管理"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.models import Banner
from app.schemas.schemas import BannerCreate, BannerUpdate, BannerOut
from app.utils.response import success, fail
from app.api.deps import get_current_admin

router = APIRouter(tags=["banner"])


@router.get("/api/banners", response_model=None)
def list_banners(db: Session = Depends(get_db)):
    q = db.query(Banner).filter(Banner.status == 1).order_by(Banner.sort.asc()).all()
    data = [BannerOut.from_orm(b).dict() for b in q]
    return success(data)


@router.get("/api/admin/banners", response_model=None)
def list_admin(db: Session = Depends(get_db), _: str = Depends(get_current_admin)):
    q = db.query(Banner).order_by(Banner.sort.asc()).all()
    data = [BannerOut.from_orm(b).dict() for b in q]
    return success(data)


@router.post("/api/admin/banners", response_model=None)
def create_banner(body: BannerCreate, db: Session = Depends(get_db),
                  _: str = Depends(get_current_admin)):
    obj = Banner(**body.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return success(BannerOut.from_orm(obj).dict(), message="轮播图添加成功")


@router.put("/api/admin/banners/{bid}", response_model=None)
def update_banner(bid: int, body: BannerUpdate, db: Session = Depends(get_db),
                  _: str = Depends(get_current_admin)):
    obj = db.query(Banner).filter(Banner.id == bid).first()
    if not obj:
        return fail(code=404, message="轮播图不存在")
    for k, v in body.dict(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    return success(BannerOut.from_orm(obj).dict(), message="轮播图更新成功")


@router.delete("/api/admin/banners/{bid}", response_model=None)
def delete_banner(bid: int, db: Session = Depends(get_db),
                  _: str = Depends(get_current_admin)):
    obj = db.query(Banner).filter(Banner.id == bid).first()
    if not obj:
        return fail(code=404, message="轮播图不存在")
    db.delete(obj)
    db.commit()
    return success(message="轮播图删除成功")
