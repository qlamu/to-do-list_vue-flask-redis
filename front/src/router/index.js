import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Authentication from '@/components/Authentication'
import Logs from '@/components/Logs'

Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Authentication,
    props: { showRegister: false }
  },
  {
    path: '/signup',
    name: 'Register',
    component: Authentication,
    props: { showRegister: true }
  },
  {
    path: '/logs',
    name: 'Logs',
    component: Logs,
  },
  {
    path: '/:list_id',
    name: 'Editor',
    component: Home,
  },
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
