<template>
  <div class="about page-wrap rise-in">
    <header class="page-head">
      <span class="head-sub">ABOUT US</span>
      <h1 class="head-title">关于本站</h1>
    </header>

    <div class="about-body">
      <p class="lead">
        {{ siteStore.siteName }} 是一个轻量化的资讯网站，
        专注于分享 <strong>生活小妙招</strong> 与 <strong>世界奇观</strong> 两类内容——
        一半让日子过得更顺手，一半让眼界变得更辽阔。
      </p>

      <div class="plate-cards">
        <router-link to="/list/1" class="plate-card">
          <span class="plate-num">01</span>
          <h3>生活小妙招</h3>
          <p>居家收纳、清洁技巧、美食妙招、生活应急、护肤穿搭……把琐碎日常过得聪明一点。</p>
          <span class="plate-link">进入板块 →</span>
        </router-link>
        <router-link to="/list/2" class="plate-card">
          <span class="plate-num">02</span>
          <h3>世界奇观</h3>
          <p>自然奇观、人文古迹、现代地标、小众秘境……不出家门，也能看见世界的壮阔。</p>
          <span class="plate-link">进入板块 →</span>
        </router-link>
      </div>

      <p class="note">本站所有内容仅供学习与分享使用，愿你在这里每天都有一点新收获。</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useSiteStore } from '@/store/site'
const siteStore = useSiteStore()
</script>

<style scoped>
.about {
  padding-top: 48px;
  max-width: 860px;
}
.page-head {
  text-align: center;
  margin-bottom: 40px;
}
.head-sub {
  font-size: 12px;
  color: var(--primary);
  letter-spacing: 4px;
  font-weight: 700;
}
.head-title {
  font-size: 34px;
  font-weight: 800;
  letter-spacing: 2px;
  margin: 10px 0 0;
}
.head-title::after {
  content: '';
  display: block;
  width: 44px;
  height: 3px;
  border-radius: 2px;
  background: var(--primary);
  margin: 16px auto 0;
}
.about-body {
  text-align: center;
}
.lead {
  font-size: 16.5px;
  line-height: 2;
  color: var(--ink-2);
  margin: 0 auto 44px;
  max-width: 640px;
}
.lead strong {
  color: var(--primary-deep);
}
.plate-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 44px;
}
.plate-card {
  position: relative;
  background: var(--surface);
  border-radius: var(--radius-m);
  padding: 32px 28px;
  text-align: left;
  box-shadow: var(--shadow-sm);
  color: inherit;
  transition: transform 0.3s var(--ease), box-shadow 0.3s var(--ease);
  overflow: hidden;
}
.plate-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-md);
}
.plate-num {
  position: absolute;
  top: 14px;
  right: 20px;
  font-family: Georgia, serif;
  font-style: italic;
  font-size: 46px;
  font-weight: 700;
  color: var(--primary);
  opacity: 0.14;
}
.plate-card h3 {
  margin: 0 0 10px;
  font-size: 19px;
  font-weight: 800;
}
.plate-card p {
  margin: 0 0 18px;
  font-size: 14px;
  color: var(--ink-3);
  line-height: 1.8;
}
.plate-link {
  font-size: 13.5px;
  color: var(--primary);
  font-weight: 600;
}
.note {
  color: var(--ink-3);
  font-size: 13.5px;
}
@media (max-width: 640px) {
  .plate-cards {
    grid-template-columns: 1fr;
  }
}
</style>
