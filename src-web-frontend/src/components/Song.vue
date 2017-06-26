<template>
  <div class="song">

    <h2 class="title">{{ song.filename }}</h2>
    <div v-if="song.thumbnail" class="song-thumbnail"><img :src="apiBaseUrl + '/thumbnail/' + song.thumbnail"></div>
    <div id="waveform"></div>
    <button @click="playPause" type="button" class="btn btn-success">Play/Pause</button>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import * as settings from '../settings'
import WaveSurfer from 'wavesurfer.js'

console.log('WaveSurfer', WaveSurfer)

let data = {
  song: {}
}

let wavesurfer

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
    playPause () {
      wavesurfer.playPause()
    }
  },

  created () {
  },

  mounted () {
    this.song = {}
    const viewSongHash = this.$store.state.route.params.songHash
    this.$store.state.songs.forEach((song) => {
      if (song.hash === viewSongHash) {
        this.song = song
      }
    })

    if (!this.song.hash) {
      // TODO: If reloading this page directly, this method is called before
      // the songs are loaded from App.vue!
      console.error(`No song with hash ${viewSongHash} found.`)
      return
    }

    console.log(this.song)

    wavesurfer = WaveSurfer.create({
      container: '#waveform',
      waveColor: 'violet',
      progressColor: 'purple',
      scrollParent: true
    })
    console.log('created wavesurfer:', wavesurfer, wavesurfer.load)

    const songUrl = `${settings.API_BASE_URL}/music/${this.song.filename}`
    console.log('songUrl', songUrl)
    wavesurfer.load(songUrl)
  },

  beforeDestroy () {
    // eventhub.$off(EVENT_DOWNLOAD_PROGRESS, this.setDownloadProgress)
    // eventhub.$off(EVENT_DOWNLOAD_STATE, this.setDownloadState)
    // this.tagId = null
    // this.tagLabel = ''
    // this.tagSongHash = null
    // this.isSaving = false
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.song {
margin: 20px 40px;
text-align: left;
}

h1, h2 {
  font-weight: normal;
}

h2.title {
  max-width: 800px;
}

.song-thumbnail img {
  max-width: 400px;
}

#waveform {
  margin-top: 10px;
  margin-bottom: 10px;
  border: 1px solid #600080;
  border-radius: 2px;
}
</style>
