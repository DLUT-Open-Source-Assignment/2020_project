<template>
  <div>
    <el-tabs type="border-card" >
      <el-tab-pane label="我的收藏">
        <el-table
            :data="likeList"
            style="width: 100%"
            max-height="530"
            height="530">
          <el-table-column
              fixed
              prop="title"
              label="歌曲名"
              width="150">
          </el-table-column>
          <el-table-column
              prop="artist"
              label="歌手"
              width="120">
          </el-table-column>
          <el-table-column
              prop="album"
              label="专辑"
              width="120">
          </el-table-column>
          <el-table-column
              prop="contributor"
              label="贡献者"
              width="120">
          </el-table-column>
          <el-table-column
              prop="collect_size"
              label="收藏数"
              width="120">
          </el-table-column>
          <el-table-column
              fixed="right"
              label="操作"
              width="100">
            <template slot-scope="scope">
              <el-button @click="handlePlayClick(scope, 0)" type="text" size="normal">播放</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="我的分享">
        <el-table
            :data="myMusicList"
            style="width: 100%"
            max-height="530"
            height="530">
          <el-table-column
              fixed
              prop="title"
              label="歌曲名"
              width="150">
          </el-table-column>
          <el-table-column
              prop="artist"
              label="歌手"
              width="120">
          </el-table-column>
          <el-table-column
              prop="album"
              label="专辑"
              width="120">
          </el-table-column>
          <el-table-column
              prop="contributor"
              label="贡献者"
              width="120">
          </el-table-column>
          <el-table-column
              prop="collect_size"
              label="收藏数"
              width="120">
          </el-table-column>
          <el-table-column
              fixed="right"
              label="操作"
              width="100">
            <template slot-scope="scope">
              <el-button @click="handlePlayClick(scope, 1)" type="text" size="normal">播放</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane key="addButton" :disabled='disable'>
       <span slot="label" style="padding: 8px">
         <el-button @click="changeMode">{{this.modeName()}}</el-button>
       </span>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
export default {
  name: "playList",
  data() {
   return {
     myMusicUrl : 'http://123.57.145.198:5000/' + '/api/get_my_music',
     likesUrl : 'http://123.57.145.198:5000/' + '/api/get_like',
     getMusicUrl : 'http://123.57.145.198:5000/' + '/api/get_music_url',
     likeList : [],
     myMusicList : [],
     playList : [],
     now : [],
     disable : true,
     mode : 0,
     pre : 0,
     audio : ''
   }
  },
  methods: {
    setAudio(audio) {
      audio.loop = false
      audio.autoplay = true

      audio.addEventListener('ended', () => {
        if (this.$store.state.tp === 0) {
          return
        }
        audio.load()
        this.nextAudio()
        this.getMusicLink(this.playList[this.now].pk)
        audio.play()
      }, false);
    },
    nextAudio() {
      if (this.mode === 0) {
        return
      } else if (this.mode === 1) {
        this.now = (this.now + 1) % this.playList.length
      } else if (this.mode === 2) {
        let k = Math.floor(Math.random() * this.playList.length)
        while (k === this.now) {
          k = Math.floor(Math.random() * this.playList.length)
        }
        console.log(k)
        this.now = k
      }
    },
    modeName() {
      if (this.mode <= 3) {
        this.pre = this.mode
        return this.getModeName(this.mode)
      }
      return this.getModeName(this.pre)
    },
    getModeName(mode) {
      if (mode === 0) {
        return '单曲循环'
      } else if (this.mode === 1) {
        return '顺序播放'
      } else if (this.mode === 2) {
        return '随机播放'
      }
    },
    changeMode() {
      this.mode = (this.mode + 1) % 3
    },
    getMyMusic() {
      let dataBody = {
        token : this.$store.state.token
      }
      this.axios.post(this.myMusicUrl, dataBody
      ).then((res) => {
        // console.log(res)
        this.myMusicList = res.data.my_music
      }).catch((err) =>{
        console.log(err)
      })
    },
    getMusicLink(id) {
      let dataBody = {
        music_id: id
      }
      // console.log(dataBody)
      this.axios.post(this.getMusicUrl, dataBody
      ).then((res) => {
        // console.log(res.data)
        this.$store.commit({
          type: 'updatePlayUrl',
          playUrl: res.data.link,
          tp : 1
        })
      }).catch((err) => {
        console.log(err)
      })
    },
    getLikes() {
      let dataBody = {
        token : this.$store.state.token
      }
      this.axios.post(this.likesUrl, dataBody
      ).then((res) => {
        console.log(res)
        this.likeList = res.data.likes
      }).catch((err) =>{
        console.log(err)
      })
    },
    update() {
      if (this.$store.state.token === '') return
      this.getLikes()
      this.getMyMusic()
    },
    handlePlayClick(row, tp) {
      this.now = row.$index
      if (tp === 0) {
        this.playList = this.likeList
      } else {
        this.playList = this.myMusicList
      }
      this.getMusicLink(this.playList[this.now].pk)
    },
  },
  mounted() {
    this.update()
  }
}
</script>

<style scoped>
.loginOut{
  position: absolute;right:20px;top:5px;
  color: #e6a23c;
  font-weight: 600;
  font-size: 14px;
}
</style>