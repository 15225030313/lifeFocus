<template>
  <router-link :to="`/article/${article.id}`" class="article-card">
    <div class="cover">
      <img :src="coverSrc" :alt="article.title" @error="onErr" />
      <span v-if="article.is_top" class="top-badge">置顶</span>
    </div>
    <div class="body">
      <h3 class="title">{{ article.title }}</h3>
      <p class="intro">{{ article.intro || '暂无简介' }}</p>
      <div class="meta">
        <span>{{ formatTime(article.create_time) }}</span>
        <span class="views"><el-icon><View /></el-icon> {{ article.view_count || 0 }}</span>
      </div>
    </div>
  </router-link>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { imgUrl } from '@/utils/request'

const props = defineProps<{ article: any }>()
const placeholder = '/static/uploads/default_cover.jpg'
const err = ref(false)
const coverSrc = ref(imgUrl(props.article.cover_img) || placeholder)

function onErr() {
  coverSrc.value = placeholder
}
function formatTime(t?: string) {
  return t ? String(t).slice(0, 10) : ''
}
</script>

<style scoped>
.article-card {
  display: block;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.2s;
  color: inherit;
}
.article-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  transform: translateY(-4px);
  border-color: var(--primary);
}
.cover {
  position: relative;
  aspect-ratio: 16 / 9;
  overflow: hidden;
  background: var(--primary-light);
}
.cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}
.article-card:hover .cover img {
  transform: scale(1.03);
}
.top-badge {
  position: absolute;
  top: 8px;
  left: 8px;
  background: #ef4444;
  color: #fff;
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 4px;
}
.body {
  padding: 12px 14px;
}
.title {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 8px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.intro {
  font-size: 13px;
  color: var(--text-3);
  margin: 0 0 10px;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: var(--text-3);
}
.views {
  display: flex;
  align-items: center;
  gap: 2px;
}
</style>
