<template>
  <div>
    <TabMenu></TabMenu>
    <upload></upload>
  </div>
</template>

<script>
import Vue from 'vue'
import TabMenu from './TabMenu.vue'
import upload from './upload.vue'
Vue.component('TabMenu', TabMenu)
Vue.component('upload', upload)
export default {
  name: 'try',
  data () {
    return {
    }
  },
  mounted: function () {
  }
}
</script>

<style scoped>

</style>
