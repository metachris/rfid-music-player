import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: require('@/components/Home')
    },
    {
      path: '/tags',
      name: 'Tags',
      component: require('@/components/Tags')
    },
    {
      path: '/add-tag',
      name: 'AddTag',
      component: require('@/components/AddTag')
    },
    {
      path: '/music',
      name: 'Music',
      component: require('@/components/Music')
    },
    {
      path: '/music/:songHash',
      name: 'Song',
      component: require('@/components/Song')
    }
  ]
})
