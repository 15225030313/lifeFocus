<template>
  <header class="app-header">
    <div class="inner">
      <router-link to="/" class="logo">
        <span class="logo-mark">🌿</span>
        <span class="logo-text">{{ siteStore.siteName }}</span>
      </router-link>
      <nav class="nav">
        <router-link to="/list/1">生活小妙招</router-link>
        <router-link to="/list/2">世界奇观</router-link>
        <router-link to="/about">关于本站</router-link>
      </nav>
      <div class="search">
        <el-input v-model="keyword" placeholder="搜索文章…" clearable @keyup.enter="doSearch">
          <template #prefix><el-icon><Search /></el-icon></template>
        </el-input>
        <el-button type="primary" @click="doSearch">搜索</el-button>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useSiteStore } from '@/store/site'

const router = useRouter()
const siteStore = useSiteStore()
const keyword = ref('')

function doSearch() {
  if (!keyword.value.trim()) return
  router.push({ path: '/search', query: { q: keyword.value.trim() } })
}
</script>

<style scoped>
.app-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: #fff;
  border-bottom: 1px solid var(--border);
}
.inner {
  max-width: 1200px;
  margin: 0 auto;
  height: 64px;
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 0 24px;
}
.logo {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--text-1);
  font-weight: 700;
  font-size: 18px;
}
.logo-mark {
  font-size: 22px;
}
.nav {
  display: flex;
  gap: 20px;
  flex: 1;
}
.nav a {
  color: var(--text-2);
  font-size: 15px;
  padding: 4px 0;
  border-bottom: 2px solid transparent;
}
.nav a.router-link-active {
  color: var(--primary);
  border-bottom-color: var(--primary);
}
.search {
  display: flex;
  gap: 8px;
}
.search .el-input {
  width: 220px;
}
</style>
