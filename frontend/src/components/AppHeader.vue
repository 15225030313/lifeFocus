<template>
  <header class="app-header" :class="{ scrolled }">
    <div class="inner">
      <router-link to="/" class="logo">
        <span class="logo-mark" style="position: relative; top: 5px">
          <svg viewBox="0 0 32 32" width="26" height="26" fill="none">
            <circle cx="16" cy="16" r="14" stroke="currentColor" stroke-width="2" />
            <path d="M10 17c2-5 10-5 12 0-2 5-10 5-12 0Z" fill="currentColor" opacity=".9" />
            <circle cx="16" cy="16" r="2.4" fill="#fff" />
          </svg>
        </span>
        <span class="logo-text">{{ siteStore.siteName }}</span>
      </router-link>

      <nav class="nav">
        <router-link to="/" exact-active-class="active">首页</router-link>
        <router-link to="/list/1" active-class="active">生活小妙招</router-link>
        <router-link to="/list/2" active-class="active">世界奇观</router-link>
        <router-link to="/about" active-class="active">关于本站</router-link>
      </nav>

      <div class="search" :class="{ open: searchOpen }">
        <button class="search-toggle" aria-label="搜索" @click="toggleSearch">
          <el-icon :size="17"><Search /></el-icon>
        </button>
        <transition name="expand">
          <div v-if="searchOpen" class="search-box">
            <input
              ref="inputRef"
              v-model="keyword"
              class="search-input"
              placeholder="搜索文章、技巧、奇观…"
              @keyup.enter="doSearch"
              @blur="onBlur"
            />
          </div>
        </transition>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useSiteStore } from '@/store/site'

const router = useRouter()
const siteStore = useSiteStore()
const keyword = ref('')
const searchOpen = ref(false)
const scrolled = ref(false)
const inputRef = ref<HTMLInputElement>()

function toggleSearch() {
  searchOpen.value = !searchOpen.value
  if (searchOpen.value) nextTick(() => inputRef.value?.focus())
}
function onBlur() {
  if (!keyword.value.trim()) searchOpen.value = false
}
function doSearch() {
  const q = keyword.value.trim()
  if (!q) return
  router.push({ path: '/search', query: { q } })
  keyword.value = ''
  searchOpen.value = false
}
function onScroll() {
  scrolled.value = window.scrollY > 24
}
onMounted(() => window.addEventListener('scroll', onScroll, { passive: true }))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<style scoped>
.app-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(247, 245, 240, 0.82);
  backdrop-filter: saturate(160%) blur(14px);
  -webkit-backdrop-filter: saturate(160%) blur(14px);
  border-bottom: 1px solid transparent;
  transition: border-color 0.3s var(--ease), background 0.3s var(--ease);
}
.app-header.scrolled {
  border-bottom-color: var(--border);
  background: rgba(247, 245, 240, 0.94);
}
.inner {
  max-width: 1200px;
  margin: 0 auto;
  height: 68px;
  display: flex;
  align-items: center;
  gap: 36px;
  padding: 0 32px;
}
.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--primary);
  flex-shrink: 0;
}
.logo-text {
  color: var(--ink);
  font-weight: 800;
  font-size: 19px;
  letter-spacing: 0.5px;
}
.nav {
  display: flex;
  gap: 6px;
  flex: 1;
}
.nav a {
  position: relative;
  color: var(--ink-2);
  font-size: 15px;
  font-weight: 500;
  padding: 6px 14px;
  border-radius: 999px;
  transition: color 0.2s, background 0.2s;
}
.nav a:hover {
  color: var(--ink);
  background: rgba(15, 155, 142, 0.08);
}
.nav a.active {
  color: var(--primary-deep);
  background: var(--primary-soft);
  font-weight: 600;
}
.search {
  display: flex;
  align-items: center;
}
.search-toggle {
  width: 38px;
  height: 38px;
  border: none;
  border-radius: 50%;
  background: transparent;
  color: var(--ink-2);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s, color 0.2s;
}
.search-toggle:hover {
  background: rgba(15, 155, 142, 0.1);
  color: var(--primary-deep);
}
.search.open .search-toggle {
  color: var(--primary-deep);
}
.search-box {
  overflow: hidden;
}
.search-input {
  width: 220px;
  height: 38px;
  border: 1px solid var(--border);
  border-radius: 999px;
  padding: 0 16px;
  font-size: 14px;
  outline: none;
  background: #fff;
  color: var(--ink);
  transition: border-color 0.2s, box-shadow 0.2s;
}
.search-input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(15, 155, 142, 0.12);
}
.expand-enter-active,
.expand-leave-active {
  transition: all 0.28s var(--ease);
  max-width: 240px;
}
.expand-enter-from,
.expand-leave-to {
  max-width: 0;
  opacity: 0;
}
@media (max-width: 768px) {
  .inner {
    gap: 12px;
    padding: 0 16px;
  }
  .nav a {
    padding: 6px 8px;
    font-size: 14px;
  }
  .search-input {
    width: 150px;
  }
}
</style>
