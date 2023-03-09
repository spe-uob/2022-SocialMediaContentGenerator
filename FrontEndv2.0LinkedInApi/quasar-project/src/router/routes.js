import Index from "layouts/Index.vue";
import Home from "pages/Home.vue";
import TwitterView from "pages/SignIn.vue";

const routes = [
  {
    path: '/',
    component: Index,
    children: [
      { path: '', component: Home },
      { path: '/home' , name: 'home', component: Home},
      { path: '/twitter', component: () => import('pages/Twitter.vue')},
      { path:  '/SignIn', component: () => import('pages/SignIn.vue')},
      { path: '/StableDiffusionUI', component: () => import('pages/StableDiffusionUI.vue')},
      { path: '/TimelineView', component: () => import('pages/TimelineView.vue')},
      { path: '/MyLinkedInPage', component: () => import('pages/MyLinkedInPage.vue')},
      { path: '/loginWithLinkedIn', component: () => import('pages/loginWithLinkedIn.vue')},
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
