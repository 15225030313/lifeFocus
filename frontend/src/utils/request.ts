import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

// 默认相对路径：由后端统一托管时使用同源 /api；开发模式由 Vite 代理转发
const base = import.meta.env.VITE_API_BASE || ''
export const API_BASE = base

const service = axios.create({
  baseURL: `${base}/api`,
  timeout: 10000,
})

service.interceptors.request.use((config) => {
  const token = localStorage.getItem('lf_token')
  if (token) {
    config.headers = config.headers || {}
    ;(config.headers as any).Authorization = `Bearer ${token}`
  }
  return config
})

service.interceptors.response.use(
  (res) => {
    const data = res.data
    if (data && typeof data.code === 'number' && data.code !== 200) {
      ElMessage.error(data.message || '请求失败')
      return Promise.reject(data)
    }
    return data
  },
  (err) => {
    const status = err.response?.status
    if (status === 401) {
      localStorage.removeItem('lf_token')
      localStorage.removeItem('lf_user')
      ElMessage.error('登录已过期，请重新登录')
      const path = router.currentRoute.value.path
      if (path.startsWith('/admin') && !path.includes('/login')) {
        router.replace('/admin/login')
      }
    } else if (status === 403) {
      ElMessage.error('无权限访问')
    } else {
      ElMessage.error(err.message || '网络错误')
    }
    return Promise.reject(err)
  }
)

export function imgUrl(p?: string): string {
  if (!p) return ''
  if (p.startsWith('http')) return p
  return `${base}${p}`
}

export default service
