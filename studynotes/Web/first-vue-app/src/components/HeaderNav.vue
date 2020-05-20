<template>
  <div class="header-nav">
    <el-row>
      <el-col :span="6" class="logo-container">
        <img src="../assets/logo.jpg" alt="logo" class='logo'>
        <span class='title'>资金管理系统</span>
      </el-col>
      <el-col :span="3" class="user">
        <div class="userinfo">
          <el-avatar :size="35" :src="user.avatar || circleUrl" class='avatar'></el-avatar>
          <div class="welcome">
            <p>欢迎</p>
            <el-dropdown @command="handleCommand">
              <span class="el-dropdown-link">
                {{user.username}}
                ysj
                <i class="el-icon-arrow-down el-icon--right"></i>
              </span>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command='profile'>个人信息</el-dropdown-item>
                <el-dropdown-item divided command='exit'>退出</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'header-nav',
  data () {
    return {
      circleUrl: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'
    }
  },
  computed: {
    user () {
      return this.$store.getters.user
    }
  },
  methods: {
    showProfile () {
      this.$router.push('/profile')
    },
    logout () {
      localStorage.removeItem('Token')
      this.$store.dispatch('clearState')
      this.$router.push('/login')
    },
    handleCommand (command) {
      switch (command) {
        case 'profile':
          this.showProfile()
          break
        case 'exit':
          this.logout()
          break
      }
    }
  }
}
</script>

<style lang='less' scoped>
.header-nav{
  width:100%;
  height: 50px;
  min-width: 600px;
  padding: 5px;
  background: #324057;
  color: #ffffff;
  border-bottom: 1px solid #1f2d3d;

  .logo-container{
    display: flex;
    .logo {
      width: 50px;
      height: 40px;
    }
    .title{
      align-self: center;
      padding-left: 10px;
    }
  }
  .user{
    float: right;
    .userinfo{
      display: flex;
      .welcome{
        align-self: center;
        padding-left: 10px;
        .el-dropdown-link {
          cursor: pointer;
          color: #409EFF;
          font-size: 16px;
        }
        .el-icon-arrow-down {
          font-size: 12px;
        }
      }
    }
  }
}
</style>
