<template>
  <div class="list-page">
    <div class="filter-bar">
      <div class="cats">
        <span class="label">分类：</span>
        <el-tag type="info" effect="plain" class="cat-tag" :class="{ active: catId === 0 }" @click="onCat(0)">全部</el-tag>
        <el-tag
          v-for="c in categories"
          :key="c.id"
          :type="catId === c.id ? 'primary' : 'info'"
          effect="plain"
          class="cat-tag"
          @click="onCat(c.id)"
        >
          {{ c.category_name }}
        </el-tag>
      </div>
      <div class="sort">
        <span class="label">排序：</span>
        <el-radio-group v-model="sort" @change="load">
          <el-radio-button label="latest">最新</el-radio-button>
          <el-radio-button label="hot">热门</el-radio-button>
        </el-radio-group>
      </div>
    </div>

    <div class="card-grid" v-if="articles.length">
      <ArticleCard v-for="a in articles" :key="a.id" :article="a" />
    </div>
    <EmptyState v-else text="暂无文章" />

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

function onCat(id: number) {
  catId.value = id
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
.filter-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 16px 32px;
  align-items: center;
  justify-content: center;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px 20px;
  margin-bottom: 24px;
}
.label {
  color: var(--text-3);
  font-size: 14px;
  margin-right: 4px;
}
.cats {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}
.cat-tag {
  cursor: pointer;
}
.cat-tag.active {
  color: var(--primary);
  border-color: var(--primary);
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
