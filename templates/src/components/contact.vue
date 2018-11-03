<template>
  <div>
    <TabMenu></TabMenu>
    <br><br>
    <h3>This site is provided by <a href="http://www.viz.media.kyoto-u.ac.jp/" target="_blank">Koyamada lab.</a> at <a href="https://www.kyoto-u.ac.jp/" target="_blank">Kyoto university</a>.</h3><br>
    <h3>Site owner : &nbsp; Nozomi Aoyama &nbsp; &nbsp; aoyama.nozomi.37x@st.kyoto-u.ac.jp</h3>
    <button v-on:click="download">Say Hi</button>
    <div id="container"></div>
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
    download: function(e){
      // var xmlHttpRequest = new XMLHttpRequest();
      // let json = null
      // xmlHttpRequest.onreadystatechange = function() {
      //   console.log(this.status)
      //   console.log(this.response)
      //   if( this.readyState == 4 && this.status == 200 ) {
      //     if( this.response ) {
      //       console.log(this.response)
      //       json = JSON.stringify(this.response, null, '\t')
      //       console.log(json)
      //       let blob = new Blob([json], {type: 'application/json'})
      //       let url = window.URL.createObjectURL(blob)
      //       let a = document.createElement('a')
      //       // a.target = '_blank'
      //       a.download = 'sample_data.json'
      //       // a.textContent = 'download sample_data.json'
      //       if (window.navigator.msSaveBlob) {
      //         // for IE
      //         window.navigator.msSaveBlob(blob, name)
      //       }
      //       else if (window.URL && window.URL.createObjectURL) {
      //         // for Firefox
      //         a.href = window.URL.createObjectURL(blob);
      //         document.body.appendChild(a);
      //         a.click();
      //         document.body.removeChild(a);
      //       }
      //       else if (window.webkitURL && window.webkitURL.createObject) {
      //         // for Chrome 
      //         a.href = window.webkitURL.createObjectURL(blob);
      //         a.click();
      //       }
      //     }
      //   }
      // }
      // xmlHttpRequest.open('GET', 'http://35.233.171.147/image/sample_data.json', true);
      // // xmlHttpRequest.setRequestHeader('Access-Control-Allow-Headers', '*');
      // // xmlHttpRequest.setRequestHeader('Content-type', 'application/json');
      // // xmlHttpRequest.setRequestHeader('Access-Control-Allow-Origin', '*');
      // xmlHttpRequest.responseType = 'json';
      // xmlHttpRequest.send( null );

      d3.json('../image/sample_data.json', function(error, root){
        console.log(error, root)
      })


      // var obj = json //{a: 123, b: "4 5 6"};
      // var data = "text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(obj));

      // $('<a href="data:' + data + '" download="data.json">download JSON</a>').appendTo('#container')
    }
  }
}
</script>

<style scoped>
</style>
