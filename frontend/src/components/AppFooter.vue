<template>
  <footer class="app-footer">
    <div class="inner">
      <div class="col">
        <h4>{{ siteStore.siteName }}</h4>
        <p>分享生活小妙招与世界的奇观，让每一天都更有趣、更有质量。</p>
      </div>
      <div class="col">
        <h4>快速导航</h4>
        <router-link to="/">首页</router-link>
        <router-link to="/list/1">生活小妙招</router-link>
        <router-link to="/list/2">世界奇观</router-link>
      </div>
      <div class="col">
        <h4>关于</h4>
        <router-link to="/about">关于本站</router-link>
      </div>
    </div>
    <div class="copyright">{{ siteStore.copyright }}</div>
  </footer>
</template>

<script setup lang="ts">
import { useSiteStore } from '@/store/site'
const siteStore = useSiteStore()
</script>

<style scoped>
.app-footer {
  background: #1f2933;
  color: #c7cdd6;
  margin-top: 40px;
}
.inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  gap: 60px;
  padding: 32px 24px;
  flex-wrap: wrap;
}
.col h4 {
  color: #fff;
  margin: 0 0 12px;
  font-size: 15px;
}
.col p {
  font-size: 13px;
  max-width: 280px;
  line-height: 1.7;
}
.col a {
  display: block;
  color: #c7cdd6;
  font-size: 13px;
  margin-bottom: 8px;
}
.col a:hover {
  color: var(--primary);
}
.copyright {
  text-align: center;
  font-size: 12px;
  color: #8a94a6;
  padding: 14px;
  border-top: 1px solid #2d3748;
}
</style>
