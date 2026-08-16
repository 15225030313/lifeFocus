"""文章接口：前台公开浏览 + 后台管理 CRUD"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.models import Article, Category
from app.schemas.schemas import ArticleCreate, ArticleUpdate, ArticleListItem, ArticleOut
from app.utils.response import success, fail
from app.api.deps import get_current_admin

router = APIRouter(tags=["article"])


def _to_list_item(a: Article, cat_name: str = ""):
    d = ArticleListItem.from_orm(a).dict()
    d["category_name"] = cat_name
    return d


# ---------- 前台：文章列表（已发布） ----------
@router.get("/api/articles", response_model=None)
def list_articles(
    plate_type: int = None,
    category_id: int = None,
    keyword: str = None,
    sort: str = "latest",  # latest | hot
    page: int = 1,
    page_size: int = 12,
    db: Session = Depends(get_db),
):
    q = db.query(Article).filter(Article.status == 1)
    if plate_type is not None:
        q = q.filter(Article.plate_type == plate_type)
    if category_id is not None:
        q = q.filter(Article.category_id == category_id)
    if keyword:
        like = f"%{keyword}%"
        q = q.filter(Article.title.like(like) | Article.content.like(like) | Article.intro.like(like))

    total = q.count()
    if sort == "hot":
        q = q.order_by(Article.view_count.desc(), Article.id.desc())
    else:
        q = q.order_by(Article.is_top.desc(), Article.id.desc())

    items = q.offset((page - 1) * page_size).limit(page_size).all()
    cat_names = {c.id: c.category_name for c in db.query(Category).all()}
    data = [_to_list_item(a, cat_names.get(a.category_id, "")) for a in items]
    return success(data, total=total)


# ---------- 前台：文章详情（浏览量 +1，含上下篇） ----------
@router.get("/api/articles/{aid}", response_model=None)
def article_detail(aid: int, db: Session = Depends(get_db)):
    art = db.query(Article).filter(Article.id == aid, Article.status == 1).first()
    if not art:
        return fail(code=404, message="文章不存在或已下架")
    art.view_count += 1
    db.commit()

    cat = db.query(Category).filter(Category.id == art.category_id).first()
    cat_name = cat.category_name if cat else ""
    d = ArticleOut.from_orm(art).dict()
    d["category_name"] = cat_name

    # 同板块已发布文章的上下篇
    siblings = db.query(Article).filter(
        Article.plate_type == art.plate_type, Article.status == 1
    ).order_by(Article.id.asc()).all()
    ids = [s.id for s in siblings]
    if art.id in ids:
        idx = ids.index(art.id)
        if idx > 0:
            d["prev_id"] = ids[idx - 1]
            d["prev_title"] = siblings[idx - 1].title
        if idx < len(ids) - 1:
            d["next_id"] = ids[idx + 1]
            d["next_title"] = siblings[idx + 1].title
    return success(d)


# ---------- 后台：文章列表（全部状态） ----------
@router.get("/api/admin/articles", response_model=None)
def list_admin(
    plate_type: int = None, category_id: int = None,
    keyword: str = None, status: int = None,
    page: int = 1, page_size: int = 12,
    db: Session = Depends(get_db), _: str = Depends(get_current_admin),
):
    q = db.query(Article)
    if plate_type is not None:
        q = q.filter(Article.plate_type == plate_type)
    if category_id is not None:
        q = q.filter(Article.category_id == category_id)
    if status is not None:
        q = q.filter(Article.status == status)
    if keyword:
        like = f"%{keyword}%"
        q = q.filter(Article.title.like(like) | Article.intro.like(like))
    total = q.count()
    q = q.order_by(Article.is_top.desc(), Article.id.desc())
    items = q.offset((page - 1) * page_size).limit(page_size).all()
    cat_names = {c.id: c.category_name for c in db.query(Category).all()}
    data = [_to_list_item(a, cat_names.get(a.category_id, "")) for a in items]
    return success(data, total=total)


@router.post("/api/admin/articles", response_model=None)
def create_article(body: ArticleCreate, db: Session = Depends(get_db),
                   _: str = Depends(get_current_admin)):
    obj = Article(**body.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return success(ArticleOut.from_orm(obj).dict(), message="文章发布成功")


@router.put("/api/admin/articles/{aid}", response_model=None)
def update_article(aid: int, body: ArticleUpdate, db: Session = Depends(get_db),
                  _: str = Depends(get_current_admin)):
    obj = db.query(Article).filter(Article.id == aid).first()
    if not obj:
        return fail(code=404, message="文章不存在")
    for k, v in body.dict(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    return success(ArticleOut.from_orm(obj).dict(), message="文章更新成功")


@router.delete("/api/admin/articles/{aid}", response_model=None)
def delete_article(aid: int, db: Session = Depends(get_db),
                  _: str = Depends(get_current_admin)):
    obj = db.query(Article).filter(Article.id == aid).first()
    if not obj:
        return fail(code=404, message="文章不存在")
    db.delete(obj)
    db.commit()
    return success(message="文章删除成功")


@router.post("/api/admin/articles/batch-delete", response_model=None)
def batch_delete(ids: list[int], db: Session = Depends(get_db),
                 _: str = Depends(get_current_admin)):
    if not ids:
        return fail(code=400, message="请选择要删除的文章")
    db.query(Article).filter(Article.id.in_(ids)).delete(synchronize_session=False)
    db.commit()
    return success(message=f"已删除 {len(ids)} 篇文章")
