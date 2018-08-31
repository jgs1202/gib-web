<template>
  <div>
    <TabMenu></TabMenu>
    <div>
      <!-- <link rel="stylesheet" href="http://104.196.232.59/css/introjs.css" crossorigin='anonymous'> -->
      <el-container class='bottom'>
        <el-aside width='20%'>
          <br><br>
            <span v-intro="'Upload a file of graph. <br>The current file is shown here.'" v-intro-step="1" class='choose'>
              <label for="fileid" class='square_btn'>
                Choose file
                <form name='form' class='fileup' style='display:none;'>
                  <input name="file" id='fileid'>
                </form>
              </label>
              <br><br>
              current file: {{current}}
            </span><br><br>
            <span v-intro="'Choose a proper layout.'" v-intro-step="2" class='buttons'>
              <el-radio-group>
                <el-radio label="ST-GIB" border size='medium' class='layoutButton'></el-radio>
                <el-radio label="CD-GIB" border size='medium' class='layoutButton'></el-radio>
              </el-radio-group>
              <el-radio-group>
                <el-radio label="FD-GIB" border size='medium' class='layoutButton'></el-radio>
                <el-radio label="TR-GiB" border size='medium' class='layoutButton'></el-radio>
              </el-radio-group>
            </span><br><br>
            <div v-intro="'Push and send me the file.'" v-intro-step="3" class='sendFile'>
              <el-button id='send' type="success">Send file
              </el-button><br>
          </div>
        </el-aside>
        <el-main>
          <div class="svg-container" :style="{width: settings.width + '%'}">
            <svg id="svg" pointer-events="all" viewBox="0 0 960 600" preserveAspectRatio="xMinYMin meet" v-intro="'The graph is shown here. <br>You can download the graph by right click.<br>You can analyze the data by click.'" v-intro-step="4">
              <!-- <g id="nodes">{{nodes}}</g>
              <g id="links">{{links}}</g>
              <g id='boxes'>{{boxes}}</g> -->
            </svg>
          </div>
        </el-main>
      </el-container>
      <br><br>
      <span v-intro="'The graph is shown here. <br>You can download the graph by right click.<br>You can analyze the data by click.'" v-intro-step="5" class='sampleData'>
        <label for="down_sample" class='square_btn'>
          <h3>Download Sample Data</h3>
          <form class='download_sample' style='display:none;'>
            <input type="button" id='sample_data'>
          </form>
        </label>
      </span>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import TabMenu from './TabMenu.vue'
import upload from './upload.vue'
import VueIntro from 'vue-introjs'
Vue.use(VueIntro)
Vue.component('TabMenu', TabMenu)
Vue.component('upload', upload)
import './introjs.css'
export default {
  name: 'try',
  data () {
    return {
      settings: {
        strokeColor: '#29B5FF',
        width: 100,
        svgWigth: 960,
        svgHeight: 600
      },
      current: null
    }
  },
  mounted: function() {
    console.log('start')
    // introJs().start()
    // console.log($intro())
    this.$intro().start(); // start the guide
    this.$intro().showHints(); // show hints
  },
  methods: {
    click: function () {
      // console.log($intro())
    this.$intro().start(); // start the guide
    this.$intro().showHints(); // show hints
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
      xmlHttpRequest.open( 'GET', 'http://104.196.232.59/image/sample_data.json', true);
      xmlHttpRequest.responseType = 'json';
      xmlHttpRequest.send( null );
    }
}
</script>

<style scoped>
body {
  margin: auto;
  margin-top: 10%;
  width: 100%;
  height: 100%;
  font-family: 'Century Gothic';
}

.app {
  margin: auto;
  width: 95%;
  height: 95%;
}

.controls {
  text-align: center;
  width: 80%;
  margin: auto;
  padding-bottom: 2rem;
  margin-top: 2rem;
  /* margin: auto; */
  background: #f8f8f8;
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
}

.sync {
  background: black;
  height: 60px;
  width: 60px;
  position: absolute;
  right: 0;
  bottom: 0;
}

.text {
  width: 80%;
  margin: auto;
  text-align: center;
  margin-top: 20%;
  font-size: 1.3rem;
}

.el-aside {
  /* border: 1px solid #67C23A; */
  box-shadow: 1px 2px 4px rgba(0, 0, 0, .5);
  text-align: center;
}

.el-main {
  box-shadow: 1px 2px 4px rgba(0, 0, 0, .5);
  text-align: center;
}

.svg-container {
  margin: auto;
  display: table;
  border: 0px solid #f8f8f8;
  /* box-shadow: 1px 2px 4px rgba(0, 0, 0, .5); */
}

.controls>*+* {
  margin-top: 1rem;
}

.links line {
  stroke: #999;
  stroke-opacity: 1;
}

.square_btn {
    position: relative;
    display: inline-block;
    padding: 0.25em 0.5em;
    text-decoration: none;
    color: #FFF;
    background: skyblue;/*背景色*/
    /*background: skyblue;*/
    /*border-bottom: solid 2px blue;/*少し濃い目の色に*/
    border-radius: 4px;/*角の丸み*/
    box-shadow: inset 0 2px 0 rgba(255,255,255,0.2), 0 2px 2px rgba(0, 0, 0, 0.19);
}

.square_btn:active {
    /*border-bottom: solid 2px #skyblue;*/
    opacity: 0.6;
    box-shadow: 0 0 2px rgba(0, 0, 0, 0.30);
}

.layoutButton {
  width: 45%;
}

.el-container { 
  position: relative;
}

.el-header, .el-footer {
    /*background-color: #B3C0D1;*/
    color: #333;
    text-align: center;
    line-height: 60px;
    height: 30%;
  }

.bottom {
  padding-top: 3%; 
}

.buttons {
  padding-bottom: 5%;
  padding-top: 5%;
  margin-bottom: 5%;
  margin-top: 5%;
}

.sendFile {
  padding-bottom: 5%;
  padding-top: 5%;
  margin-bottom: 5%;
  margin-top: 5%;
}

.choose {
  padding-bottom: 5%;
  padding-top: 5%;
  margin-bottom: 5%;
  margin-top: 5%;
}

#sample_data {
  padding: 4%;
}
</style>
