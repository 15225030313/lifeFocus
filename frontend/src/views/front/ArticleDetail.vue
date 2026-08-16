<template>
  <div class="detail" v-loading="loading">
    <template v-if="article">
      <nav class="breadcrumb">
        <router-link to="/">首页</router-link> /
        <router-link :to="`/list/${article.plate_type}`">{{
          article.plate_type === 1 ? '生活小妙招' : '世界奇观'
        }}</router-link> /
        <span>{{ article.title }}</span>
      </nav>
      <h1 class="title">
        <el-tag v-if="article.is_top" type="danger" size="small">置顶</el-tag>
        {{ article.title }}
      </h1>
      <div class="meta">
        <el-tag size="small" effect="plain">{{ article.category_name }}</el-tag>
        <span>{{ formatTime(article.create_time) }}</span>
        <span><el-icon><View /></el-icon> {{ article.view_count }} 浏览</span>
      </div>
      <div class="content" v-html="article.content" @click="onImgClick"></div>

      <div class="pager-nav">
        <router-link v-if="article.prev_id" :to="`/article/${article.prev_id}`" class="nav-item prev">
          ← {{ article.prev_title }}
        </router-link>
        <span v-else></span>
        <router-link v-if="article.next_id" :to="`/article/${article.next_id}`" class="nav-item next">
          {{ article.next_title }} →
        </router-link>
      </div>
      <div class="back">
        <el-button @click="$router.push(`/list/${article.plate_type}`)">返回列表</el-button>
      </div>
    </template>
    <EmptyState v-else-if="!loading" text="文章不存在或已下架" />

    <el-dialog v-model="imgVisible" title="图片预览" width="80%">
      <img :src="imgSrc" style="width: 100%" />
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import EmptyState from '@/components/EmptyState.vue'
import { getArticle } from '@/api'

const route = useRoute()
const article = ref<any>(null)
const loading = ref(true)
const imgVisible = ref(false)
const imgSrc = ref('')

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
  max-width: 760px;
  margin: 0 auto;
}
.breadcrumb {
  font-size: 13px;
  color: var(--text-3);
  margin-bottom: 16px;
}
.breadcrumb a {
  color: var(--text-3);
}
.title {
  font-size: 26px;
  line-height: 1.4;
  margin: 0 0 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.meta {
  display: flex;
  align-items: center;
  gap: 16px;
  color: var(--text-3);
  font-size: 13px;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border);
}
.content {
  line-height: 1.85;
  font-size: 15px;
  color: var(--text-1);
}
.content :deep(img) {
  max-width: 100%;
  border-radius: 8px;
  margin: 12px 0;
  cursor: zoom-in;
}
.content :deep(h1),
.content :deep(h2),
.content :deep(h3) {
  margin: 20px 0 10px;
}
.content :deep(p) {
  margin: 12px 0;
}
.pager-nav {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin: 32px 0 16px;
}
.nav-item {
  flex: 1;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 12px 16px;
  color: var(--text-2);
  font-size: 14px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.nav-item:hover {
  border-color: var(--primary);
  color: var(--primary);
}
.back {
  text-align: center;
}
</style>
