import Index from "layouts/Index.vue";
import Home from "pages/Home.vue";
import FaceBookPost from "src/pages/FaceBookPost.vue";
import PostPage from "src/pages/PostPage.vue";

const routes = [
  {
    path: '/',
    component: Index,
    children: [
      { path: '', component: Home },
      { path: '/twitter', component: () => import('pages/Twitter.vue')},
      { path: '/FaceBookPost', name: 'FaceBookPost', component: FaceBookPost},
      { path: '/signin', component: () => import('src/pages/SignIn.vue')},
      { path: '/stablediffusionUI', component: () => import('pages/StableDiffusionUI.vue')},
      { path: '/GeneratedImage', component: () => import('pages/GeneratedImage.vue')},
      { path: '/BlogPreview', component: () => import('pages/BlogPreview.vue')},
      { path: '/LinkedInPost', component: () => import('pages/LinkedInPost.vue')},
      { path: '/TextGenerator', component: () => import('pages/TextGenerator.vue')},
      { path: '/Text', component: () => import('pages/Text.vue')},
      { path: '/post', component: () => import('pages/PostPage.vue')},
      { path: '/aboutUs', component: () => import('pages/AboutUs.vue')},
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
