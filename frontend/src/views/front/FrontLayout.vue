<template>
  <div class="front-layout">
    <AppHeader />
    <main class="content">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'
import { getSite, getBanners } from '@/api'
import { useSiteStore } from '@/store/site'

const siteStore = useSiteStore()
onMounted(async () => {
  try {
    const site: any = await getSite()
    if (site.data) siteStore.setSite(site.data.site_name, site.data.copyright)
    const b: any = await getBanners()
    if (b.data) siteStore.setBanners(b.data)
  } catch {}
})
</script>

<style scoped>
.content {
  min-height: 62vh;
}
.page-enter-active {
  transition: all 0.32s var(--ease);
}
.page-leave-active {
  transition: all 0.18s ease;
}
.page-enter-from {
  opacity: 0;
  transform: translateY(14px);
}
.page-leave-to {
  opacity: 0;
}
</style>
