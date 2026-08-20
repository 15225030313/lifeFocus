<template>
  <div class="home">
    <!-- Hero 轮播 -->
    <section class="hero page-wrap rise-in">
      <el-carousel
        v-if="slides.length"
        height="480px"
        class="hero-carousel"
        :interval="6000"
        indicator-position="none"
        arrow="hover"
      >
        <el-carousel-item v-for="s in slides" :key="s.id">
          <div class="hero-item" @click="goArticle(s.article_id)">
            <img class="hero-img" :src="s.img" :alt="s.title" @error="onImgErr($event)" />
            <div class="hero-mask"></div>
            <div class="hero-text">
              <span class="hero-tag" :style="{ background: s.color }">{{ s.plateName }}</span>
              <h1 class="hero-title">{{ s.title }}</h1>
              <p class="hero-intro">{{ s.intro }}</p>
              <span class="hero-btn">
                阅读全文
                <el-icon :size="14"><Right /></el-icon>
              </span>
            </div>
          </div>
        </el-carousel-item>
      </el-carousel>
      <div v-if="slides.length" class="hero-dots">
        <span
          v-for="(s, i) in slides"
          :key="s.id"
          class="dot"
          :class="{ on: i === activeSlide }"
        ></span>
      </div>
    </section>

    <!-- 品牌理念 -->
    <section class="promise page-wrap rise-in">
      <div class="promise-item">
        <div class="promise-icon">
          <el-icon :size="22"><Collection /></el-icon>
        </div>
        <div>
          <h4>严选内容</h4>
          <p>每一篇都经过筛选，只留实用与美</p>
        </div>
      </div>
      <div class="promise-item">
        <div class="promise-icon">
          <el-icon :size="22"><Sunny /></el-icon>
        </div>
        <div>
          <h4>轻松易懂</h4>
          <p>图文并茂，三分钟读完一个小技巧</p>
        </div>
      </div>
      <div class="promise-item">
        <div class="promise-icon">
          <el-icon :size="22"><Compass /></el-icon>
        </div>
        <div>
          <h4>开阔眼界</h4>
          <p>从厨房角落到世界尽头，皆有可观</p>
        </div>
      </div>
    </section>

    <!-- 板块分区 -->
    <section
      v-for="(p, idx) in plates"
      :key="p.type"
      class="plate-section page-wrap rise-in"
    >
      <div class="section-head">
        <div class="head-left">
          <span class="num" :style="{ color: p.color }">0{{ idx + 1 }}</span>
          <div>
            <h2 class="section-title">{{ p.name }}</h2>
            <span class="section-sub">{{ p.sub }}</span>
          </div>
        </div>
        <router-link :to="`/list/${p.type}`" class="more">
          查看全部
          <el-icon :size="13"><ArrowRight /></el-icon>
        </router-link>
      </div>

      <div v-if="p.articles.length" class="plate-grid">
        <!-- 首篇大卡 -->
        <router-link :to="`/article/${p.articles[0].id}`" class="feature-card">
          <div class="feature-cover">
            <img :src="coverOf(p.articles[0])" :alt="p.articles[0].title" loading="lazy" @error="onImgErr($event)" />
          </div>
          <div class="feature-body">
            <span class="feature-cat" :style="{ color: p.color }">{{ p.articles[0].category_name || p.name }}</span>
            <h3 class="feature-title">{{ p.articles[0].title }}</h3>
            <p class="feature-intro">{{ p.articles[0].intro }}</p>
            <div class="feature-meta">
              <span>{{ fmtDate(p.articles[0].create_time) }}</span>
              <span class="read-more">继续阅读 →</span>
            </div>
          </div>
        </router-link>
        <!-- 其余小卡 -->
        <div class="side-cards">
          <ArticleCard v-for="a in p.articles.slice(1, 4)" :key="a.id" :article="a" />
        </div>
      </div>
      <EmptyState v-else text="暂无内容，敬请期待" />
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ArticleCard from '@/components/ArticleCard.vue'
import EmptyState from '@/components/EmptyState.vue'
import { getBanners, getArticles, getArticle } from '@/api'
import { imgUrl } from '@/utils/request'
import { useSiteStore } from '@/store/site'

const router = useRouter()
const siteStore = useSiteStore()
const activeSlide = ref(0)
const fallback = '/static/uploads/default_cover.jpg'

interface Slide {
  id: number
  article_id?: number
  img: string
  title: string
  intro: string
  plateName: string
  color: string
}
const slides = ref<Slide[]>([])

const plates = ref([
  { type: 1, name: '生活小妙招', sub: 'LIFE HACKS', color: 'var(--orange)', articles: [] as any[] },
  { type: 2, name: '世界奇观', sub: 'WONDERS OF THE WORLD', color: 'var(--blue)', articles: [] as any[] },
])

function coverOf(a: any) {
  return imgUrl(a.cover_img) || fallback
}
function onImgErr(e: any) {
  e.target.src = fallback
}
function fmtDate(t?: string) {
  return t ? String(t).slice(0, 10) : ''
}
function goArticle(id?: number) {
  if (id) router.push(`/article/${id}`)
}

onMounted(async () => {
  // 轮播：拉取 banner，并补充对应文章的标题/简介
  try {
    const b: any = await getBanners()
    const list = b.data || []
    if (list.length) siteStore.setBanners(list)
    const enriched = await Promise.all(
      list.map(async (item: any) => {
        let title = '精彩内容'
        let intro = ''
        let plateName = '精选'
        let color = 'var(--primary)'
        if (item.article_id) {
          try {
            const a: any = await getArticle(item.article_id)
            if (a.data) {
              title = a.data.title
              intro = a.data.intro || ''
              plateName = a.data.plate_type === 1 ? '生活小妙招' : '世界奇观'
              color = a.data.plate_type === 1 ? 'var(--orange)' : 'var(--blue)'
            }
          } catch {}
        }
        return {
          id: item.id,
          article_id: item.article_id,
          img: imgUrl(item.banner_img) || fallback,
          title,
          intro,
          plateName,
          color,
        }
      })
    )
    slides.value = enriched
  } catch {}

  // 板块文章
  for (const p of plates.value) {
    try {
      const r: any = await getArticles({ plate_type: p.type, sort: 'latest', page: 1, page_size: 4 })
      p.articles = r.data || []
    } catch {}
  }
})
</script>

<style scoped>
.home {
  padding-top: 28px;
}

/* ---------- Hero ---------- */
.hero {
  position: relative;
}
.hero-carousel {
  border-radius: var(--radius-l);
  overflow: hidden;
  box-shadow: var(--shadow-md);
}
.hero-item {
  position: relative;
  width: 100%;
  height: 100%;
  cursor: pointer;
}
.hero-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.hero-mask {
  position: absolute;
  inset: 0;
  background: linear-gradient(100deg, rgba(16, 18, 20, 0.72) 0%, rgba(16, 18, 20, 0.35) 52%, transparent 78%);
}
.hero-text {
  position: absolute;
  left: 56px;
  bottom: 64px;
  max-width: 560px;
  color: #fff;
}
.hero-tag {
  display: inline-block;
  font-size: 12.5px;
  font-weight: 600;
  letter-spacing: 1.5px;
  padding: 5px 14px;
  border-radius: 999px;
  margin-bottom: 18px;
}
.hero-title {
  font-size: 34px;
  font-weight: 800;
  line-height: 1.3;
  letter-spacing: 0.5px;
  margin: 0 0 14px;
  text-shadow: 0 2px 16px rgba(0, 0, 0, 0.3);
}
.hero-intro {
  font-size: 15px;
  line-height: 1.75;
  opacity: 0.88;
  margin: 0 0 24px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.hero-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #fff;
  color: var(--ink);
  font-size: 14px;
  font-weight: 600;
  padding: 10px 22px;
  border-radius: 999px;
  transition: gap 0.25s var(--ease), background 0.25s;
}
.hero-item:hover .hero-btn {
  gap: 10px;
  background: var(--primary);
  color: #fff;
}
.hero-dots {
  position: absolute;
  right: 36px;
  bottom: 26px;
  display: flex;
  gap: 8px;
  z-index: 5;
}
.dot {
  width: 22px;
  height: 3px;
  border-radius: 2px;
  background: rgba(255, 255, 255, 0.4);
  transition: background 0.3s, width 0.3s;
}
.dot.on {
  background: #fff;
  width: 34px;
}
:deep(.el-carousel__arrow) {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(6px);
}
:deep(.el-carousel__arrow:hover) {
  background: rgba(255, 255, 255, 0.4);
}

/* ---------- 品牌理念 ---------- */
.promise {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-top: 40px;
}
.promise-item {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  background: var(--surface);
  border-radius: var(--radius-m);
  padding: 22px 24px;
  box-shadow: var(--shadow-sm);
}
.promise-icon {
  width: 46px;
  height: 46px;
  border-radius: 12px;
  background: var(--primary-soft);
  color: var(--primary-deep);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.promise-item h4 {
  margin: 2px 0 4px;
  font-size: 15.5px;
  font-weight: 700;
}
.promise-item p {
  margin: 0;
  font-size: 13px;
  color: var(--ink-3);
  line-height: 1.6;
}

/* ---------- 板块 ---------- */
.plate-section {
  margin-top: 72px;
}
.section-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 26px;
}
.head-left {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}
.num {
  font-family: Georgia, serif;
  font-size: 44px;
  font-weight: 700;
  line-height: 1;
  opacity: 0.32;
  font-style: italic;
}
.section-title {
  font-size: 27px;
  font-weight: 800;
  letter-spacing: 1px;
  margin: 0;
  line-height: 1.2;
}
.section-sub {
  font-size: 11.5px;
  color: var(--ink-3);
  letter-spacing: 3px;
  text-transform: uppercase;
}
.more {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: var(--ink-2);
  font-size: 14px;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: var(--surface);
  transition: all 0.25s var(--ease);
}
.more:hover {
  color: #fff;
  background: var(--primary);
  border-color: var(--primary);
  gap: 9px;
}

.plate-grid {
  display: grid;
  grid-template-columns: 1.15fr 1fr;
  gap: 24px;
}
.side-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}
.side-cards .article-card:first-child {
  grid-column: 1 / -1;
}

/* 大卡 */
.feature-card {
  display: flex;
  flex-direction: column;
  background: var(--surface);
  border-radius: var(--radius-m);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: transform 0.35s var(--ease), box-shadow 0.35s var(--ease);
  color: inherit;
}
.feature-card:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-md);
}
.feature-cover {
  aspect-ratio: 16 / 8.5;
  overflow: hidden;
  background: #eceae3;
}
.feature-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s var(--ease);
}
.feature-card:hover .feature-cover img {
  transform: scale(1.05);
}
.feature-body {
  padding: 24px 28px 22px;
}
.feature-cat {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
}
.feature-title {
  font-size: 21px;
  font-weight: 800;
  line-height: 1.4;
  margin: 8px 0 10px;
}
.feature-intro {
  font-size: 14px;
  color: var(--ink-2);
  line-height: 1.75;
  margin: 0 0 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.feature-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12.5px;
  color: var(--ink-3);
}
.read-more {
  color: var(--primary);
  font-weight: 600;
}

@media (max-width: 992px) {
  .plate-grid {
    grid-template-columns: 1fr;
  }
  .hero-title {
    font-size: 26px;
  }
  .hero-text {
    left: 32px;
    bottom: 40px;
    right: 32px;
  }
  .promise {
    grid-template-columns: 1fr;
  }
}
</style>
