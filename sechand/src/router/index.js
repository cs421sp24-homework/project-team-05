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
import Empty from '@/views/Empty.vue'
import Chat from '@/views/Chat.vue'

import ChatTest from '../views/ChatTest.vue'; // Import your chat component

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
    },
    // Chat DEV
    {
      path: '/chattest/:roomId/',
      name: 'chattest',
      component: ChatTest,
      props: true,
    },
    {
      path: '/userhome',
      name: 'UserHome',
      component: UserHome,
      meta: { requiresAuth: true }
    },
    {
      path: '/me',
      name: 'Me',
      component: Me,
      meta: { requiresAuth: true }
    },
    {
      path: '/postitem',
      name: 'PostItem',
      component: PostItem,
      meta: { requiresAuth: true }
    },
    {
      path: '/showitem',
      component: Empty,
      meta: { requiresAuth: false }
    },
    {
      path: '/edititem',
      component: Empty,
      meta: { requiresAuth: true }
    },
    {
      path: '/showitem/:id',
      name: 'ShowItem',
      component: ShowItem,
      meta: { requiresAuth: false }
    },
    {
      path: '/edititem/:id',
      name: 'EditItem',
      component: EditItem,
      meta: { requiresAuth: true }
    },
    {
        path: '/login',
        component: Login,
        name: 'Login',
        meta: { requiresAuth: false }
    },
    {
        path: '/signup',
        component: Signup,
        name: "Signup",
        meta: { requiresAuth: false }
    },
    {
        path: '/profile',
        component: Profile,
        name: 'Profile',
        meta: { requiresAuth: true }
    },
    {
        path: '/chat',
        component: Chat,
        name: 'Chat',
        meta: { requiresAuth: false }
    },
  ]
})

router.beforeEach((to, from, next) => {
    const isAuthenticated = localStorage.getItem('access_token');
    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (!isAuthenticated) {
            next({ name: 'Home' });

        } 
        else {
            next();
        }
    } 
    else {
        next(); 
    }
  }
);

export default router
