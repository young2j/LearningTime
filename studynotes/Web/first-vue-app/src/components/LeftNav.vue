<template>
  <el-row class="left-nav">
    <el-col >
      <el-menu
        default-active="2"
        class="el-menu-vertical"
        @open="handleOpen"
        @close="handleClose"
        background-color="#324057"
        text-color="#fff"
        active-text-color="#ffd04b">
        <router-link to='/home' tag='li'>
          <el-menu-item index='0'>
            <i class="el-icon-s-home"></i>
            <span slot="title">首页</span>
          </el-menu-item>
        </router-link>

        <template v-for="item in items">
          <el-submenu v-if='item.children' :index='item.path' :key='item.path'>
            <template slot='title'>
              <i :class="item.icon"></i>
              <span>{{item.name}}</span>
            </template>
            <router-link v-for='(child,index) in item.children' :to='child.path' :key='index' tag='li'>
              <el-menu-item :index='child.path'>
                <span slot='title'>{{child.name}}</span>
              </el-menu-item>
            </router-link>
          </el-submenu>
        </template>
      </el-menu>
    </el-col>
  </el-row>
</template>

<script>
export default {
  name: 'left-nav',
  data () {
    return {
      items: [
        {
          icon: 'el-icon-money',
          name: '资金管理',
          path: 'cash',
          children: [
            {
              path: 'cashflow',
              name: '资金流水'
            }
          ]
        },
        {
          icon: 'el-icon-info',
          name: '信息管理',
          path: 'info',
          children: [
            {
              path: 'profile',
              name: '个人信息'
            }
          ]
        }
      ]
    }
  },
  methods: {
    handleOpen (key, keyPath) {
      console.log(key, keyPath)
    },
    handleClose (key, keyPath) {
      console.log(key, keyPath)
    }
  }
}
</script>

<style lang='less' scoped>
.left-nav{
  height: 100vh;
  .el-menu-vertical{
    height: 100vh;
    border: none;
    .el-submenu{
      .el-menu-item{
        min-width: 120px;
      }
    }
  }
}
</style>
