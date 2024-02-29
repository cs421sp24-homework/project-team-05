import { createRouter, createWebHistory } from 'vue-router'
import Login from '.././views/Login.vue'
import Signup from '.././views/Signup.vue'
import Profile from '.././views/Profile.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // {
    //   path: '/',
    //   name: 'home',
    //   component: HomeView
    // },
    {
        path: '/login',
        component: Login,
        name: 'login'
    },
    {
        path: '/signup',
        component: Signup
    },
    {
        path: '/profile',
        component: Profile
    },
  ]
})

export default router
