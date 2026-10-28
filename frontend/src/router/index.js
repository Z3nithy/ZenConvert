import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      meta: { title: 'ZenConvert — seu espaço de arquivos' },
      component: () => import('@/views/HomeDashboard.vue'),
    },
    {
      path: '/design-system',
      name: 'design-system',
      meta: { title: 'Design System — ZenConvert' },
      component: () => import('@/views/DesignSystem.vue'),
    },
  ],
})

router.afterEach((to) => {
  document.title = to.meta.title
})

export default router
