<template>
  <div>
    <el-dialog title="注册" :visible.sync="dialogFormVisible">
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
        <el-button type="primary" @click="registerCLick">注 册</el-button>
      </div>
    </el-dialog>
    <el-button type="text" @click="dialogFormVisible = true">注册</el-button>
  </div>

</template>

<script>
export default {
  name: "register",
  data() {
    return {
      form : {
        username : '',
        password : ''
      },
      dialogFormVisible : false,
      registerUrl : "http://123.57.145.198:5000" + '/api/register'
    }
  },
  methods: {
    register(username, password) {
      let dataBody = {
        username, password
      }
      console.log(this.registerUrl)
      this.axios.post(this.registerUrl, dataBody
      ).then((res) => {
        if (res.data.username === undefined) {
          throw res.data.msg
        }
        this.dialogFormVisible = false
        this.$message({
          message: '注册成功，用户' + username,
          type: 'success'
        })
      }).catch((err) =>{
        this.$message.error(
            err
        )
      })
    },
    registerCLick() {
      this.register(this.form.username, this.form.password)
    }
  }
}
</script>

<style scoped>

</style>