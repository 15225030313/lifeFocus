"""数据库连接与会话管理（支持 SQLite / MySQL 一键切换）

切换方式（二选一）：
  1) 改下方 DB_TYPE = "mysql"   （最简单，推荐新手）
  2) 或设置环境变量 DB_TYPE=mysql  （适合部署）

切到 MySQL 后，记得把 MYSQL_PASSWORD 改成你安装 MySQL 时设的 root 密码。
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ===== 数据库类型：sqlite（默认，零配置） / mysql =====
DB_TYPE = os.getenv("DB_TYPE", "mysql").lower()

# ===== MySQL 连接信息（仅 DB_TYPE=mysql 时生效）=====
# 把 MYSQL_PASSWORD 的空字符串改成你的 MySQL root 密码即可。
MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "Zcc117713190")   # ← 改成你的 MySQL root 密码
MYSQL_DB = os.getenv("MYSQL_DB", "life_focus")

# backend 目录（app 的上级目录）作为数据库文件所在根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "app.db")

if DB_TYPE == "mysql":
    # MySQL 连接串：mysql + pymysql 驱动
    SQLALCHEMY_DATABASE_URL = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
        f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4"
    )
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_pre_ping=True,    # 自动剔除失效连接
        pool_recycle=3600,     # 避开 MySQL 默认 8 小时断连
    )
else:
    # SQLite 内嵌文件数据库（默认）
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI 依赖：提供数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
