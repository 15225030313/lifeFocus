<template>
  <div class="search-page page-wrap rise-in">
    <header class="page-head">
      <span class="head-sub">SEARCH</span>
      <h1 class="head-title">
        “{{ keyword }}”
        <span class="count">共 {{ total }} 条结果</span>
      </h1>
    </header>

    <div v-if="articles.length" class="card-grid">
      <ArticleCard v-for="a in articles" :key="a.id" :article="a" />
    </div>
    <EmptyState v-else text="没有找到相关文章，换个关键词试试">
      <el-button type="primary" round @click="$router.push('/')">返回首页</el-button>
    </EmptyState>

    <el-pagination
      v-if="total > pageSize"
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
  window.scrollTo({ top: 0, behavior: 'smooth' })
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
.search-page {
  padding-top: 48px;
  padding-bottom: 24px;
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
  font-size: 28px;
  font-weight: 800;
  margin: 12px 0 0;
}
.count {
  font-size: 14px;
  font-weight: 400;
  color: var(--ink-3);
  margin-left: 10px;
}
.card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}
@media (max-width: 992px) {
  .card-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 640px) {
  .card-grid {
    grid-template-columns: 1fr;
  }
}
.pager {
  justify-content: center;
  margin-top: 40px;
  display: flex;
}
</style>
