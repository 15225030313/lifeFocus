# 生活奇观资讯展示网站（lifeFocus）

一款轻量化资讯展示类**前后端分离**网站，专注分享「生活小妙招」与「世界奇观」两类内容。
前端 **Vue3 + TypeScript + Element Plus**，后端 **FastAPI + SQLite（内嵌零配置）**，
克隆即可运行，无需安装 MySQL / Redis 等第三方服务。

---

## 1. 技术栈

| 层 | 技术 |
|---|---|
| 前端 | Vue 3（组合式 API）· TypeScript · Element Plus · Vue Router 4 · Pinia · Axios · Vite |
| 后端 | FastAPI · SQLAlchemy · Pydantic · JWT · SQLite（内嵌 `.db` 文件） |

## 2. 功能概览

**前台（公开）**：首页轮播 + 双板块分区、文章列表（分类/排序/分页）、文章详情（上下篇/浏览量/图片放大）、全站搜索、关于本站、404 页。
**后台（JWT 鉴权）**：管理员登录、仪表盘统计、文章管理（增删改查/批量/草稿置顶/富文本）、分类管理、轮播图与站点配置、修改密码。

## 3. 目录结构

```
lifeFocus/
├── backend/                 # FastAPI 后端
│   ├── app/
│   │   ├── api/             # 接口路由（auth/category/article/banner/system）
│   │   ├── models/          # SQLAlchemy 模型
│   │   ├── schemas/         # Pydantic 校验
│   │   ├── utils/           # 安全(JWT/MD5)、文件上传、统一返回
│   │   ├── database/        # 连接 & 初始化默认数据
│   │   └── main.py          # 应用入口（同时托管构建后的前端）
│   ├── static/uploads/      # 上传图片
│   ├── app.db               # SQLite 数据库（首次启动自动生成）
│   └── requirements.txt
├── frontend/                # Vue3 前端
│   ├── src/
│   │   ├── api/  components/  views/  router/  store/  utils/  styles/
│   └── package.json
├── start.bat / start.sh     # 一键启动
└── README.md
```

> 后端 `main.py` 在返回前端构建产物 `frontend/dist` 的同时提供 `/api` 接口，因此**一个地址即可同时访问前端与接口**。

## 4. 环境依赖

- Python 3.9+
- Node.js 16+（含 npm）
- 无需 MySQL / Redis

## 5. 快速启动

### 方式一：一键启动（推荐）
在项目根目录执行：
- Windows：双击 `start.bat`
- macOS / Linux：`./start.sh`

脚本会自动：创建 Python 虚拟环境并安装依赖 → 安装前端依赖 → 构建前端 → 启动后端（同时托管前端）。
启动完成后访问 **http://localhost:8000**。

### 方式二：分开启动
**后端**（自动建库建表、生成默认数据）：
```bash
cd backend
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
# 接口文档：http://localhost:8000/docs
```
**前端开发模式**（独立 Vite 开发服务器，含热更新，默认 5173 端口，经代理访问后端）：
```bash
cd frontend
npm install
npm run dev
# 访问：http://localhost:5173
```

## 6. 访问地址

| 页面 | 地址 |
|---|---|
| 前台首页 | http://localhost:8000 |
| 后台登录 | http://localhost:8000/admin/login |
| Swagger 文档 | http://localhost:8000/docs |
| Redoc 文档 | http://localhost:8000/redoc |

## 7. 后台默认账号

- 用户名：`admin`
- 密码：`admin123`
- 首次登录后请到「系统管理 → 修改密码」修改

## 8. 数据库说明（SQLite 内嵌）

- 数据库文件 `backend/app.db` 随项目生成，**无需手动建库建表**。
- 首次启动自动初始化：默认管理员、两大板块 9 个分类、8 篇示例文章、2 条轮播。
- 数据持久化：本地操作永久保存，重启不丢失。
- 迁移 MySQL（一键切换，业务代码无需改动）：
  1. 安装 MySQL 8.0 并启动服务（默认端口 3306），用 root 登录执行：
     `CREATE DATABASE life_focus CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;`
  2. 打开 `backend/app/database/database.py`，把 `DB_TYPE = "sqlite"` 改为 `DB_TYPE = "mysql"`，
     并把 `MYSQL_PASSWORD = ""` 改成你安装 MySQL 时设的 root 密码。
  3. 安装依赖（已含 `pymysql`），重启后端即可。首次启动会自动建表并写入默认数据。

## 9. 接口规范

- 统一返回：`{ code, message, data, total? }`
- 分页参数：`page`、`page_size`；返回 `total`（总条数）。
- 图片上传：单图，返回 `/static/uploads/xxx` 访问地址。
- 前台接口公开；后台接口需 `Authorization: Bearer <token>`。

## 10. 常见问题（FAQ）

| 现象 | 解决 |
|---|---|
| 端口 8000 被占用 | 修改 `uvicorn` 的 `--port` 参数，或关闭占用程序 |
| 前端图片裂图 | 占位图依赖网络（placehold.co）；本地上传的图片存于 `backend/static/uploads` |
| 数据库初始化异常 | 删除 `backend/app.db` 后重启后端，会重新建库建表 |
| 前端 `npm install` 慢 | 使用国内镜像，如 `npm config set registry https://registry.npmmirror.com` |
| 后台接口 401 | 登录过期，重新登录获取 token |

---

© 生活奇观资讯展示网站 · 前后端分离演示项目
