
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: import('pages/HomePage.vue') },
      { path: '/home' , name: 'home', component: import('pages/HomePage.vue')},
      { path: '/twitter', component: () => import('pages/Twitter.vue')},
      { path:  '/TwitterView', component: () => import('pages/TwitterView.vue')},
      { path: '/StableDiffusionUI', component: () => import('pages/StableDiffusionUI.vue')},
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
