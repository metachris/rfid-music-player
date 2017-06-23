<template>
  <div class="home">
    <div class="main-items">
      <router-link to="/tags">
        <div class="main-item">
          <h2>RFID Tags</h2>
          <img src="../assets/rfid.png">
        </div>
      </router-link>

      <router-link to="/music">
        <div class="main-item">
          <h2>Music Library</h2>
          <img src="../assets/music.png">
        </div>
      </router-link>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import eventhub, { EVENT_DOWNLOAD_PROGRESS, EVENT_DOWNLOAD_STATE } from '../eventhub'
import * as settings from '../settings'

let data = {
  downloadProgressValue: null,
  downloadState: null
}

export default {
  name: 'home',
  data: function () {
    return data
  },
  computed: {
    apiBaseUrl () { return settings.API_BASE_URL },
    ...mapState([
      'songs',
      'tags',
      'isDownloadingSong'
    ])
  },

  methods: {
    removeTag (tagId) {
      this.$store.dispatch('removeTag', tagId)
    },

    downloadProgress (progressValue) {
      console.log(EVENT_DOWNLOAD_PROGRESS, progressValue)
      this.downloadProgressValue = progressValue
    },

    setDownloadState (downloadState) {
      console.log('setDownloadState', downloadState)
      this.downloadState = downloadState
    },

    ...mapActions([
      'addSong'
    ])
  },

  mounted () {
    eventhub.$on(EVENT_DOWNLOAD_PROGRESS, this.downloadProgress)
    eventhub.$on(EVENT_DOWNLOAD_STATE, this.setDownloadState)
    this.downloadProgressValue = 0
  },

  beforeDestroy () {
    eventhub.$off(EVENT_DOWNLOAD_PROGRESS, this.downloadProgress)
    eventhub.$off(EVENT_DOWNLOAD_STATE, this.setDownloadState)
    this.tagId = null
    this.tagLabel = ''
    this.tagSongHash = null
    this.isSaving = false
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.home {
  margin-top: 80px;
  margin-bottom: 60px;
}

a {
  cursor: pointer;
}

h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin: 0 10px;
}

a {
  color: #42b983;
}

.main-items {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  margin-top: 30px;
  margin-bottom: 30px;
}

.main-items a:hover {
  text-decoration: none;
}

.main-item {
  margin: 20px;
  width: 300px;
  min-width: 120px;
  height: 300px;
  border: 2px solid #ccc;
  border-radius: 5px;
  padding: 20px;
  cursor: pointer;
}

.main-item:hover {
  border: 2px solid #666;
  background: #fafade;
}

.main-item img {
  max-width: 200px;
}

.main-item h2 {
  margin: 0;
  margin-bottom: 8px;
}

</style>
