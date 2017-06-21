<template>
  <div id="app">
    <router-link to="/"><img src="./assets/turntable.svg" style="max-width: 300px;"></router-link>
    <router-view></router-view>
  </div>
</template>

<script>
import 'bootstrap/dist/css/bootstrap.min.css'
import eventhub, { EVENT_RFID_DETECTED, EVENT_DOWNLOAD_PROGRESS, EVENT_DOWNLOAD_STATE } from './eventhub'
import * as settings from './settings'

export default {
  name: 'app',
  created () {
    // Load initial data
    this.$store.dispatch('loadTags')
    this.$store.dispatch('loadSongs')

    // Setup Websockets
    const vm = this
    vm.ws = new WebSocket(settings.WEBSOCKET_URL)

    vm.ws.onopen = function () {
      vm.ws.send('Hello, world')
    }

    vm.ws.onmessage = function (event) {
      const [msgType, msgValue] = event.data.split(':')
      console.log(event.data, msgType, msgValue)
      if (msgType === EVENT_RFID_DETECTED) {
        eventhub.$emit(EVENT_RFID_DETECTED, msgValue)
      } else if (msgType === EVENT_DOWNLOAD_PROGRESS) {
        eventhub.$emit(EVENT_DOWNLOAD_PROGRESS, msgValue)
      } else if (msgType === EVENT_DOWNLOAD_STATE) {
        eventhub.$emit(EVENT_DOWNLOAD_STATE, msgValue)
      }
    }
  },
  beforeDestroy () {
    // Cleanup websockets
    this.ws.onmessage = null
    this.ws = null
  }
}
</script>

<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 30px;
}
</style>
