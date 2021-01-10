<template>
  <div>
    <el-dialog title="上传" :visible.sync="dialogFormVisible" width="400px">
      <el-upload
          v-loading="loading"
          element-loading-text="拼命上传中"
          element-loading-spinner="el-icon-loading"
          element-loading-background="rgba(0, 0, 0, 0.8)"
          class="upload-demo"
          drag
          :action="uploadUrl"
          :on-change="fileChange"
          @submit="submit"
          :auto-upload="false"
          :disabled="loading"
          multiple>
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">将音乐文件拖到此处，或<em>点击上传</em></div>
      </el-upload>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
      </div>
    </el-dialog>
    <el-button type="text" @click="dialogFormVisible = true">上传</el-button>
  </div>

</template>

<script>
export default {
  name: "MusicUpload.vue",
  data() {
    return {
      uploadUrl : "http://123.57.145.198:5000/" + '/api/upload',
      file : '',
      loading : false,
      dialogFormVisible : false,
    }
  },
  methods: {
    submit() {
      if (this.file === '') {
        return
      }
      if (this.$store.state.token === '') {
        this.$message.error('Please login first')
      } else {
        let formData = new FormData()
        formData.append('file', this.file.raw)
        formData.append('filename', this.file.name)
        formData.append('token', this.$store.state.token)

        this.loading = true

        this.axios.post(this.uploadUrl, formData,{
          headers: {
            "Content-Type": "multipart/form-data"
          }
        }
        ).then(res => {
          console.log(res)
          this.loading = false

          let msg = '<i>歌曲名：</i><b>' + res.data.title + '</b><br><i>歌手：</i><b>' + res.data.artist + '</b><br><i>专辑：</i><b>' + res.data.album + '</b><br><i>贡献者：</i><b>' + res.data.contributor + '</b><br>'

          console.log(msg)

          this.$notify({
            title: '成功上传歌曲',
            dangerouslyUseHTMLString: true,
            message: msg,
            type: 'success',
            duration: 0
          })
        }).catch(err => {
          this.loading = false
          this.$notify.error({
            title: '出错',
            message: err,
            duration: 0
          })
        })
      }
      this.file = ''
    },
    fileChange(file) {
      this.file = file
      this.submit()
    }
  }
}
</script>

<style scoped>

</style>