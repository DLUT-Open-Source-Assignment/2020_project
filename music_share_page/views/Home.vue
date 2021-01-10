<template>
  <div class="home">
    <el-row >
      <el-col :span="1"><login></login></el-col>
      <el-col :span="1"><register></register></el-col>
      <el-col :span="1"><music-upload /></el-col>
      <el-col :span="1"><el-button type="text" @click="update">更新</el-button></el-col>
    </el-row>

    <el-row>
      <el-col :span="12"><music-list ref="musicList"/></el-col>
      <el-col :span="12"><play-list ref="playList"/></el-col>
    </el-row>

    <audio :src="this.$store.state.playUrl" ref="audio" controls style="position:fixed; bottom:0; width: 100%"></audio>


  </div>
</template>

<script>
// @ is an alias to /src
import MusicList from '@/components/MusicList'
import Login from "@/components/Login";
import MusicUpload from "@/components/MusicUpload";
import PlayList from "@/components/PlayList";
import Register from "@/components/Register";

export default {
  name: 'Home',
  components: {
    Register,
    Login,
    MusicList,
    MusicUpload,
    PlayList
  },
  mounted() {
    this.$refs.playList.setAudio(this.$refs.audio)
  },
  methods: {
    update() {
      this.$refs.musicList.update()
      this.$refs.playList.update()
      console.log(233)
    }
  }
}
</script>
