"""首次启动自动建表并写入默认数据（管理员/分类/轮播/示例文章）"""
from datetime import datetime

from app.database.database import engine, SessionLocal, Base
from app.models.models import Admin, Category, Article, Banner, SiteConfig
from app.utils.security import hash_password


DEFAULT_ADMIN = {"username": "admin", "password": "admin123"}

CATEGORIES = [
    # 生活妙招 (plate_type=1)
    {"category_name": "居家收纳", "category_desc": "空间利用与整理技巧", "plate_type": 1, "sort": 1},
    {"category_name": "清洁技巧", "category_desc": "高效清洁小窍门", "plate_type": 1, "sort": 2},
    {"category_name": "美食妙招", "category_desc": "厨房与烹饪技巧", "plate_type": 1, "sort": 3},
    {"category_name": "生活应急", "category_desc": "突发情况应对常识", "plate_type": 1, "sort": 4},
    {"category_name": "护肤穿搭", "category_desc": "日常护理与穿搭", "plate_type": 1, "sort": 5},
    # 世界奇观 (plate_type=2)
    {"category_name": "自然奇观", "category_desc": "自然地貌与生态奇景", "plate_type": 2, "sort": 1},
    {"category_name": "人文古迹", "category_desc": "历史遗迹与文明印记", "plate_type": 2, "sort": 2},
    {"category_name": "现代地标", "category_desc": "城市与现代建筑地标", "plate_type": 2, "sort": 3},
    {"category_name": "小众秘境", "category_desc": "鲜为人知的绝美之地", "plate_type": 2, "sort": 4},
]

SAMPLE_ARTICLES = [
    {
        "title": "5 个让衣柜瞬间清爽的收纳妙招",
        "plate_type": 1, "category_name": "居家收纳",
        "cover_img": "/static/uploads/lifehack_organize.jpg",
        "intro": "换季整理不再头疼，几个小技巧让空间利用率翻倍。",
        "content": "<p>换季最让人头疼的就是衣柜爆满。下面分享 5 个实用收纳法：</p><p>1. 按使用频率分层；2. 真空压缩换季被褥；3. 统一收纳盒；4. 竖立折叠法；5. 一进一出原则。</p>",
        "is_top": 1,
    },
    {
        "title": "厨房油污一擦即净的清洁公式",
        "plate_type": 1, "category_name": "清洁技巧",
        "cover_img": "/static/uploads/lifehack_clean.jpg",
        "intro": "小苏打 + 白醋，天然去油不伤手。",
        "content": "<p>厨房重油污不用愁。将小苏打撒在油垢处，喷上白醋，静置 5 分钟后擦拭，效果惊人。</p>",
    },
    {
        "title": "煮米饭更香的 3 个隐藏技巧",
        "plate_type": 1, "category_name": "美食妙招",
        "cover_img": "/static/uploads/lifehack_cook.jpg",
        "intro": "加一勺它，米饭粒粒分明还回甜。",
        "content": "<p>煮饭时加几滴油或一小勺盐，能让米粒更亮更香；浸泡 20 分钟后再煮口感更佳。</p>",
    },
    {
        "title": "突发停电时的家庭应急清单",
        "plate_type": 1, "category_name": "生活应急",
        "cover_img": "/static/uploads/lifehack_emergency.jpg",
        "intro": "提前准备，停电也不慌。",
        "content": "<p>常备手电、充电宝、饮用水与简易药品；燃气阀门及时关闭；保持手机电量。</p>",
    },
    {
        "title": "极光是怎么形成的？",
        "plate_type": 2, "category_name": "自然奇观",
        "cover_img": "/static/uploads/wonder_aurora.jpg",
        "intro": "太阳风与地球磁场的浪漫共舞。",
        "content": "<p>极光是太阳带电粒子进入地球磁层，与高层大气分子碰撞发光的现象，多见于高纬度地区。</p>",
        "is_top": 1,
    },
    {
        "title": "走进吴哥窟：被丛林吞没的古城",
        "plate_type": 2, "category_name": "人文古迹",
        "cover_img": "/static/uploads/wonder_temple.jpg",
        "intro": "高棉文明的巅峰遗迹。",
        "content": "<p>吴哥窟是柬埔寨国宝，世界上最大的宗教建筑群，见证了高棉帝国的辉煌与沧桑。</p>",
    },
    {
        "title": "迪拜哈利法塔：人类高度的新标尺",
        "plate_type": 2, "category_name": "现代地标",
        "cover_img": "/static/uploads/wonder_skyscraper.jpg",
        "intro": "828 米的沙漠奇迹。",
        "content": "<p>哈利法塔是目前世界第一高楼，融合了尖端工程与伊斯兰建筑美学。</p>",
    },
    {
        "title": "冰岛小众秘境：钻石冰沙滩",
        "plate_type": 2, "category_name": "小众秘境",
        "cover_img": "/static/uploads/wonder_iceland.jpg",
        "intro": "黑沙之上散落着晶莹冰块。",
        "content": "<p>杰古沙龙冰河湖入海口，冰块被海浪冲上黑沙海滩，宛如散落的钻石。</p>",
    },
]


def init_db():
    # 1. 建表
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # 2. 默认管理员
        if db.query(Admin).count() == 0:
            db.add(Admin(
                username=DEFAULT_ADMIN["username"],
                password=hash_password(DEFAULT_ADMIN["password"]),
            ))

        # 3. 默认分类
        cat_map = {}
        if db.query(Category).count() == 0:
            for c in CATEGORIES:
                obj = Category(**c)
                db.add(obj)
                db.flush()
                cat_map[(c["plate_type"], c["category_name"])] = obj.id

        # 4. 站点配置
        if db.query(SiteConfig).count() == 0:
            db.add(SiteConfig())

        # 5. 示例文章
        if db.query(Article).count() == 0:
            # 构建分类名 -> id 映射
            for c in db.query(Category).all():
                cat_map[(c.plate_type, c.category_name)] = c.id
            for a in SAMPLE_ARTICLES:
                cid = cat_map.get((a["plate_type"], a["category_name"]))
                db.add(Article(
                    title=a["title"],
                    intro=a.get("intro", ""),
                    content=a.get("content", ""),
                    cover_img=a.get("cover_img", ""),
                    plate_type=a["plate_type"],
                    category_id=cid,
                    is_top=a.get("is_top", 0),
                    status=1,
                    view_count=0,
                ))
            db.commit()

        # 6. 示例轮播（取两篇置顶文章）
        if db.query(Banner).count() == 0:
            tops = db.query(Article).filter(Article.is_top == 1).limit(2).all()
            for i, art in enumerate(tops):
                db.add(Banner(
                    banner_img=art.cover_img or "/static/uploads/default_cover.jpg",
                    article_id=art.id,
                    sort=i + 1,
                    status=1,
                ))
            db.commit()

        db.commit()
    finally:
        db.close()
