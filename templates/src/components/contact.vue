<template>
  <div>
    <TabMenu></TabMenu>
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
  },
    sampleData: function() {
      var xmlHttpRequest = new XMLHttpRequest();
      xmlHttpRequest.onreadystatechange = function() {
        if( this.readyState == 4 && this.status == 200 ) {
          if( this.response ) {
            console.log(this.response)
            let json = JSON.stringify(this.response, null, '\t')
            console.log(json)
            let blob = new Blob([json], {type: 'application/json'})
            let url = window.URL.createObjectURL(blob)
            let a = document.createElement('a')
            // a.target = '_blank'
            a.download = 'sample_data.json'
            // a.textContent = 'download sample_data.json'
            if (window.navigator.msSaveBlob) {
              // for IE
              window.navigator.msSaveBlob(blob, name)
            }
            else if (window.URL && window.URL.createObjectURL) {
              // for Firefox
              a.href = window.URL.createObjectURL(blob);
              document.body.appendChild(a);
              a.click();
              document.body.removeChild(a);
            }
            else if (window.webkitURL && window.webkitURL.createObject) {
              // for Chrome
              a.href = window.webkitURL.createObjectURL(blob);
              a.click();
            }
          }
        }
      }
      xmlHttpRequest.open( 'GET', 'http://35.200.124.149/image/sample_data.json', true);
      xmlHttpRequest.responseType = 'json';
      xmlHttpRequest.send( null );
    }
}
</script>

<style scoped>
</style>
