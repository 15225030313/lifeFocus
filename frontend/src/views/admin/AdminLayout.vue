<template>
  <el-container class="admin-layout">
    <el-aside width="220px" class="aside">
      <div class="logo">🌿 管理后台</div>
      <el-menu :default-active="activeMenu" router class="menu">
        <el-menu-item index="/admin/dashboard"><el-icon><DataLine /></el-icon>仪表盘</el-menu-item>
        <el-menu-item index="/admin/articles"><el-icon><Document /></el-icon>文章管理</el-menu-item>
        <el-menu-item index="/admin/categories"><el-icon><Files /></el-icon>分类管理</el-menu-item>
        <el-menu-item index="/admin/system"><el-icon><Setting /></el-icon>系统管理</el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="topbar">
        <span class="crumb">当前：{{ currentTitle }}</span>
        <div class="right">
          <a href="/" target="_blank" class="view-site">查看前台</a>
          <span class="user">{{ userStore.username }}</span>
          <el-button text type="danger" @click="logout">退出</el-button>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { ElMessageBox } from 'element-plus'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const activeMenu = computed(() => route.path)
const titles: Record<string, string> = {
  '/admin/dashboard': '仪表盘',
  '/admin/articles': '文章管理',
  '/admin/categories': '分类管理',
  '/admin/system': '系统管理',
}
const currentTitle = computed(() => titles[route.path] || '管理后台')

function logout() {
  ElMessageBox.confirm('确定退出登录？', '提示')
    .then(() => {
      userStore.logout()
      router.replace('/admin/login')
    })
    .catch(() => {})
}
</script>

<style scoped>
.admin-layout {
  height: 100vh;
}
.aside {
  background: #1f2933;
}
.logo {
  height: 64px;
  display: flex;
  align-items: center;
  padding: 0 20px;
  font-weight: 700;
  font-size: 18px;
  color: #fff;
  border-bottom: 1px solid #2d3748;
}
.menu {
  border-right: none;
  background: transparent;
}
.menu :deep(.el-menu-item) {
  color: #c7cdd6;
}
.menu :deep(.el-menu-item.is-active) {
  background: var(--primary);
  color: #fff;
}
.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
  border-bottom: 1px solid var(--border);
}
.crumb {
  font-size: 15px;
  color: var(--text-2);
}
.right {
  display: flex;
  align-items: center;
  gap: 16px;
}
.view-site {
  color: var(--primary);
  text-decoration: none;
  font-size: 14px;
}
.user {
  color: var(--text-2);
  font-size: 14px;
}
</style>
