import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import UserHome from '../views/UserHome.vue'
import Me from '../views/Me.vue'
import PostItem from '../views/PostItem.vue'
import ShowItem from '../views/ShowItem.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
    },
    {
      path: '/userhome',
      name: 'UserHome',
      component: UserHome,
    },
    {
      path: '/me',
      name: 'Me',
      component: Me,
    },
    {
      path: '/postitem',
      name: 'PostItem',
      component: PostItem,
    },
    {
      path: '/showitem/:id',
      name: 'ShowItem',
      component: ShowItem,
    },
  ]
})

export default router
