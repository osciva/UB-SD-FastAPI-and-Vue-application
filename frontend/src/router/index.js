import Vue from 'vue'
import Router from 'vue-router'
import Matches from '@/components/Matches'
import Login from '@/components/Login.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    { // poner path: '/login' si queremos runnear primero matches o poner path: '/' para runnear primero login
      path: '/',
      name: 'Login',
      component: Login
    },
    { //  poner path: '/' si queremos runnear primero matches o poner path: '/matches' para runnear primero login
      path: '/matches',
      name: 'Matches',
      component: Matches
    }
  ]
})
