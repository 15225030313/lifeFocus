<template>
  <div v-loading="loading">
    <el-row :gutter="20" class="stats">
      <el-col :span="6" v-for="s in stats" :key="s.label">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-icon" :style="{ background: s.bg }">
            <el-icon><component :is="s.icon" /></el-icon>
          </div>
          <div>
            <div class="num">{{ s.value }}</div>
            <div class="label">{{ s.label }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-card class="latest" header="最新发布文章">
      <el-table :data="latest" stripe>
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="title" label="标题" />
        <el-table-column label="板块" width="120">
          <template #default="{ row }">
            <el-tag size="small" :type="row.plate_type === 1 ? 'warning' : 'primary'">
              {{ row.plate_type === 1 ? '生活妙招' : '世界奇观' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="view_count" label="浏览量" width="100" />
        <el-table-column label="状态" width="90">
          <template #default="{ row }">
            <el-tag size="small" :type="row.status === 1 ? 'success' : 'info'">
              {{ row.status === 1 ? '已发布' : '草稿' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="发布时间" width="120">
          <template #default="{ row }">{{ String(row.create_time).slice(0, 10) }}</template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Document, DataLine, Trophy, View } from '@element-plus/icons-vue'
import { getDashboard } from '@/api'

const loading = ref(true)
const latest = ref<any[]>([])
const stats = ref<any[]>([])

onMounted(async () => {
  try {
    const r: any = await getDashboard()
    const d = r.data || {}
    latest.value = d.latest || []
    stats.value = [
      { label: '总文章数', value: d.total_articles || 0, icon: Document, bg: '#E6F7F4' },
      { label: '生活妙招', value: d.life_articles || 0, icon: Trophy, bg: '#FFF1E6' },
      { label: '世界奇观', value: d.wonder_articles || 0, icon: View, bg: '#E8F0FE' },
      { label: '总浏览量', value: d.total_views || 0, icon: DataLine, bg: '#EAF1FF' },
    ]
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.stats {
  margin-bottom: 20px;
}
.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
}
.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: var(--primary);
}
.num {
  font-size: 26px;
  font-weight: 700;
}
.label {
  color: var(--text-3);
  font-size: 13px;
}
</style>
