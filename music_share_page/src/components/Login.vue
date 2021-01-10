<template>
  <div>
    <el-dialog title="登入" :visible.sync="dialogFormVisible">
      <el-form :model="form">
        <el-form-item label="用户名" label-width="120px">
          <el-input placeholder="请输入用户名" v-model="form.username" autocomplete="off" clearable></el-input>
        </el-form-item>
        <el-form-item label="密码" label-width="120px">
          <el-input placeholder="请输入密码" v-model="form.password" autocomplete="off" show-password></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="loginCLick">登 入</el-button>
      </div>
    </el-dialog>
    <el-button type="text" @click="dialogFormVisible = true">登入</el-button>
  </div>

</template>

<script>
export default {
  name: "login",
  data() {
    return {
      form : {
        username : '',
        password : ''
      },
      dialogFormVisible : false,
      loginUrl : 'http://123.57.145.198:5000' + '/api/login'
    }
  },
  methods: {
    login(username, password) {
      let dataBody = {
        username, password
      }
      this.axios.post(this.loginUrl, dataBody
      ).then((res) => {
        if (res.data.token === undefined) {
          throw res.data.msg
        }
        this.$store.commit({
          type : 'updateLoginState',
          token : res.data.token,
          username
        })
        this.dialogFormVisible = false
        this.$message({
          message: '登入成功，用户' + username,
          type: 'success'
        })
      }).catch((err) =>{
        this.$message.error(
            err
        )
      })
    },
    loginCLick() {
      this.login(this.form.username, this.form.password)
    }
  }
}
</script>

<style scoped>

</style>