<template>
  <div>
    <div class="toolbar">
      <el-button type="primary" @click="openCreate"><el-icon><Plus /></el-icon>新增分类</el-button>
    </div>
    <el-table :data="list" border v-loading="loading">
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="category_name" label="分类名称" />
      <el-table-column prop="category_desc" label="描述" show-overflow-tooltip />
      <el-table-column label="所属板块" width="120">
        <template #default="{ row }">
          <el-tag size="small" :type="row.plate_type === 1 ? 'warning' : 'primary'">
            {{ row.plate_type === 1 ? '生活妙招' : '世界奇观' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="sort" label="排序" width="80" />
      <el-table-column label="状态" width="90">
        <template #default="{ row }">
          <el-tag size="small" :type="row.status === 1 ? 'success' : 'info'">
            {{ row.status === 1 ? '启用' : '禁用' }}
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

    <el-dialog v-model="dialog" :title="form.id ? '编辑分类' : '新增分类'" width="480px">
      <el-form :model="form" label-width="90px">
        <el-form-item label="名称"><el-input v-model="form.category_name" /></el-form-item>
        <el-form-item label="描述"><el-input v-model="form.category_desc" /></el-form-item>
        <el-form-item label="板块">
          <el-radio-group v-model="form.plate_type">
            <el-radio :label="1">生活妙招</el-radio>
            <el-radio :label="2">世界奇观</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="排序"><el-input-number v-model="form.sort" :min="0" /></el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="form.status" :active-value="1" :inactive-value="0" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialog = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="save">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getAdminCategories, createCategory, updateCategory, deleteCategory } from '@/api'

const list = ref<any[]>([])
const loading = ref(false)
const dialog = ref(false)
const saving = ref(false)
const form = ref<any>({ id: 0, category_name: '', category_desc: '', plate_type: 1, sort: 0, status: 1 })

async function load() {
  loading.value = true
  try {
    const r: any = await getAdminCategories()
    list.value = r.data || []
  } finally {
    loading.value = false
  }
}
function openCreate() {
  form.value = { id: 0, category_name: '', category_desc: '', plate_type: 1, sort: 0, status: 1 }
  dialog.value = true
}
function openEdit(row: any) {
  form.value = { ...row }
  dialog.value = true
}
async function save() {
  if (!form.value.category_name) {
    ElMessage.warning('请填写名称')
    return
  }
  saving.value = true
  try {
    if (form.value.id) await updateCategory(form.value.id, form.value)
    else await createCategory(form.value)
    ElMessage.success('保存成功')
    dialog.value = false
    load()
  } finally {
    saving.value = false
  }
}
function del(row: any) {
  ElMessageBox.confirm(`确定删除分类《${row.category_name}》？`, '提示')
    .then(async () => {
      const r: any = await deleteCategory(row.id)
      if (r.code === 200) {
        ElMessage.success('已删除')
        load()
      }
    })
    .catch(() => {})
}
onMounted(load)
</script>

<style scoped>
.toolbar {
  margin-bottom: 16px;
}
</style>
