<template>
  <div class="profile">
    <el-row type="flex" class="row-bg" justify="center" align="middle">
      <el-col :span="6" :push="2" class='profile-left'>
        <div class="useravatar">
          <el-avatar :src='user.avatar || circleUrl' :size='80'></el-avatar>
        </div>
      </el-col>
      <el-col :span="18" :push="2" class='profile-right'>
        <div class="userinfo">
          <div class='username'>
            <i class="el-icon-user-solid"/><span>{{ user.username || 'ysj' }}</span>
          </div>
          <div class="userrole">
            <i class="el-icon-setting"/><span>{{ user.role || '普通用户' }}</span>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  data () {
    return {
      circleUrl: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'
    }
  },
  computed: {
    user () {
      return this.$store.getters.user
    }
  }
}
</script>

<style lang='less' scoped>
.profile{
  .profile-left{
    background: #ffffff;
    height: 100vh;
    position: relative;
    .useravatar{
      position: absolute;
      top:28%;
      left: 20%;
    }
  }
  .profile-right{
    background: #dedede;
    height: 100vh;
    position: relative;
    .userinfo{
      position: absolute;
      top:30%;
      left: 5%;
      .username,.userrole{
        margin-bottom: 20px;
        span {
          margin-left: 10px;
        }
      }
    }
  }
}

</style>
