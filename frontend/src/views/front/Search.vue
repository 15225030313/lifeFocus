<template>
  <div class="search-page">
    <h2 class="page-title">“{{ keyword }}” 的搜索结果（{{ total }}）</h2>
    <div class="card-grid" v-if="articles.length">
      <ArticleCard v-for="a in articles" :key="a.id" :article="a" />
    </div>
    <EmptyState v-else text="没有找到相关文章" />
    <el-pagination
      class="pager"
      background
      layout="prev, pager, next"
      :total="total"
      :page-size="pageSize"
      :current-page="page"
      @current-change="onPage"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import ArticleCard from '@/components/ArticleCard.vue'
import EmptyState from '@/components/EmptyState.vue'
import { getArticles } from '@/api'

const route = useRoute()
const keyword = ref(String(route.query.q || ''))
const articles = ref<any[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = 12

async function load() {
  const r: any = await getArticles({ keyword: keyword.value, page: page.value, page_size: pageSize })
  articles.value = r.data || []
  total.value = r.total || 0
}
function onPage(p: number) {
  page.value = p
  load()
}
watch(
  () => route.query.q,
  (v) => {
    keyword.value = String(v || '')
    page.value = 1
    load()
  }
)
onMounted(load)
</script>

<style scoped>
.page-title {
  font-size: 20px;
  margin: 0 0 20px;
}
.card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}
@media (max-width: 992px) {
  .card-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
.pager {
  justify-content: center;
  margin-top: 28px;
  display: flex;
}
</style>
