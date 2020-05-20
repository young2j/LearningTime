<template>
  <div class="login">
    <section class="form-container">
      <div class="form-body">
        <span class="title">资金管理后台系统</span>
        <el-form
          :model="loginForm"
          status-icon
          :rules="rules"
          ref="loginRef"
          label-width="100px"
          class="login-form"
          size="medium"
        >
          <el-form-item label="用户名" prop="usernameOrEmail">
            <el-input v-model="loginForm.usernameOrEmail" placeholder="请输入用户名或邮箱"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input
              type="password"
              v-model="loginForm.password"
              autocomplete="off"
              placeholder="请输入密码"
            ></el-input>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="submitForm('loginRef')" class='login-btn'>确定</el-button>
          </el-form-item>
        </el-form>
        <div class="go-register">
          还没有账号？<router-link to='/register'>去注册</router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import jwtDecode from 'jwt-decode'

export default {
  name: 'login',
  components: {},
  data () {
    return {
      loginForm: {
        usernameOrEmail: '',
        password: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名或邮箱', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '密码不能为空', trigger: 'blur' },
          { min: 6, max: 30, message: '密码6-30个字符', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    isEmpty (value) {
      return (
        value === undefined || value === null ||
        (typeof (value) === 'object' && Object.keys(value).length === 0) ||
        (typeof (value) === 'string' && value.trim().length === 0)
      )
    },
    submitForm (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          // console.log(this.loginForm)
          this.$axios.post('/login', this.loginForm)
            .then(res => {
              this.$message({
                message: '登录成功',
                type: 'success'
              })
              this.$router.push('/index') // 实际不能放这里

              // 验证Token
              const { token } = res.data
              window.localStorage.setItem('Token', token)

              // 解析Token
              const decodeJWT = jwtDecode(token)
              // 存储到vuex
              this.$store.dispactch('setAuthenticated', !this.isEmpty(decodeJWT))
              this.$store.dispactch('setUser', decodeJWT)

              // this.$router.push('/index')
            })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    }
  }
}
</script>

<style lang='less' scoped>
.login {
  background: url("../assets/bg.jpeg") no-repeat center center;
  background-size: cover;
  width: 100vw;
  height: 100vh;
  position: relative;

  .form-container {
    position: absolute;
    top: 20%;
    left: 30%;
    width: 40%;
    background-color: #efefef;
    padding-top: 30px;
    .form-body {
      text-align: center;
      .title{
        font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
        color: #606266;
        font-size: 18px;
      }
      .login-form{
        margin-top: 30px;
        .el-form-item{
          width: 90%;
          label{
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            color: aliceblue;
            font-size: 18px;
          }
        }
        .login-btn{
          width: 100%;
        }
      }
      .go-register{
        padding-bottom: 30px;
        text-align: center;
      }
    }
  }
}
</style>
