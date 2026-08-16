import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSiteStore = defineStore('site', () => {
  const siteName = ref('生活奇观资讯站')
  const copyright = ref('© 2026 生活奇观资讯展示网站')
  const banners = ref<any[]>([])

  function setSite(name: string, cr: string) {
    siteName.value = name
    copyright.value = cr
  }
  function setBanners(b: any[]) {
    banners.value = b
  }
  return { siteName, copyright, banners, setSite, setBanners }
})
