<template>
  <div id="app">
    <!-- <img src="./assets/logo.png"> -->
    <router-view/>
  </div>
</template>

<script>
// import Vue from 'vue'
export default {
  name: 'App'
}
</script>

<style>
body{
  margin-top: 4%
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 95%;
  width: 95%;
  margin: auto;
}
</style>
