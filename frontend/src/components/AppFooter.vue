<template>
  <footer class="app-footer">
    <div class="inner">
      <div class="brand">
        <div class="brand-name">{{ siteStore.siteName }}</div>
        <p class="brand-desc">
          分享生活小妙招与世界各地奇观，<br />把实用与美，带给每一天。
        </p>
      </div>
      <div class="col">
        <h4>内容板块</h4>
        <router-link to="/list/1">生活小妙招</router-link>
        <router-link to="/list/2">世界奇观</router-link>
      </div>
      <div class="col">
        <h4>快速导航</h4>
        <router-link to="/">首页</router-link>
        <router-link to="/about">关于本站</router-link>
      </div>
    </div>
    <div class="bottom">
      <span>{{ siteStore.copyright }}</span>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { useSiteStore } from '@/store/site'
const siteStore = useSiteStore()
</script>

<style scoped>
.app-footer {
  margin-top: 96px;
  background: #181a1d;
  color: #9ea3ab;
}
.inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 56px 32px 40px;
  display: grid;
  grid-template-columns: 1.6fr 1fr 1fr;
  gap: 48px;
}
.brand-name {
  color: #fff;
  font-size: 20px;
  font-weight: 800;
  letter-spacing: 1px;
  margin-bottom: 14px;
}
.brand-desc {
  font-size: 13.5px;
  line-height: 1.9;
  color: #7d828c;
  margin: 0;
}
.col h4 {
  color: #e7e9ec;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 2px;
  margin: 4px 0 18px;
  text-transform: uppercase;
}
.col a {
  display: block;
  color: #9ea3ab;
  font-size: 14px;
  margin-bottom: 12px;
  transition: color 0.2s, transform 0.2s;
}
.col a:hover {
  color: #fff;
  transform: translateX(3px);
}
.bottom {
  border-top: 1px solid #26292e;
  padding: 18px 32px;
  text-align: center;
  font-size: 12.5px;
  color: #6b7079;
  letter-spacing: 0.5px;
}
@media (max-width: 768px) {
  .inner {
    grid-template-columns: 1fr;
    gap: 28px;
  }
}
</style>
