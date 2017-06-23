<template>
  <div class="tags">

    <h2>RFID Tags</h2>
    <img src="../assets/rfid3.jpg" style="max-width: 300px;">

    <!-- <h2>RFID Tags</h2> -->
    <div class="add-tag"><router-link to="/add-tag"><button type="button" class="btn btn-success">Add a new tag</button></router-link></div>

    <center>
    <table class="table table-striped table-hover">
      <thead>
        <tr>
          <th>Tag ID</th>
          <th>Label</th>
          <th>Song</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="tag in tags">
          <td>{{ tag.id }}</td>
          <td>{{ tag.label }}</td>
          <td>{{ tag.song }}</td>
          <td class="td-actions">
            <a @click="removeTag(tag.id)" title="Remove"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span></a>
          </td>
        </tr>
      </tbody>
    </table>
    </center>

  </div>
</template>

<script>
import { mapState } from 'vuex'
import * as settings from '../settings'

export default {
  name: 'home',
  computed: {
    apiBaseUrl () { return settings.API_BASE_URL },
    ...mapState([
      'tags',
      'isDownloadingSong'
    ])
  },

  methods: {
    removeTag (tagId) {
      this.$store.dispatch('removeTag', tagId)
    }
  },

  beforeDestroy () {
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
  margin-top: 10px;
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

.add-tag {
  margin-bottom: 20px;
}

td.td-actions {
  text-align: right;
  padding-right: 40px;
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
