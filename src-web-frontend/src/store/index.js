import Vue from 'vue'
import Vuex from 'vuex'

import * as types from './mutation-types'
import * as settings from '../settings'
import eventhub, { EVENT_RFID_DETECTED, EVENT_DOWNLOAD_PROGRESS, EVENT_DOWNLOAD_STATE } from '../eventhub'

Vue.use(Vuex)

let websocketConnection = null

const state = {
  tags: [],
  songs: [],
  isDownloadingSong: false,

  browserHasWebSocketSupport: !!WebSocket,
  webSocketError: null,
  apiError: null
}

const mutations = {
  [types.ADD_SONG] (state, song) {
    state.songs.push(song)
  },
  [types.SET_SONGS] (state, songs) {
    state.songs = songs
  },
  [types.SET_TAGS] (state, tags) {
    state.tags = tags
  },
  [types.SET_UI_IS_SONG_DOWNLOADING] (state, isDownloading) {
    state.isDownloadingSong = isDownloading
  },
  [types.SET_WEBSOCKET_ERROR] (state, errorString) {
    state.webSocketError = errorString
  },
  [types.SET_API_ERROR] (state, errorString) {
    state.apiError = errorString
  }
}

const actions = {
  websocketConnect ({ commit, state }) {
    if (websocketConnection) {
      console.log('action websocketConnect: websocketConnection already exists', websocketConnection)
      return
    }

    websocketConnection = new WebSocket(settings.WEBSOCKET_URL)

    websocketConnection.onclose = function (e) {
      console.warn('ws.onclose', e)
      websocketConnection.onmessage = null
      websocketConnection = null

      commit(types.SET_WEBSOCKET_ERROR, 'WebSocket connection error.')

      console.log('Trying WebSocket reconnect in 5 seconds...')
      setTimeout(() => {
        actions.websocketConnect({ commit, state })
      }, 5000)
    }

    websocketConnection.onerror = function (e) {
      console.error('ws.onerror', e)
    }

    websocketConnection.onopen = function () {
      commit(types.SET_WEBSOCKET_ERROR, null)
      websocketConnection.send('Hello, world')
    }

    websocketConnection.onmessage = function (event) {
      console.log('websocketConnection.onmessage', event)
      const [msgType, msgValue] = event.data.split(':')
      console.log(`type: '${msgType}', value: ${msgValue}`)
      if (msgType === EVENT_RFID_DETECTED) {
        eventhub.$emit(EVENT_RFID_DETECTED, msgValue)
      } else if (msgType === EVENT_DOWNLOAD_PROGRESS) {
        eventhub.$emit(EVENT_DOWNLOAD_PROGRESS, msgValue)
      } else if (msgType === EVENT_DOWNLOAD_STATE) {
        eventhub.$emit(EVENT_DOWNLOAD_STATE, msgValue)
      }
    }
  },

  loadTags ({ commit, state }) {
    console.log('action: loadTags')
    const url = `${settings.API_BASE_URL}/tags`
    Vue.axios.get(url)
      .then((response) => {
        console.log('tags response:', response.data)
        commit(types.SET_TAGS, response.data.tags)
      }).catch((e) => {
        console.error(e)
        const errorString = (e.response && e.response.data) ? e.response.data : e.toString()
        commit(types.SET_API_ERROR, errorString)
      })
  },

  loadSongs ({ commit, state }) {
    console.log('action: loadSongs')
    const url = `${settings.API_BASE_URL}/songs`
    Vue.axios.get(url)
      .then((response) => {
        console.log('songs response:', response.data)
        commit(types.SET_SONGS, response.data.songs)
      }).catch((e) => {
        console.error(e)
        const errorString = (e.response && e.response.data) ? e.response.data : e.toString()
        commit(types.SET_API_ERROR, errorString)
      })
  },

  addSong ({ commit, state }) {
    console.log('action: addSong')
    const youtubeUrl = window.prompt('YouTube URL', 'https://www.youtube.com/watch?v=rJWZhitXWzI')
    if (!youtubeUrl) return
    if (youtubeUrl.indexOf('https://www.youtube.com/watch?v=') !== 0) {
      window.alert('Not a valid youtube URL (eg. "https://www.youtube.com/watch?v=rJWZhitXWzI")')
    }
    const youtubeId = youtubeUrl.split('=').slice(-1)[0]
    // console.log('addSong', youtubeUrl, youtubeId)

    commit(types.SET_UI_IS_SONG_DOWNLOADING, true)
    const url = `${settings.API_BASE_URL}/youtube-dl/${youtubeId}`
    Vue.axios.get(url)
      .then((response) => {
        console.log(response.data)
        commit(types.SET_UI_IS_SONG_DOWNLOADING, false)
      }).catch((e) => {
        console.error(e)
        const errorString = (e.response && e.response.data) ? e.response.data : e.toString()
        window.alert('Error: ' + errorString)
        commit(types.SET_API_ERROR, errorString)
        commit(types.SET_UI_IS_SONG_DOWNLOADING, false)
      })
      .then(() => {
        actions.loadSongs({ commit, state })
      })
  },

  saveTag ({ commit, state }, tag) {
    return new Promise((resolve, reject) => {
      console.log('action: saveTag', tag)
      let song = null
      for (let s of state.songs) {
        if (s.hash === tag.songHash) {
          song = s
          break
        }
      }

      if (!song) {
        console.error(`song ${tag.songHash} not found`)
        return
      }

      const url = `${settings.API_BASE_URL}/tags`
      Vue.axios
        .post(url, {
          id: tag.rfidId,
          label: tag.label,
          song: song.filename
        })
        .then((response) => {
          console.log(response.data)
          commit(types.SET_TAGS, response.data.tags)
          resolve(response.data)
        }).catch((e) => {
          console.error(e)
          const errorString = (e.response && e.response.data) ? e.response.data : e.toString()
          window.alert('Error: ' + errorString)
          commit(types.SET_API_ERROR, errorString)
          reject(e.response.data)
        })
    })
  },

  removeTag ({ commit, state }, tagId) {
    const reallyDelete = window.confirm(`Really delete tag with id '${tagId}'?`)
    if (!reallyDelete) return

    const url = `${settings.API_BASE_URL}/tags/${tagId}`
    console.log(url)
    Vue.axios
      .delete(url)
      .then((response) => {
        console.log(response.data)
        actions.loadTags({ commit, state })
      }).catch((e) => {
        console.error(e)
        const errorString = (e.response && e.response.data) ? e.response.data : e.toString()
        window.alert('Error: ' + errorString)
        commit(types.SET_API_ERROR, errorString)
      })
  }
}

const getters = {
  hasErrors: state => state.apiError || state.webSocketError,
  getErrors: state => {
    let errors = []
    if (state.apiError) errors.push(state.apiError)
    if (state.webSocketError) errors.push(state.webSocketError)
    return errors
  }
}

// A Vuex instance is created by combining the state, mutations, actions,
// and getters.
export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations
})
