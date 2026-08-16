import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: () => import('@/views/front/FrontLayout.vue'),
      children: [
        { path: '', name: 'home', component: () => import('@/views/front/Home.vue') },
        { path: 'list/:plate', name: 'list', component: () => import('@/views/front/ArticleList.vue') },
        { path: 'article/:id', name: 'detail', component: () => import('@/views/front/ArticleDetail.vue') },
        { path: 'search', name: 'search', component: () => import('@/views/front/Search.vue') },
        { path: 'about', name: 'about', component: () => import('@/views/front/About.vue') },
      ],
    },
    {
      path: '/admin/login',
      name: 'adminLogin',
      component: () => import('@/views/admin/AdminLogin.vue'),
    },
    {
      path: '/admin',
      component: () => import('@/views/admin/AdminLayout.vue'),
      meta: { auth: true },
      children: [
        { path: '', redirect: '/admin/dashboard' },
        { path: 'dashboard', name: 'dashboard', component: () => import('@/views/admin/Dashboard.vue'), meta: { auth: true } },
        { path: 'articles', name: 'articleManage', component: () => import('@/views/admin/ArticleManage.vue'), meta: { auth: true } },
        { path: 'categories', name: 'categoryManage', component: () => import('@/views/admin/CategoryManage.vue'), meta: { auth: true } },
        { path: 'system', name: 'systemManage', component: () => import('@/views/admin/SystemManage.vue'), meta: { auth: true } },
      ],
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'notFound',
      component: () => import('@/views/front/NotFound.vue'),
    },
  ],
})

router.beforeEach((to) => {
  if (to.meta.auth) {
    const token = localStorage.getItem('lf_token')
    if (!token) return '/admin/login'
  }
})

export default router
