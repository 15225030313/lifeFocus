import request from '@/utils/request'

// ---------- 前台公开 ----------
export const getSite = () => request.get('/site')
export const getCategories = (plateType?: number) =>
  request.get('/categories', { params: { plate_type: plateType } })
export const getBanners = () => request.get('/banners')
export const getArticles = (params: any) => request.get('/articles', { params })
export const getArticle = (id: number) => request.get(`/articles/${id}`)

// ---------- 管理员登录 ----------
export const adminLogin = (username: string, password: string) =>
  request.post('/admin/login', { username, password })

// ---------- 后台文章 ----------
export const getAdminArticles = (params: any) => request.get('/admin/articles', { params })
export const createArticle = (data: any) => request.post('/admin/articles', data)
export const updateArticle = (id: number, data: any) => request.put(`/admin/articles/${id}`, data)
export const deleteArticle = (id: number) => request.delete(`/admin/articles/${id}`)
export const batchDeleteArticles = (ids: number[]) =>
  request.post('/admin/articles/batch-delete', ids)

// ---------- 后台分类 ----------
export const getAdminCategories = (plateType?: number) =>
  request.get('/admin/categories', { params: { plate_type: plateType } })
export const createCategory = (data: any) => request.post('/admin/categories', data)
export const updateCategory = (id: number, data: any) => request.put(`/admin/categories/${id}`, data)
export const deleteCategory = (id: number) => request.delete(`/admin/categories/${id}`)

// ---------- 后台轮播 ----------
export const getAdminBanners = () => request.get('/admin/banners')
export const createBanner = (data: any) => request.post('/admin/banners', data)
export const updateBanner = (id: number, data: any) => request.put(`/admin/banners/${id}`, data)
export const deleteBanner = (id: number) => request.delete(`/admin/banners/${id}`)

// ---------- 系统 ----------
export const uploadImage = (file: File) => {
  const form = new FormData()
  form.append('file', file)
  return request.post('/admin/upload', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}
export const getDashboard = () => request.get('/admin/dashboard')
export const getAdminSite = () => request.get('/admin/site')
export const updateSite = (data: any) => request.put('/admin/site', data)
export const changePassword = (old_password: string, new_password: string) =>
  request.put('/admin/password', { old_password, new_password })
