import Index from "layouts/Index.vue";
import Home from "pages/Home.vue";
import TwitterView from "src/pages/SignIn.vue";


const routes = [
  {
    path: '/',
    component: Index,
    children: [
      { path: '', component: Home },
      { path: '/home' , name: 'home', component: Home},
      { path: '/twitter', component: () => import('pages/Twitter.vue')},
      { path: '/FaceBookPost', component: () => import('pages/FaceBookPost.vue')},
      { path:  '/signin', component: () => import('src/pages/SignIn.vue')},
      { path: '/stablediffusionUI', component: () => import('pages/StableDiffusionUI.vue')},
      { path: '/TimelineView', component: () => import('pages/TimelineView.vue')},
      { path: '/LinkedInPost', component: () => import('pages/LinkedInPost.vue')},
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
