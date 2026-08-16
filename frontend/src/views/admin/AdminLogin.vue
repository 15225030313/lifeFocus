<template>
  <div class="login-wrap">
    <el-card class="login-card">
      <h2>管理员登录</h2>
      <el-form :model="form" @submit.prevent="onSubmit">
        <el-form-item>
          <el-input v-model="form.username" placeholder="用户名" :prefix-icon="User" />
        </el-form-item>
        <el-form-item>
          <el-input
            v-model="form.password"
            type="password"
            placeholder="密码"
            :prefix-icon="Lock"
            show-password
            @keyup.enter="onSubmit"
          />
        </el-form-item>
        <el-button type="primary" style="width: 100%" :loading="loading" @click="onSubmit">登录</el-button>
      </el-form>
      <p class="tip">默认账号 admin / admin123</p>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { User, Lock } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { adminLogin } from '@/api'
import { useUserStore } from '@/store/user'

const router = useRouter()
const userStore = useUserStore()
const form = ref({ username: '', password: '' })
const loading = ref(false)

async function onSubmit() {
  if (!form.value.username || !form.value.password) {
    ElMessage.warning('请输入账号和密码')
    return
  }
  loading.value = true
  try {
    const r: any = await adminLogin(form.value.username, form.value.password)
    if (r.code === 200) {
      userStore.set(r.data.token, r.data.username)
      ElMessage.success('登录成功')
      router.replace('/admin/dashboard')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-wrap {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #e6f7f4, #f5f7f8);
}
.login-card {
  width: 360px;
  padding: 12px;
}
.login-card h2 {
  text-align: center;
  margin: 8px 0 20px;
  color: var(--primary);
}
.tip {
  text-align: center;
  color: var(--text-3);
  font-size: 12px;
  margin: 12px 0 0;
}
</style>
