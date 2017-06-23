<template>
  <div class="music">

    <h2>Music Library</h2>
    <img src="../assets/music.png" style="max-width: 300px;">

    <div v-if="!isDownloadingSong" class="add-song"><a @click="addSong"><button type="button" class="btn btn-success">Add a new song</button></a></div>
    <div v-else>
      <div class="download-info">
        <div v-if="downloadState === 'finished'">Converting (this may take a few minutes)...</div>
        <div v-else>Downloading...</div>
        <div class="progress">
          <div class="progress-bar progress-bar-success progress-bar-striped active" role="progressbar" :aria-valuenow="downloadProgressValue" aria-valuemin="0" aria-valuemax="100" v-bind:style="{ width: downloadProgressValue + '%' }">
          </div>
        </div>
      </div>
    </div>

    <div class="songs">
      <div v-for="song in songs" class="song">
        <div v-if="song.thumbnail" class="song-thumbnail"><img :src="apiBaseUrl + '/thumbnail/' + song.thumbnail"></div>
        <div class="song-filename">{{ song.filename }}</div>
        <div style="clear: both;"></div>
      </div>
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
  name: 'music',
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
    setDownloadProgress (progressValue) {
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
    eventhub.$on(EVENT_DOWNLOAD_PROGRESS, this.setDownloadProgress)
    eventhub.$on(EVENT_DOWNLOAD_STATE, this.setDownloadState)
    this.downloadProgressValue = 0
  },

  beforeDestroy () {
    eventhub.$off(EVENT_DOWNLOAD_PROGRESS, this.setDownloadProgress)
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
.music {
  margin-top: 10px;
  margin-bottom: 60px;
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

td.td-actions {
  text-align: right;
  padding-right: 40px;
}

.add-song {
  margin-bottom: 20px;
}

.songs {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}

.song {
  max-width: 400px;
  margin: 20px;
  padding: 10px;
  border: 1px solid #eee;
  border-radius: 2px;
}

.song-thumbnail img {
  max-width: 200px;
  float: left;
  margin-right: 10px;
}

.download-info {
  margin: 10px;
  margin-bottom: 20px;
}
.progress {
  max-width: 600px;
  margin: auto;
}
</style>
