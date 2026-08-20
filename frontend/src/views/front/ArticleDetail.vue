<template>
  <div class="detail page-wrap rise-in" v-loading="loading">
    <template v-if="article">
      <!-- 头部 -->
      <header class="art-head">
        <nav class="breadcrumb">
          <router-link to="/">首页</router-link>
          <span class="sep">/</span>
          <router-link :to="`/list/${article.plate_type}`">{{
            article.plate_type === 1 ? '生活小妙招' : '世界奇观'
          }}</router-link>
          <span class="sep">/</span>
          <span class="cur">正文</span>
        </nav>
        <h1 class="title">{{ article.title }}</h1>
        <div class="meta">
          <span v-if="article.is_top" class="top-chip">精选</span>
          <span class="cat">{{ article.category_name }}</span>
          <span class="dot-sep">·</span>
          <span>{{ formatTime(article.create_time) }}</span>
          <span class="dot-sep">·</span>
          <span class="views">
            <el-icon :size="13"><View /></el-icon>{{ article.view_count }} 人读过
          </span>
        </div>
      </header>

      <!-- 封面 -->
      <figure v-if="cover" class="cover">
        <img :src="cover" :alt="article.title" @error="cover = ''" />
      </figure>

      <!-- 正文 -->
      <article class="content" v-html="article.content" @click="onImgClick"></article>

      <!-- 上下篇 -->
      <nav class="pager-nav">
        <router-link v-if="article.prev_id" :to="`/article/${article.prev_id}`" class="nav-item">
          <span class="nav-label">上一篇</span>
          <span class="nav-title">{{ article.prev_title }}</span>
        </router-link>
        <span v-else class="nav-item disabled">
          <span class="nav-label">上一篇</span>
          <span class="nav-title">已经是最早一篇</span>
        </span>
        <router-link v-if="article.next_id" :to="`/article/${article.next_id}`" class="nav-item right">
          <span class="nav-label">下一篇</span>
          <span class="nav-title">{{ article.next_title }}</span>
        </router-link>
        <span v-else class="nav-item right disabled">
          <span class="nav-label">下一篇</span>
          <span class="nav-title">已经是最新一篇</span>
        </span>
      </nav>
    </template>
    <EmptyState v-else-if="!loading" text="文章不存在或已下架">
      <el-button type="primary" round @click="$router.push('/')">返回首页</el-button>
    </EmptyState>

    <!-- 图片预览 -->
    <el-dialog v-model="imgVisible" width="80%" class="img-dialog" :show-close="true">
      <img :src="imgSrc" style="width: 100%; border-radius: 8px" />
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import EmptyState from '@/components/EmptyState.vue'
import { getArticle } from '@/api'
import { imgUrl } from '@/utils/request'

const route = useRoute()
const article = ref<any>(null)
const loading = ref(true)
const imgVisible = ref(false)
const imgSrc = ref('')

const cover = computed({
  get: () => (article.value ? imgUrl(article.value.cover_img) : ''),
  set: () => {},
})

function formatTime(t?: string) {
  return t ? String(t).slice(0, 10) : ''
}
function onImgClick(e: any) {
  if (e.target && e.target.tagName === 'IMG') {
    imgSrc.value = e.target.src
    imgVisible.value = true
  }
}
async function load() {
  loading.value = true
  window.scrollTo({ top: 0 })
  try {
    const r: any = await getArticle(Number(route.params.id))
    article.value = r.data || null
  } catch {
    article.value = null
  }
  loading.value = false
}
watch(() => route.params.id, load)
onMounted(load)
</script>

<style scoped>
.detail {
  max-width: 780px;
  padding-top: 44px;
}

/* 头部 */
.art-head {
  text-align: center;
  margin-bottom: 36px;
}
.breadcrumb {
  font-size: 13px;
  color: var(--ink-3);
  margin-bottom: 22px;
}
.breadcrumb a {
  color: var(--ink-3);
  transition: color 0.2s;
}
.breadcrumb a:hover {
  color: var(--primary);
}
.breadcrumb .sep {
  margin: 0 8px;
  opacity: 0.5;
}
.breadcrumb .cur {
  color: var(--ink-2);
}
.title {
  font-size: 32px;
  font-weight: 800;
  line-height: 1.4;
  letter-spacing: 0.5px;
  margin: 0 0 20px;
}
.meta {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 10px;
  color: var(--ink-3);
  font-size: 13.5px;
}
.top-chip {
  background: linear-gradient(135deg, #d9b078, var(--gold));
  color: #fff;
  font-size: 11.5px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 999px;
}
.cat {
  color: var(--primary-deep);
  background: var(--primary-soft);
  padding: 3px 12px;
  border-radius: 999px;
  font-size: 12.5px;
  font-weight: 600;
}
.dot-sep {
  opacity: 0.5;
}
.views {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

/* 封面 */
.cover {
  margin: 0 0 40px;
  border-radius: var(--radius-m);
  overflow: hidden;
  box-shadow: var(--shadow-md);
}
.cover img {
  width: 100%;
  display: block;
}

/* 正文排版 */
.content {
  font-size: 16px;
  line-height: 1.95;
  color: #2b2c30;
  letter-spacing: 0.2px;
}
.content :deep(p) {
  margin: 0 0 22px;
}
.content :deep(h1),
.content :deep(h2),
.content :deep(h3) {
  font-weight: 800;
  line-height: 1.4;
  margin: 36px 0 16px;
}
.content :deep(h2) {
  font-size: 23px;
  padding-left: 14px;
  border-left: 4px solid var(--primary);
}
.content :deep(h3) {
  font-size: 19px;
}
.content :deep(img) {
  max-width: 100%;
  border-radius: var(--radius-s);
  margin: 14px 0;
  cursor: zoom-in;
  box-shadow: var(--shadow-sm);
}
.content :deep(blockquote) {
  margin: 24px 0;
  padding: 16px 22px;
  background: var(--primary-soft);
  border-left: 4px solid var(--primary);
  border-radius: 0 var(--radius-s) var(--radius-s) 0;
  color: var(--ink-2);
}
.content :deep(ul),
.content :deep(ol) {
  padding-left: 24px;
  margin: 0 0 22px;
}
.content :deep(li) {
  margin-bottom: 8px;
}
.content :deep(strong) {
  color: var(--ink);
}
.content :deep(a) {
  color: var(--primary);
  border-bottom: 1px solid rgba(15, 155, 142, 0.35);
}

/* 上下篇 */
.pager-nav {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin: 56px 0 24px;
}
.nav-item {
  background: var(--surface);
  border-radius: var(--radius-m);
  padding: 18px 22px;
  box-shadow: var(--shadow-sm);
  transition: transform 0.25s var(--ease), box-shadow 0.25s var(--ease);
  color: inherit;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.nav-item:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}
.nav-item.right {
  text-align: right;
}
.nav-item.disabled {
  opacity: 0.45;
  pointer-events: none;
}
.nav-label {
  font-size: 12px;
  color: var(--primary);
  font-weight: 700;
  letter-spacing: 1.5px;
}
.nav-title {
  font-size: 14.5px;
  font-weight: 600;
  color: var(--ink);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
@media (max-width: 640px) {
  .title {
    font-size: 25px;
  }
  .pager-nav {
    grid-template-columns: 1fr;
  }
}
</style>
