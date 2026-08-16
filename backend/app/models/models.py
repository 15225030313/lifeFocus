"""数据库模型定义（admin / category / article / banner / site_config）"""
from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey,
)
from app.database.database import Base


class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(100), nullable=False)  # MD5 加密存储
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(50), nullable=False)
    category_desc = Column(String(200), default="")
    plate_type = Column(Integer, nullable=False, default=1)  # 1=生活妙招 2=世界奇观
    sort = Column(Integer, default=0)
    status = Column(Integer, default=1)  # 1=启用 0=禁用
    create_time = Column(DateTime, default=datetime.now)


class Article(Base):
    __tablename__ = "article"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    cover_img = Column(String(255), default="")
    intro = Column(String(500), default="")
    content = Column(Text, default="")
    category_id = Column(Integer, ForeignKey("category.id"), nullable=True)
    plate_type = Column(Integer, nullable=False, default=1)  # 1=生活妙招 2=世界奇观
    view_count = Column(Integer, default=0)
    is_top = Column(Integer, default=0)  # 1=置顶
    status = Column(Integer, default=1)  # 1=已发布 0=草稿
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Banner(Base):
    __tablename__ = "banner"
    id = Column(Integer, primary_key=True, index=True)
    banner_img = Column(String(255), nullable=False)
    article_id = Column(Integer, nullable=True)  # 关联跳转文章
    sort = Column(Integer, default=0)
    status = Column(Integer, default=1)  # 1=启用 0=禁用
    create_time = Column(DateTime, default=datetime.now)


class SiteConfig(Base):
    """网站基础配置（扩展表，承载 4.5 系统管理需求）"""
    __tablename__ = "site_config"
    id = Column(Integer, primary_key=True, index=True)
    site_name = Column(String(100), default="生活奇观资讯站")
    copyright = Column(String(200), default="© 2026 生活奇观资讯展示网站")
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
