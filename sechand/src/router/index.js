import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import UserHome from '../views/UserHome.vue'
import Me from '../views/Me.vue'
import PostItem from '../views/PostItem.vue'
import ShowItem from '../views/ShowItem.vue'
import EditItem from '../views/EditItem.vue'
import Login from '.././views/Login.vue'
import Signup from '.././views/Signup.vue'
import Profile from '.././views/Profile.vue'

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
    {
      path: '/edititem/:id',
      name: 'EditItem',
      component: EditItem,
    },
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
