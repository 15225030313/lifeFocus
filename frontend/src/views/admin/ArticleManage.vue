<template>
  <div>
    <div class="toolbar">
      <el-button type="primary" @click="openCreate"><el-icon><Plus /></el-icon>新增文章</el-button>
      <el-button type="danger" :disabled="!selected.length" @click="batchDel">
        批量删除（{{ selected.length }}）
      </el-button>
      <div class="filters">
        <el-select v-model="filterPlate" placeholder="板块" clearable style="width: 140px" @change="load">
          <el-option :value="1" label="生活小妙招" />
          <el-option :value="2" label="世界奇观" />
        </el-select>
        <el-input
          v-model="filterKeyword"
          placeholder="标题关键词"
          style="width: 180px"
          clearable
          @keyup.enter="load"
        />
        <el-button @click="load">查询</el-button>
      </div>
    </div>

    <el-table :data="list" border @selection-change="onSelect" v-loading="loading">
      <el-table-column type="selection" width="50" />
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column label="封面" width="90">
        <template #default="{ row }">
          <img :src="imgUrl(row.cover_img) || ph" class="tb-cover" @error="(e: any) => (e.target.src = ph)" />

        </template>
      </el-table-column>
      <el-table-column prop="title" label="标题" show-overflow-tooltip />
      <el-table-column label="板块" width="110">
        <template #default="{ row }">
          <el-tag size="small" :type="row.plate_type === 1 ? 'warning' : 'primary'">
            {{ row.plate_type === 1 ? '生活妙招' : '世界奇观' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="view_count" label="浏览" width="80" />
      <el-table-column label="状态" width="90">
        <template #default="{ row }">
          <el-tag size="small" :type="row.status === 1 ? 'success' : 'info'">
            {{ row.status === 1 ? '已发布' : '草稿' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="160">
        <template #default="{ row }">
          <el-button text type="primary" @click="openEdit(row)">编辑</el-button>
          <el-button text type="danger" @click="del(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      class="pager"
      background
      layout="total, prev, pager, next"
      :total="total"
      :page-size="pageSize"
      :current-page="page"
      @current-change="(p: number) => { page = p; load() }"
    />

    <el-drawer v-model="drawer" :title="form.id ? '编辑文章' : '新增文章'" size="720px">
      <el-form :model="form" label-width="90px">
        <el-form-item label="所属板块">
          <el-radio-group v-model="form.plate_type">
            <el-radio :label="1">生活小妙招</el-radio>
            <el-radio :label="2">世界奇观</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="form.category_id" placeholder="选择分类" style="width: 100%">
            <el-option v-for="c in categories" :key="c.id" :value="c.id" :label="c.category_name" />
          </el-select>
        </el-form-item>
        <el-form-item label="标题"><el-input v-model="form.title" /></el-form-item>
        <el-form-item label="封面图">
          <el-upload :show-file-list="false" :auto-upload="false" :on-change="onCover" accept="image/*">
            <img v-if="coverPreview" :src="coverPreview" class="cover-prev" />
            <el-button v-else>选择封面</el-button>
          </el-upload>
        </el-form-item>
        <el-form-item label="简介">
          <el-input v-model="form.intro" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="正文">
          <RichEditor v-model="form.content" />
        </el-form-item>
        <el-form-item label="置顶/状态">
          <el-switch v-model="form.is_top" :active-value="1" :inactive-value="0" active-text="置顶" />
          <el-switch
            v-model="form.status"
            :active-value="1"
            :inactive-value="0"
            active-text="发布"
            inactive-text="草稿"
            style="margin-left: 20px"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="drawer = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="save">保存</el-button>
      </template>
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getAdminArticles,
  createArticle,
  updateArticle,
  deleteArticle,
  batchDeleteArticles,
  getAdminCategories,
  uploadImage,
} from '@/api'
import { imgUrl, API_BASE } from '@/utils/request'
import RichEditor from '@/components/RichEditor.vue'

const list = ref<any[]>([])
const loading = ref(false)
const total = ref(0)
const page = ref(1)
const pageSize = 10
const filterPlate = ref<number | undefined>()
const filterKeyword = ref('')
const selected = ref<any[]>([])
const categories = ref<any[]>([])
const drawer = ref(false)
const saving = ref(false)
const ph = '/static/uploads/default_cover.jpg'
const coverPreview = ref('')
const form = ref<any>({
  id: 0,
  plate_type: 1,
  category_id: undefined,
  title: '',
  intro: '',
  content: '',
  cover_img: '',
  is_top: 0,
  status: 1,
})

async function load() {
  loading.value = true
  try {
    const r: any = await getAdminArticles({
      plate_type: filterPlate.value,
      keyword: filterKeyword.value,
      page: page.value,
      page_size: pageSize,
    })
    list.value = r.data || []
    total.value = r.total || 0
  } finally {
    loading.value = false
  }
}
function onSelect(rows: any[]) {
  selected.value = rows
}
async function onCover(file: any) {
  try {
    const res: any = await uploadImage(file.raw)
    form.value.cover_img = res.data.url
    coverPreview.value = API_BASE + res.data.url
  } catch {
    ElMessage.error('封面上传失败')
  }
}
function openCreate() {
  form.value = {
    id: 0,
    plate_type: 1,
    category_id: undefined,
    title: '',
    intro: '',
    content: '',
    cover_img: '',
    is_top: 0,
    status: 1,
  }
  coverPreview.value = ''
  drawer.value = true
}
function openEdit(row: any) {
  form.value = { ...row }
  coverPreview.value = row.cover_img ? API_BASE + row.cover_img : ''
  drawer.value = true
}
async function save() {
  if (!form.value.title) {
    ElMessage.warning('请填写标题')
    return
  }
  saving.value = true
  try {
    if (form.value.id) await updateArticle(form.value.id, form.value)
    else await createArticle(form.value)
    ElMessage.success('保存成功')
    drawer.value = false
    load()
  } finally {
    saving.value = false
  }
}
function del(row: any) {
  ElMessageBox.confirm(`确定删除《${row.title}》？`, '提示').then(async () => {
    await deleteArticle(row.id)
    ElMessage.success('已删除')
    load()
  }).catch(() => {})
}
function batchDel() {
  ElMessageBox.confirm(`确定删除选中的 ${selected.value.length} 篇文章？`, '提示').then(async () => {
    await batchDeleteArticles(selected.value.map((s) => s.id))
    ElMessage.success('已删除')
    load()
  }).catch(() => {})
}
onMounted(async () => {
  categories.value = (await getAdminCategories()).data || []
  load()
})
</script>

<style scoped>
.toolbar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}
.filters {
  margin-left: auto;
  display: flex;
  gap: 8px;
}
.tb-cover {
  width: 60px;
  height: 38px;
  object-fit: cover;
  border-radius: 4px;
}
.cover-prev {
  width: 160px;
  height: 90px;
  object-fit: cover;
  border-radius: 6px;
  display: block;
}
.pager {
  justify-content: center;
  margin-top: 20px;
  display: flex;
}
</style>
