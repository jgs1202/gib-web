<template>
  <div>
    <TabMenu></TabMenu>
    <br><br>
    <h3>This site is provided by <a href="http://www.viz.media.kyoto-u.ac.jp/" target="_blank">Koyamada lab.</a> at <a href="https://www.kyoto-u.ac.jp/" target="_blank">Kyoto university</a>.</h3><br>
    <h3>Site owner : &nbsp; Nozomi Aoyama &nbsp; &nbsp; aoyama.nozomi.37x@st.kyoto-u.ac.jp</h3>
  </div>
</template>

<script>
import Vue from 'vue'
import TabMenu from './TabMenu.vue'
import $ from 'jquery'
Vue.component('TabMenu', TabMenu)
let d3 = require('d3')
export default {
  name: 'contact',
  data () {
    return {
      current: null,
    }
  },
  mounted: function() {
    var that = this
    console.log('start')
  },
  methods: {
    click: function () {
    },
  }
}
</script>

<style scoped>
</style>
