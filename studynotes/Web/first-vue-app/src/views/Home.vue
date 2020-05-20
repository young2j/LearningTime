<template>
  <div class="home">
    <h1>这里是首页</h1>
  </div>
</template>

<script>
export default {
  name: 'home'
}
</script>

<style lang='less' scoped>
.home{
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.8);
  overflow: hidden;
  text-align: center;
  h1 {
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    color: aliceblue;
    font-size: 18px;
    margin: 50px auto;
    margin-bottom: 10px;
  }
}
</style>
