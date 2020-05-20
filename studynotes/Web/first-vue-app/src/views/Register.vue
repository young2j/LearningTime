<template>
  <div class="register">
    <section class="form-container">
      <div class="form-body">
        <span class="title">资金管理后台系统</span>
        <el-form
          :model="registerForm"
          status-icon
          :rules="rules"
          ref="registerRef"
          label-width="100px"
          class="register-form"
          size="medium"
        >
          <el-form-item label="用户名" prop="username">
            <el-input v-model="registerForm.username" placeholder="请输入用户名"></el-input>
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <el-input type="email" v-model="registerForm.email" placeholder="请输入邮箱"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input
              type="password"
              v-model="registerForm.password"
              autocomplete="off"
              placeholder="请输入密码"
            ></el-input>
          </el-form-item>
          <el-form-item label="确认密码" prop="checkPassword">
            <el-input
              type="password"
              v-model="registerForm.checkPassword"
              autocomplete="off"
              placeholder="请再次输入密码"
            ></el-input>
          </el-form-item>
          <el-form-item label="角色" prop="role">
            <el-select v-model="registerForm.role" placeholder="选择角色" class='role-select'>
              <el-option label="管理员" value="admin"></el-option>
              <el-option label="普通用户" value="user"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm('registerRef')" class="confirm-btn">确定</el-button>
            <el-button @click="resetForm('registerRef')" class='reset-btn'>重置</el-button>
          </el-form-item>
        </el-form>
        <div class="go-login">
          已有账号？<router-link to='/login'>去登录</router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'register',
  components: {},
  data () {
    const validatePassword = (rule, value, callback) => {
      console.log(rule, value, callback)
      if (value !== this.registerForm.password) {
        callback(new Error('两次输入密码不一致'))
      } else {
        callback()
      }
    }
    return {
      registerForm: {
        username: '',
        email: '',
        password: '',
        checkPassword: '',
        role: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        email: [
          { type: 'email', required: true, message: '请输入邮箱', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '密码不能为空', trigger: 'blur' },
          { min: 6, max: 30, message: '密码6-30个字符', trigger: 'blur' }
        ],
        checkPassword: [
          { required: true, message: '密码不能为空', trigger: 'blur' },
          { min: 6, max: 30, message: '密码6-30个字符', trigger: 'blur' },
          { validator: validatePassword, trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    submitForm (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          // console.log(this.registerForm)
          this.$axios.post('/register', this.registerForm)
            .then(res => {
              this.$message({
                message: '注册成功',
                type: 'success'
              })
            })
          this.$router.push('/login')
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
.register {
  background: url("../assets/bg.jpeg") no-repeat center center;
  background-size: cover;
  width: 100vw;
  height: 100vh;
  position: relative;

  .form-container {
    position: absolute;
    top: 10%;
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
      .register-form{
        margin-top: 30px;
        .el-form-item{
          width: 90%;
          label{
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            color: aliceblue;
            font-size: 18px;
          }
          .role-select{
            width: 100%;
          }
          .confirm-btn, .reset-btn{
            width: 48%;
          }
        }
      }
      .go-login{
        padding-bottom: 30px;
      }
    }
  }
}
</style>
