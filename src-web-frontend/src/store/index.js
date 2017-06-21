import Vue from 'vue'
import Vuex from 'vuex'

import * as types from './mutation-types'
import * as settings from '../settings'

Vue.use(Vuex)

const state = {
  tags: [],
  songs: [],
  isDownloadingSong: false
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
  }
}

const actions = {
  loadTags ({ commit, state }) {
    console.log('action: loadTags')
    const url = `${settings.API_BASE_URL}/tags`
    Vue.axios.get(url).then((response) => {
      console.log('tags response:', response.data)
      commit(types.SET_TAGS, response.data.tags)
    })
  },

  loadSongs ({ commit, state }) {
    console.log('action: loadSongs')
    const url = `${settings.API_BASE_URL}/songs`
    Vue.axios.get(url).then((response) => {
      console.log('songs response:', response.data)
      commit(types.SET_SONGS, response.data.songs)
    })
  },

  addTag ({ commit, state }) {
    console.log('action: addTag')
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
        console.error(e, e.response.data)
        window.alert('Error: ' + e.response.data.error)
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
          window.alert(e.response.data)
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
        window.alert(e.response.data)
      })
  }
}

const getters = {
}

// A Vuex instance is created by combining the state, mutations, actions,
// and getters.
export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations
})
