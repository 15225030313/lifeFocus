"""Pydantic 数据校验模型"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# ---------- 管理员 ----------
class AdminLogin(BaseModel):
    username: str
    password: str


# ---------- 分类 ----------
class CategoryCreate(BaseModel):
    category_name: str
    category_desc: Optional[str] = ""
    plate_type: int = 1
    sort: int = 0
    status: int = 1


class CategoryUpdate(BaseModel):
    category_name: Optional[str] = None
    category_desc: Optional[str] = None
    plate_type: Optional[int] = None
    sort: Optional[int] = None
    status: Optional[int] = None


class CategoryOut(BaseModel):
    id: int
    category_name: str
    category_desc: Optional[str] = ""
    plate_type: int
    sort: int
    status: int
    create_time: Optional[datetime] = None

    class Config:
        from_attributes = True


# ---------- 文章 ----------
class ArticleCreate(BaseModel):
    title: str
    cover_img: Optional[str] = ""
    intro: Optional[str] = ""
    content: Optional[str] = ""
    category_id: Optional[int] = None
    plate_type: int = 1
    is_top: int = 0
    status: int = 1


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    cover_img: Optional[str] = None
    intro: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[int] = None
    plate_type: Optional[int] = None
    is_top: Optional[int] = None
    status: Optional[int] = None


class ArticleListItem(BaseModel):
    id: int
    title: str
    cover_img: Optional[str] = ""
    intro: Optional[str] = ""
    category_id: Optional[int] = None
    plate_type: int
    view_count: int = 0
    is_top: int = 0
    status: int = 1
    create_time: Optional[datetime] = None
    category_name: Optional[str] = ""

    class Config:
        from_attributes = True


class ArticleOut(ArticleListItem):
    content: Optional[str] = ""
    update_time: Optional[datetime] = None
    prev_id: Optional[int] = None
    prev_title: Optional[str] = None
    next_id: Optional[int] = None
    next_title: Optional[str] = None


# ---------- 轮播图 ----------
class BannerCreate(BaseModel):
    banner_img: str
    article_id: Optional[int] = None
    sort: int = 0
    status: int = 1


class BannerUpdate(BaseModel):
    banner_img: Optional[str] = None
    article_id: Optional[int] = None
    sort: Optional[int] = None
    status: Optional[int] = None


class BannerOut(BaseModel):
    id: int
    banner_img: str
    article_id: Optional[int] = None
    sort: int
    status: int
    create_time: Optional[datetime] = None

    class Config:
        from_attributes = True


# ---------- 站点配置 ----------
class SiteConfigOut(BaseModel):
    id: int
    site_name: str
    copyright: str

    class Config:
        from_attributes = True


class SiteConfigUpdate(BaseModel):
    site_name: Optional[str] = None
    copyright: Optional[str] = None


# ---------- 其他 ----------
class PasswordChange(BaseModel):
    old_password: str
    new_password: str


class DashboardStat(BaseModel):
    total_articles: int
    life_articles: int
    wonder_articles: int
    total_views: int
    latest: list = []
