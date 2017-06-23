<template>
  <div class="add-tag">

    <h2>Add a RFID Tag</h2>
    <img src="../assets/rfid.png" style="max-width: 300px;">

    <div v-if="waitingForTag">
      <div><b>Waiting for a RFID tag...</b></div>
      <img src="../assets/loader.gif" style="max-width:100px;">
      <div><router-link to="/tags">Cancel</router-link></div>
    </div>

    <div v-else>
      <div>Tag ID: {{ tagId }}</div>
      <div><a @click="setLabel" v-if="!isSaving">Label</a><span v-else>Label</span>: {{ tagLabel }}</div>
      <div v-if="song">
        <div><a @click="setShowSongPicker" v-if="!isSaving">Song</a><span v-else>Song</span>:</div>
        <div><center>{{ song.filename }}</center></div>
        <div v-if="song.thumbnail" class="song-current-thumbnail"><center><img :src="apiBaseUrl + '/thumbnail/' + song.thumbnail"></center></div>
      </div>

      <div v-if="showSongPicker" class="song-picker">
        <h3>Pick a song:</h3>
        <div class="songs">
          <div v-for="song in songs" class="song" @click="setSong(song.hash)">
            <div v-if="song.thumbnail" class="song-thumbnail"><img :src="apiBaseUrl + '/thumbnail/' + song.thumbnail"></div>
            <div class="song-filename">{{ song.filename }}</div>
          </div>
        </div>
      </div>

      <button v-if="song && !isSaving" @click="save" class="btn">Save</button>
      <div v-if="isSaving">Saving...</div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import eventhub, { EVENT_RFID_DETECTED } from '../eventhub'
import * as settings from '../settings'

let data = {
  tagId: null,
  tagLabel: '',
  tagSongHash: null,
  isSaving: false
}

export default {
  name: 'add-tag',
  data: function () {
    return data
  },
  computed: {
    apiBaseUrl () { return settings.API_BASE_URL },
    ...mapState([
      'songs',
      'isDownloadingSong'
    ]),
    waitingForTag () {
      return !this.tagId
    },
    showSongPicker () {
      return !this.tagSongHash
    },
    song () {
      if (!this.tagSongHash) return null
      for (let s of this.$store.state.songs) {
        if (s.hash === this.tagSongHash) {
          return s
        }
      }
    }
  },
  methods: {
    rfidDetected (rfidId) {
      console.log('rfid detected:', rfidId)
      this.tagId = rfidId
    },

    setLabel () {
      const label = window.prompt('Label for this RFID Tag:', this.tagLabel)
      console.log(label)
      if (!label) return
      this.tagLabel = label
    },

    setShowSongPicker () {
      this.tagSongHash = null
    },

    setSong (songHash) {
      console.log('setSong:', songHash)
      this.tagSongHash = songHash
    },

    save () {
      const tag = {
        rfidId: this.tagId,
        label: this.tagLabel,
        songHash: this.tagSongHash
      }
      this.isSaving = true
      this.$store
        .dispatch('saveTag', tag)
        .then(() => this.$router.push('/'))
        .catch((e) => console.error(e))
    }
  },

  mounted () {
    eventhub.$on(EVENT_RFID_DETECTED, this.rfidDetected)
  },

  beforeDestroy () {
    eventhub.$off(EVENT_RFID_DETECTED, this.rfidDetected)
    this.tagId = null
    this.tagLabel = ''
    this.tagSongHash = null
    this.isSaving = false
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
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

.song-picker {
  margin-top: 20px;
}

.songs {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
}

.song {
  max-width: 400px;
  margin: 10px;
  padding: 10px;
  border: 1px solid #eee;
  border-radius: 2px;
}

.song-thumbnail img {
  max-width: 180px;
  float: left;
  margin-right: 10px;
}

.song-current-thumbnail img {
  max-width: 280px;
}

.song-picker .song {
  cursor: pointer;
}

.song-picker .song:hover {
  border: 1px solid #a5a5a5;
  background: #ffe8ce;
}

.btn {
  margin-top: 10px;
  cursor: pointer;
  background: #50d130;
  background-image: linear-gradient(to bottom, #50d130, #47b82b);
  border-radius: 5px;
  font-family: Arial;
  color: #ffffff;
  font-size: 20px;
  padding: 10px 20px 10px 20px;
  text-decoration: none;
}

.btn:hover {
  background: #3cb0fd;
  background-image: linear-gradient(to bottom, #3cb0fd, #3498db);
  text-decoration: none;
}

</style>
