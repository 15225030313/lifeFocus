<template>
  <div class="home">
    <el-carousel
      v-if="banners.length"
      height="380px"
      class="banner"
      indicator-position="outside"
      :autoplay="true"
      :interval="5000"
    >
      <el-carousel-item v-for="b in banners" :key="b.id">
        <div class="banner-item" @click="goArticle(b.article_id)" :style="bgStyle(b.banner_img)">
          <span class="hint">点击查看详情 →</span>
        </div>
      </el-carousel-item>
    </el-carousel>

    <section v-for="p in plates" :key="p.type" class="plate-section">
      <div class="section-head">
        <div class="title-wrap">
          <span class="bar" :style="{ background: p.color }"></span>
          <h2 :style="{ color: p.color }">{{ p.name }}</h2>
        </div>
        <router-link :to="`/list/${p.type}`" class="more">查看更多 →</router-link>
      </div>
      <div class="card-grid">
        <ArticleCard v-for="a in p.articles" :key="a.id" :article="a" />
      </div>
      <EmptyState v-if="!p.articles.length" text="暂无内容" />
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ArticleCard from '@/components/ArticleCard.vue'
import EmptyState from '@/components/EmptyState.vue'
import { getBanners, getArticles } from '@/api'
import { imgUrl } from '@/utils/request'
import { useSiteStore } from '@/store/site'

const router = useRouter()
const siteStore = useSiteStore()
const banners = ref<any[]>(siteStore.banners)
const plates = ref([
  { type: 1, name: '生活小妙招', color: '#FF8C42', articles: [] as any[] },
  { type: 2, name: '世界奇观', color: '#3B82F6', articles: [] as any[] },
])

function bgStyle(img: string) {
  const url = imgUrl(img) || '/static/uploads/default_cover.jpg'
  return { backgroundImage: `url(${url})` }
}
function goArticle(id?: number) {
  if (id) router.push(`/article/${id}`)
}
onMounted(async () => {
  try {
    const b: any = await getBanners()
    if (b.data?.length) {
      banners.value = b.data
      siteStore.setBanners(b.data)
    }
  } catch {}
  for (const p of plates.value) {
    try {
      const r: any = await getArticles({ plate_type: p.type, sort: 'latest', page: 1, page_size: 6 })
      p.articles = r.data || []
    } catch {}
  }
})
</script>

<style scoped>
.banner {
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 32px;
}
.banner-item {
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  cursor: pointer;
  position: relative;
}
.banner-item .hint {
  position: absolute;
  bottom: 16px;
  right: 20px;
  background: rgba(0, 0, 0, 0.45);
  color: #fff;
  padding: 6px 14px;
  border-radius: 999px;
  font-size: 13px;
}
.plate-section {
  margin-bottom: 36px;
}
.section-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.title-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
}
.bar {
  width: 4px;
  height: 22px;
  border-radius: 2px;
}
.section-head h2 {
  font-size: 22px;
  margin: 0;
}
.more {
  color: var(--text-3);
  font-size: 14px;
}
.more:hover {
  color: var(--primary);
}
.card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}
@media (max-width: 992px) {
  .card-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
