<template>
  <div>
    <TabMenu></TabMenu>
    <gibExample></gibExample>
  </div>
</template>

<script>
import Vue from 'vue'
import TabMenu from './TabMenu.vue'
import gibExample from './gib-example.vue'
import contact from './contact.vue'
Vue.component('TabMenu', TabMenu)
Vue.component('gibExample', gibExample)
Vue.component('contact', contact)
export default {
  name: 'home',
  data () {
    return {
      title: 'GIB layout'
    }
  },
  mounted: function () {
  }
}
</script>

<style scoped>

li {
  margin-left: auto;
}

/*  router-linkがaタグとして表示されてたのでスタイルをaタグに書いた*/
a {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  color: white;
  text-decoration: none;
  line-height: 50px;
}

div {
  margin-left: auto;
}

</style>
