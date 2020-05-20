<template>
  <div class='index'>
    <HeaderNav></HeaderNav>
    <el-row type='flex'>
      <el-col :span='4'>
        <LeftNav></LeftNav>
      </el-col>
      <el-col>
        <router-view></router-view>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import HeaderNav from '../components/HeaderNav.vue'
import LeftNav from '../components/LeftNav.vue'

export default {
  name: 'index',
  components: {
    HeaderNav: HeaderNav,
    LeftNav: LeftNav
  }
}
</script>

<style>
.index{
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}
</style>
