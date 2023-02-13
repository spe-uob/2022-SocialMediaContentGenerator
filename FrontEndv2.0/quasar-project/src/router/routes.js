import Index from "layouts/Index.vue";
import Home from "pages/Home.vue";
import TwitterView from "pages/TwitterView.vue";

const routes = [
  {
    path: '/',
    component: Index,
    children: [
      { path: '', component: Home },
      { path: '/home' , name: 'home', component: Home},
<<<<<<< HEAD
      { path: '/StableDiffusionUI', component: () => import('pages/StableDiffusionUI.vue')},
      {path:  '/TwitterView', component: () => import('pages/TwitterView.vue')},
=======
      { path: '/twitter', component: () => import('pages/Twitter.vue')},
      { path:  '/TwitterView', component: () => import('pages/TwitterView.vue')},
>>>>>>> 5f1780183eb534b1769487e98f59fd2bb2d593e4
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
