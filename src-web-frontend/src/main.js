// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'

import store from './store'
import App from './App'
import router from './router'
import { sync } from 'vuex-router-sync'

Vue.config.productionTip = false
Vue.use(VueAxios, axios)

// Setup vuex router sync
sync(store, router)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  router,
  template: '<App/>',
  components: { App }
})
