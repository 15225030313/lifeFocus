<template>
  <el-tabs v-model="tab">
    <el-tab-pane label="网站配置" name="site">
      <el-form :model="siteForm" label-width="100px" style="max-width: 480px">
        <el-form-item label="网站名称"><el-input v-model="siteForm.site_name" /></el-form-item>
        <el-form-item label="版权信息"><el-input v-model="siteForm.copyright" /></el-form-item>
        <el-button type="primary" :loading="savingSite" @click="saveSite">保存配置</el-button>
      </el-form>
    </el-tab-pane>

    <el-tab-pane label="轮播图管理" name="banner">
      <div class="toolbar">
        <el-upload :show-file-list="false" :auto-upload="false" :on-change="onBannerUpload" accept="image/*">
          <el-button type="primary"><el-icon><Plus /></el-icon>上传轮播图</el-button>
        </el-upload>
      </div>
      <el-table :data="banners" border v-loading="loadingBanner">
        <el-table-column label="图片" width="160">
          <template #default="{ row }">
            <img :src="imgUrl(row.banner_img) || ph" class="bn-img" @error="(e: any) => (e.target.src = ph)" />
          </template>
        </el-table-column>
        <el-table-column label="跳转文章" min-width="160">
          <template #default="{ row }">
            <el-select
              v-model="row.article_id"
              placeholder="不跳转"
              clearable
              style="width: 100%"
              @change="(v: any) => updBanner(row.id, { article_id: v })"
            >
              <el-option v-for="a in allArticles" :key="a.id" :value="a.id" :label="a.title.slice(0, 12)" />
            </el-select>
          </template>
        </el-table-column>
        <el-table-column label="排序" width="120">
          <template #default="{ row }">
            <el-input-number v-model="row.sort" :min="0" @change="(v: any) => updBanner(row.id, { sort: v })" />
          </template>
        </el-table-column>
        <el-table-column label="状态" width="90">
          <template #default="{ row }">
            <el-switch
              v-model="row.status"
              :active-value="1"
              :inactive-value="0"
              @change="(v: any) => updBanner(row.id, { status: v })"
            />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="80">
          <template #default="{ row }">
            <el-button text type="danger" @click="delBanner(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-tab-pane>

    <el-tab-pane label="修改密码" name="pwd">
      <el-form :model="pwdForm" label-width="100px" style="max-width: 420px">
        <el-form-item label="原密码">
          <el-input v-model="pwdForm.old_password" type="password" show-password />
        </el-form-item>
        <el-form-item label="新密码">
          <el-input v-model="pwdForm.new_password" type="password" show-password />
        </el-form-item>
        <el-button type="primary" :loading="savingPwd" @click="savePwd">修改密码</el-button>
      </el-form>
    </el-tab-pane>
  </el-tabs>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import {
  getAdminSite,
  updateSite,
  getAdminBanners,
  createBanner,
  updateBanner,
  deleteBanner,
  getAdminArticles,
  uploadImage,
  changePassword,
} from '@/api'
import { imgUrl, API_BASE } from '@/utils/request'

const tab = ref('site')
const siteForm = ref({ site_name: '', copyright: '' })
const savingSite = ref(false)
const pwdForm = ref({ old_password: '', new_password: '' })
const savingPwd = ref(false)
const banners = ref<any[]>([])
const loadingBanner = ref(false)
const allArticles = ref<any[]>([])
const ph = '/static/uploads/default_cover.jpg'

async function loadSite() {
  const r: any = await getAdminSite()
  if (r.data) siteForm.value = { site_name: r.data.site_name, copyright: r.data.copyright }
}
async function saveSite() {
  savingSite.value = true
  try {
    await updateSite(siteForm.value)
    ElMessage.success('已保存')
  } finally {
    savingSite.value = false
  }
}
async function savePwd() {
  if (!pwdForm.value.old_password || !pwdForm.value.new_password) {
    ElMessage.warning('请填写完整')
    return
  }
  savingPwd.value = true
  try {
    const r: any = await changePassword(pwdForm.value.old_password, pwdForm.value.new_password)
    if (r.code === 200) {
      ElMessage.success('密码已修改')
      pwdForm.value = { old_password: '', new_password: '' }
    }
  } finally {
    savingPwd.value = false
  }
}
async function loadBanners() {
  loadingBanner.value = true
  try {
    const r: any = await getAdminBanners()
    banners.value = r.data || []
  } finally {
    loadingBanner.value = false
  }
}
async function loadArticles() {
  const r: any = await getAdminArticles({ page: 1, page_size: 100 })
  allArticles.value = r.data || []
}
async function onBannerUpload(file: any) {
  try {
    const res: any = await uploadImage(file.raw)
    await createBanner({
      banner_img: res.data.url,
      article_id: null,
      sort: banners.value.length + 1,
      status: 1,
    })
    ElMessage.success('已添加')
    loadBanners()
  } catch {
    ElMessage.error('上传失败')
  }
}
async function updBanner(id: number, data: any) {
  await updateBanner(id, data)
}
async function delBanner(row: any) {
  await deleteBanner(row.id)
  ElMessage.success('已删除')
  loadBanners()
}
onMounted(() => {
  loadSite()
  loadBanners()
  loadArticles()
})
</script>

<style scoped>
.toolbar {
  margin-bottom: 16px;
}
.bn-img {
  width: 140px;
  height: 54px;
  object-fit: cover;
  border-radius: 4px;
}
</style>
