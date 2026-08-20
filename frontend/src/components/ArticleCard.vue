<template>
  <router-link :to="`/article/${article.id}`" class="article-card">
    <div class="cover">
      <img :src="coverSrc" :alt="article.title" loading="lazy" @error="onErr" />
      <span v-if="article.is_top" class="top-badge">
        <el-icon :size="11"><Top /></el-icon> 精选
      </span>
      <span v-if="article.category_name" class="cat-chip">{{ article.category_name }}</span>
    </div>
    <div class="body">
      <h3 class="title">{{ article.title }}</h3>
      <p class="intro">{{ article.intro || '暂无简介' }}</p>
      <div class="meta">
        <span class="date">{{ formatTime(article.create_time) }}</span>
        <span class="views">
          <el-icon :size="13"><View /></el-icon>{{ formatViews(article.view_count) }}
        </span>
      </div>
    </div>
  </router-link>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { imgUrl } from '@/utils/request'

const props = defineProps<{ article: any }>()
const placeholder = '/static/uploads/default_cover.jpg'
const coverSrc = ref(imgUrl(props.article.cover_img) || placeholder)

function onErr() {
  coverSrc.value = placeholder
}
function formatTime(t?: string) {
  return t ? String(t).slice(0, 10) : ''
}
function formatViews(v?: number) {
  const n = v || 0
  return n >= 10000 ? (n / 10000).toFixed(1) + 'w' : String(n)
}
</script>

<style scoped>
.article-card {
  display: flex;
  flex-direction: column;
  background: var(--surface);
  border-radius: var(--radius-m);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: transform 0.35s var(--ease), box-shadow 0.35s var(--ease);
  color: inherit;
}
.article-card:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-md);
}
.cover {
  position: relative;
  aspect-ratio: 16 / 10;
  overflow: hidden;
  background: #eceae3;
}
.cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s var(--ease);
}
.article-card:hover .cover img {
  transform: scale(1.06);
}
.top-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  display: inline-flex;
  align-items: center;
  gap: 3px;
  background: linear-gradient(135deg, #d9b078, var(--gold));
  color: #fff;
  font-size: 11.5px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 999px;
  letter-spacing: 0.5px;
  box-shadow: 0 2px 8px rgba(201, 162, 107, 0.4);
}
.cat-chip {
  position: absolute;
  bottom: 12px;
  left: 12px;
  background: rgba(24, 26, 29, 0.55);
  backdrop-filter: blur(8px);
  color: #fff;
  font-size: 11.5px;
  padding: 4px 10px;
  border-radius: 999px;
  letter-spacing: 0.3px;
}
.body {
  padding: 18px 20px 16px;
  display: flex;
  flex-direction: column;
  flex: 1;
}
.title {
  font-size: 17px;
  font-weight: 700;
  margin: 0 0 8px;
  line-height: 1.45;
  letter-spacing: 0.2px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  transition: color 0.2s;
}
.article-card:hover .title {
  color: var(--primary-deep);
}
.intro {
  font-size: 13.5px;
  color: var(--ink-3);
  margin: 0 0 14px;
  line-height: 1.65;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}
.meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12.5px;
  color: var(--ink-3);
  padding-top: 12px;
  border-top: 1px solid #f0ede6;
}
.views {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}
</style>
