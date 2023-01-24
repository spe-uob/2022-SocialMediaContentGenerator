
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') },
      { path: '/LabStation', component: () => import('pages/LabStation.vue')},
      { path: '/StatisticsData', component: () => import('pages/StatisticsData.vue')},
      { path: '/AboutUs', component: () => import('pages/AboutUs.vue')},
      { path: '/AppInfo', component: () => import('pages/AppInfo.vue')},
      { path: '/AppSettings', component: () => import('pages/AppSettings.vue')},
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
