<template>
  <div>
    <el-tabs type="border-card">
      <el-tab-pane label="收藏榜单">
        <el-table
            :data="musicList"
            style="width: 100%"
            max-height="500"
            height="500">
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
              <el-button @click="handlePlayClick(scope.row)" type="text" size="small">播放</el-button>
              <el-button @click="handleLikeClick(scope.row)" type="text" size="small">收藏</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <div class="block">
        <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="currentPage"
            :page-sizes="[3, 5, 10, 20]"
            :page-size="pageSize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="musicSize">
        </el-pagination>
      </div>
    </el-tabs>
  </div>

</template>

<script>
export default {
  name: "musicList",
  data() {
    return {
      getListUrl : "http://123.57.145.198:5000" + '/api/get_music_list',
      getMusicUrl : "http://123.57.145.198:5000" + '/api/get_music_url',
      likeMusicUrl : "http://123.57.145.198:5000" + '/api/like',
      musicList : [],
      musicSize : 0,
      pageSize : 3,
      currentPage : 1,
    }
  },
  methods: {
    getList(l, r) {
      let dataBody = {
        l,r
      }
      this.axios.post(this.getListUrl, dataBody
      ).then((res) => {
        console.log(res)
        this.musicList = res.data.res
        this.musicSize = res.data.len
      }).catch((err) =>{
        console.log(err)
      })
    },
    getMusicLink(id) {
      let dataBody = {
        music_id : id
      }
      this.axios.post(this.getMusicUrl, dataBody
      ).then((res) => {
        this.$store.commit({
          type : 'updatePlayUrl',
          playUrl : res.data.link,
          tp : 0
        })
      }).catch((err) =>{
        console.log(err)
      })
    },
    likeMusic(music) {
      if (this.$store.state.token === '') {
        this.$message.error('Please login first')
      } else {
        let dataBody = {
          token : this.$store.state.token,
          music_id: music.pk
        }
        this.axios.post(this.likeMusicUrl, dataBody
        ).then((res) => {
          if (res.data.msg !== 'success') {
            throw 'Error'
          }
          this.$message({
            message: '成功收藏歌曲 ' + music.title + ' ' + '请手动刷新',
            type: 'success'
          })
        }).catch((err) =>{
          this.$message.error(
              err
          )
        })
      }
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.getList((this.currentPage - 1) * this.pageSize, this.currentPage * this.pageSize)
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.getList((this.currentPage - 1) * this.pageSize, this.currentPage * this.pageSize)
    },
    handlePlayClick(row) {
      this.getMusicLink(row.pk)
    },
    handleLikeClick(row) {
      this.likeMusic(row)
    },
    update() {
      this.getList((this.currentPage - 1) * this.pageSize, this.currentPage * this.pageSize)
    }
  },
  mounted() {
    this.update()
  }
}
</script>

<style scoped>

</style>