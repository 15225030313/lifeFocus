"""分类管理接口：前台公开列表 + 后台 CRUD"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.models import Category, Article
from app.schemas.schemas import CategoryCreate, CategoryUpdate, CategoryOut
from app.utils.response import success, fail
from app.api.deps import get_current_admin

router = APIRouter(tags=["category"])


# ---------- 前台公开 ----------
@router.get("/api/categories", response_model=None)
def list_categories(plate_type: int = None, db: Session = Depends(get_db)):
    q = db.query(Category)
    if plate_type is not None:
        q = q.filter(Category.plate_type == plate_type)
    q = q.filter(Category.status == 1).order_by(Category.sort.asc())
    data = [CategoryOut.from_orm(c).dict() for c in q.all()]
    return success(data)


# ---------- 后台（需登录） ----------
@router.get("/api/admin/categories", response_model=None)
def list_admin(plate_type: int = None, db: Session = Depends(get_db),
               _: str = Depends(get_current_admin)):
    q = db.query(Category)
    if plate_type is not None:
        q = q.filter(Category.plate_type == plate_type)
    q = q.order_by(Category.sort.asc())
    data = [CategoryOut.from_orm(c).dict() for c in q.all()]
    return success(data)


@router.post("/api/admin/categories", response_model=None)
def create_category(body: CategoryCreate, db: Session = Depends(get_db),
                    _: str = Depends(get_current_admin)):
    obj = Category(**body.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return success(CategoryOut.from_orm(obj).dict(), message="分类创建成功")


@router.put("/api/admin/categories/{cid}", response_model=None)
def update_category(cid: int, body: CategoryUpdate, db: Session = Depends(get_db),
                    _: str = Depends(get_current_admin)):
    obj = db.query(Category).filter(Category.id == cid).first()
    if not obj:
        return fail(code=404, message="分类不存在")
    for k, v in body.dict(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    return success(CategoryOut.from_orm(obj).dict(), message="分类更新成功")


@router.delete("/api/admin/categories/{cid}", response_model=None)
def delete_category(cid: int, db: Session = Depends(get_db),
                    _: str = Depends(get_current_admin)):
    obj = db.query(Category).filter(Category.id == cid).first()
    if not obj:
        return fail(code=404, message="分类不存在")
    # 禁止删除已有文章关联的分类
    if db.query(Article).filter(Article.category_id == cid).count() > 0:
        return fail(code=400, message="该分类下存在文章，无法删除")
    db.delete(obj)
    db.commit()
    return success(message="分类删除成功")
