<template>
  <div class="about">
    <h1>关于本站</h1>
    <p>
      {{ siteStore.siteName }} 是一个轻量化资讯展示网站，专注于分享
      <strong>生活小妙招</strong> 与 <strong>世界奇观</strong> 两类优质内容。
    </p>
    <ul>
      <li>生活小妙招：居家收纳、清洁技巧、美食妙招、生活应急、护肤穿搭等实用技巧。</li>
      <li>世界奇观：自然奇观、人文古迹、现代地标、小众秘境等地标与科普。</li>
    </ul>
    <p>本站内容仅供学习与分享使用。</p>
  </div>
</template>

<script setup lang="ts">
import { useSiteStore } from '@/store/site'
const siteStore = useSiteStore()
</script>

<style scoped>
.about {
  max-width: 760px;
  margin: 0 auto;
  line-height: 1.9;
}
.about h1 {
  font-size: 26px;
  margin-bottom: 16px;
}
.about p,
.about li {
  color: var(--text-2);
}
</style>
