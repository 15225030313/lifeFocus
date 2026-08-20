<template>
  <div class="list-page page-wrap rise-in">
    <!-- 页头 -->
    <header class="page-head">
      <span class="head-sub">{{ plateInfo.sub }}</span>
      <h1 class="head-title">{{ plateInfo.name }}</h1>
      <p class="head-desc">{{ plateInfo.desc }}</p>
    </header>

    <!-- 筛选条：分类 + 排序，整体居中 -->
    <div class="filter-bar">
      <div class="cats">
        <button class="cat-pill" :class="{ on: catId === 0 }" @click="onCat(0)">全部</button>
        <button
          v-for="c in categories"
          :key="c.id"
          class="cat-pill"
          :class="{ on: catId === c.id }"
          @click="onCat(c.id)"
        >
          {{ c.category_name }}
        </button>
      </div>
      <div class="sort">
        <button class="sort-btn" :class="{ on: sort === 'latest' }" @click="onSort('latest')">
          最新发布
        </button>
        <span class="sort-sep"></span>
        <button class="sort-btn" :class="{ on: sort === 'hot' }" @click="onSort('hot')">
          热门浏览
        </button>
      </div>
    </div>

    <!-- 文章网格 -->
    <div v-if="articles.length" class="card-grid">
      <ArticleCard v-for="a in articles" :key="a.id" :article="a" />
    </div>
    <EmptyState v-else text="该分类下暂无文章" />

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
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import ArticleCard from '@/components/ArticleCard.vue'
import EmptyState from '@/components/EmptyState.vue'
import { getArticles, getCategories } from '@/api'

const route = useRoute()
const plate = ref(Number(route.params.plate) || 1)
const categories = ref<any[]>([])
const catId = ref(0)
const sort = ref('latest')
const articles = ref<any[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = 12

const plateInfo = computed(() =>
  plate.value === 1
    ? { name: '生活小妙招', sub: 'LIFE HACKS', desc: '居家收纳、清洁技巧、美食妙招与生活应急，让日常更从容。' }
    : { name: '世界奇观', sub: 'WONDERS OF THE WORLD', desc: '自然奇观、人文古迹、现代地标与小众秘境，看见更大的世界。' }
)

function onCat(id: number) {
  catId.value = id
  page.value = 1
  load()
}
function onSort(s: string) {
  if (sort.value === s) return
  sort.value = s
  page.value = 1
  load()
}
async function load() {
  const r: any = await getArticles({
    plate_type: plate.value,
    category_id: catId.value || undefined,
    sort: sort.value,
    page: page.value,
    page_size: pageSize,
  })
  articles.value = r.data || []
  total.value = r.total || 0
}
function onPage(p: number) {
  page.value = p
  load()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
watch(
  () => route.params.plate,
  async (v) => {
    plate.value = Number(v) || 1
    catId.value = 0
    page.value = 1
    const c: any = await getCategories(plate.value)
    categories.value = c.data || []
    load()
  }
)
onMounted(async () => {
  const c: any = await getCategories(plate.value)
  categories.value = c.data || []
  load()
})
</script>

<style scoped>
.list-page {
  padding-top: 48px;
  padding-bottom: 24px;
}

/* 页头 */
.page-head {
  text-align: center;
  margin-bottom: 36px;
}
.head-sub {
  font-size: 12px;
  color: var(--primary);
  letter-spacing: 4px;
  text-transform: uppercase;
  font-weight: 700;
}
.head-title {
  font-size: 34px;
  font-weight: 800;
  letter-spacing: 2px;
  margin: 10px 0 12px;
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
.head-desc {
  color: var(--ink-3);
  font-size: 14.5px;
  margin: 14px 0 0;
}

/* 筛选条 */
.filter-bar {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  margin-bottom: 40px;
}
.cats {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
}
.cat-pill {
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--ink-2);
  font-size: 13.5px;
  padding: 7px 18px;
  border-radius: 999px;
  cursor: pointer;
  transition: all 0.22s var(--ease);
  font-family: inherit;
}
.cat-pill:hover {
  border-color: var(--primary);
  color: var(--primary-deep);
}
.cat-pill.on {
  background: var(--primary);
  border-color: var(--primary);
  color: #fff;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(15, 155, 142, 0.28);
}
.sort {
  display: flex;
  align-items: center;
  gap: 14px;
}
.sort-btn {
  border: none;
  background: none;
  font-size: 13px;
  color: var(--ink-3);
  cursor: pointer;
  padding: 4px 2px;
  font-family: inherit;
  border-bottom: 2px solid transparent;
  transition: color 0.2s, border-color 0.2s;
}
.sort-btn:hover {
  color: var(--ink);
}
.sort-btn.on {
  color: var(--primary-deep);
  font-weight: 600;
  border-bottom-color: var(--primary);
}
.sort-sep {
  width: 1px;
  height: 12px;
  background: var(--border);
}

/* 网格 */
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
