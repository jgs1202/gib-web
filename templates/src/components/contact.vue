<template>
  <div>
    <TabMenu></TabMenu>
    <br><br>
    <h3>This site is provided by Koyamada lab. at <a href="https://www.kyoto-u.ac.jp/en/">Kyoto university</a>.</h3><br>
    <h3>Site owner : &nbsp; Nozomi Aoyama &nbsp; &nbsp; aoyama.nozomi.37x@st.kyoto-u.ac.jp</h3>
  </div>
</template>

<script>
import Vue from 'vue'
import TabMenu from './TabMenu.vue'
Vue.component('TabMenu', TabMenu)
export default {
  name: 'contact',
  data () {
    return {
      current: null,
    }
  },
  mounted: function() {
    console.log('start')
  },
  methods: {
    click: function () {
    }
  }
}
</script>

<style scoped>
</style>
