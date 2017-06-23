<template>
  <div id="app">
    <nav>
      <div class="nav-item nav-brand" v-bind:class="{ 'active': route.name === 'Home' }">
        <router-link to="/">RFID Music Player</router-link>
      </div>
      <div class="nav-item" v-bind:class="{ 'active': ['Tags', 'AddTag'].indexOf(route.name) > -1 }">
        <router-link to="/tags">Tags</router-link>
      </div>
      <div class="nav-item" v-bind:class="{ 'active': route.name === 'Music' }">
        <router-link to="/music">Music</router-link>
      </div>
      <div style="clear:both;"></div>
    </nav>

    <div v-if="!browserHasWebSocketSupport" id="error-no-websocket" class="app-errors alert alert-danger" role="alert">
      <img src="./assets/turntable.svg" style="max-width: 300px;">

      <p><b>
        Your browser does not support WebSockets!
      </b></p>
      <p>Please switch to a more modern browser such as <a href="https://www.mozilla.org/firefox/new/">Firefox</a> or <a href="https://www.google.com/chrome/browser/desktop">Chrome</a>.</p>
    </div>

    <div v-if="hasErrors" id="app-errors">
      <div v-for="error in getErrors" class="app-errors alert alert-danger" role="alert">
        <b>{{ error }}</b>
      </div>
    </div>

    <router-view v-if="browserHasWebSocketSupport"></router-view>
  </div>
</template>

<script>
import 'bootstrap/dist/css/bootstrap.min.css'

import { mapState, mapGetters } from 'vuex'

export default {
  name: 'app',
  computed: {
    ...mapState([
      'browserHasWebSocketSupport',
      'errors',
      'route'
    ]),
    ...mapGetters([
      'hasErrors',
      'getErrors'
    ])
  },
  created () {
    if (!this.$store.state.browserHasWebSocketSupport) {
      console.error('Browser does not support WebSockets. This webapp does not work in this browser..')
      return
    }

    this.$store.dispatch('websocketConnect')

    // Load initial data
    this.$store.dispatch('loadTags')
    this.$store.dispatch('loadSongs')
  }
}
</script>

<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #131313;
}

a {
  cursor: pointer;
}

nav {
  background: #4444b3;
  text-align: left;
}

.nav-item {
  display: inline-block;
  float: left;
  color: white;
  font-size: 16px;
}

.nav-item:hover,
.nav-item:focus,
.nav-item a:focus,
.nav-item a:hover,
.nav-item.active  {
  background: #1d1d7d;
  color: white;
  text-decoration: none;
}

.nav-item.active {
}

.nav-item a {
  display: block;
  color: white;
  text-decoration: none;
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 20px;
  padding-right: 20px;
}

.app-errors {
  margin-top: 40px;
  margin: 30px;
  padding: 10px;
}
</style>
