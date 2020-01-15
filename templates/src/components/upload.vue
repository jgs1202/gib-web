<template>
  <div class="app">
    <el-container class='bottom'>
      <el-aside width='20%'>
        <br><br>
        <label for="fileid" class='square_btn'>
          Choose file
          <form name='form' class='fileup' style='display:none;'>
            <input type="file" name="file" id='fileid'>
          </form>
        </label>
        <br><br>
        current file: {{current}}
        <br><br>
        <span>
          <el-radio-group v-model="layout">
            <el-radio label="ST-GIB" border size='medium' class='layoutButton'></el-radio>
            <el-radio label="CD-GIB" border size='medium' class='layoutButton'></el-radio><br>
            <el-radio label="FD-GIB" border size='medium' class='layoutButton'></el-radio>
            <el-radio label="TR-GIB" border size='medium' class='layoutButton'></el-radio>
          </el-radio-group>
          <br><br>
        </span>
        <div>
          <el-button id='send' type="success" v-on:click='sendData'>{{status}}
          </el-button><br>
          {{message}}
        </div>
        <div><br>
          Current Node data:<br><br>
          Name &nbsp;: {{nodeData.name}}<br>
          Group : {{nodeData.group}}<br>
        </div>
        <br><br>
        <label for="reset" class='square_btn'>
          Reset zoom
          <input type="button" name="reset" id='reset' style='display:none' v-on:click='resetted'>
        </label>
      </el-aside>
      <el-main>
        <div class="svg-container" :style="{width: settings.width + '%'}">
          <svg id="svg" pointer-events="all" viewBox="0 0 960 600" preserveAspectRatio="xMinYMin meet">
            <g id="nodes">{{nodes}}</g>
            <g id="links">{{links}}</g>
            <g id='boxes'>{{boxes}}</g>
          </svg>
        </div>
      </el-main>
    </el-container>
    <br><br>
    <label for="down_sample" class='square_btn'>
        <h3>Download Sample Data</h3>
      <form name='sampleData' class='sampleData' style='display:none;'>
        <input type="button" name="down_sample" id='down_sample' v-on:click='sampleData'>
      </form>
    </label>
    <label for="json_file" class='square_btn' style="margin-left: 5rem">
          <h3>Download json file</h3>
          <input type="button" name="json_file" id='json_file' style='display:none' v-on:click='get_json'>
    </label>
  </div>
</template>

<script>
import $ from 'jquery'
const swal = require('sweetalert')
const d3 = require('d3')
const downloadable = require('d3-downloadable')
export default {
  name: 'upload',
  data: function () {
    return {
      graph: null,
      gib: null,
      layout: 'ST-GIB',
      simulation: null,
      settings: {
        strokeColor: '#29B5FF',
        width: 100,
        svgWigth: 960,
        svgHeight: 600
      },
      nodes: [],
      links: [],
      boxes: [],
      message: null,
      current: 'None',
      nodeData: {
        name: null,
        group: null,
      },
      status: 'Send File',
      normalSize: 2,
      relatedSize: 4,
      selectSize: 5,
      selectWidth: 2.5,
      selected: [],
      related: [],
      redLinks: [],
      groupColors: [],
      zoom: null
    }
  },
  mounted: function () {
    let that = this
    let form = document.forms.form
    // ファイルが読み込まれた時の処理
    form.file.addEventListener('change', that.load, false)
    that.zoom = d3.zoom()
      .scaleExtent([1 / 2, 12])
      .on('zoom', that.zoomed)
    d3.select('svg').call(that.zoom)
    d3.select('svg').call(downloadable.downloadable().filename('graph.png'))
    // console.log('downloadable')
  },
  methods: {
    zoomed: function() {
      var that = this
      d3.select('svg').attr('transform', d3.event.transform)
    },
    resetted: function() {
      var that = this
      d3.select('svg').transition()
        .duration(500)
        .call(that.zoom.transform, d3.zoomIdentity);
    },
    load: function (e) {
      let that = this
      let result = e.target.files[0]
      if (result.name.slice(-5) !== '.json') {
        swal('Only a json file is valid.')
      } else {
        let reader = new FileReader()
        reader.addEventListener('load', function () {
          that.graph = JSON.parse(reader.result)
        }, false)
        reader.readAsText(result)
      }
      that.current = result.name
    },
    sampleData: function() {
      d3.json('../image/sample_data.json').then(function(graph){
        let json = JSON.stringify(graph, null, '\t')
            // console.log(json)
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
      })
    },
    get_json: function() {
      d3.json('../image/gib.json').then(function(graph){
        let json = JSON.stringify(graph, null, '\t')
            // console.log(json)
            let blob = new Blob([json], {type: 'application/json'})
            let url = window.URL.createObjectURL(blob)
            let a = document.createElement('a')
            // a.target = '_blank'
            a.download = 'gib.json'
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
      })
    },
    sendData: function (e) {
      let that = this
      // console.log((that.graph))
      if (that.graph) {
        that.status = 'calculating...'
        let data = {}
        data.data = that.graph
        data.layout = that.layout
        // console.log(typeof JSON.stringify(data))
        $.ajax({
          // url: 'http://35.233.171.147:80/upload',
          url: 'http://35.233.171.147/upload',
          type: 'POST',
          data: JSON.stringify(data),
          // dataType: 'json',
          // jsonpCallback: 'data',
          // dataType: 'text',
          contentType: 'application/json;charset=UTF-8',
          timeout: 10000000
        })
        .done(function(res) {
          that.message = null
          that.gib = res
          that.restart()
          that.status = 'Send File'
          that.related = []
          for (let i=0; i < that.gib.nodes.length; i++){
            that.related.push([])
          }
          that.redLinks = []
          for (let i=0; i < that.gib.links.length; i++){
            that.redLinks.push([])
          }
        })
        .fail(function(XMLHttpRequest, textStatus, errorThrown) {
          that.status = 'Send File'
          swal('An error occurred! Please send us a message from the contact.')
        })
      }
    },
    restart: function() {
      var that = this
      that.groupColors = []
      for (let i=0; i<parseInt(that.gib.groups.length); i++) {
        that.groupColors.push(d3.interpolateRainbow(i / that.gib.groups.length))
      }
      that.gib.groups.pop()
      that.$set(that.boxes, that.reBoxes())
      that.$set(that.links, that.reLinks())
      that.$set(that.nodes, that.reNodes())
    },
    reNodes: function() {
      var that = this;
      if (that.gib) {
        d3.selectAll('circle').remove()
        d3.select("svg").append("g")
          .attr("class", "nodes")
          .selectAll("circle")
          .data(that.gib.nodes)
          .enter().append("circle")
          .attr('cx', that.settings.svgWigth / 2)
          .attr('cy', that.settings.svgHeight / 2)
          .attr("r", 3)
        return d3.selectAll("circle")
          .each(function(d, i) {
            var selection = d3.select(this)
            selection.transition()
              .attr('cx', that.gib.nodes[i].cx)
              .attr("cy", that.gib.nodes[i].cy)
              .attr("fill", function(d, i) {
                // return that.color(d.group / that.gib.groups.length);
                return that.groupColors[parseInt(d.group)]
              })
            selection.on('mouseover', function(d, i){
              selection.attr('r', that.selectSize)
              let argvs = {}
              if (d.name) {
                that.nodeData.name = d.name
              } if (d.group) {
                that.nodeData.group = that.gib.groups[parseInt(d.group)].name
              }
            })
            selection.on('click', function(d, i){
              // console.log('click')
              that.selectNode(d, i)
            })
            selection.on('mouseout', function(d, i){
              that.nodeData.name = null
              that.nodeData.group = null
              if (($.inArray(d, that.selected) < 0) && (that.related[d.id].length === 0)){
                selection.attr('r', that.normalSize)
              } else if (($.inArray(d, that.selected) < 0) && (that.related[d.id].length !== 0)){
                selection.attr('r', that.relatedSize)
              }
            })
          })
	     }
    },
    reLinks: function() {
      var that = this;
      if (that.gib) {
        d3.selectAll('line').remove()
        d3.select("svg").append("g")
          .attr("class", "links")
          .selectAll("line")
          .data(that.gib.links)
          .enter().append("line")
          .attr('stroke', 'gray')
          .attr("stroke-width", function(d) {
            // return Math.sqrt(d.value);
            return 0.4;
          })
        d3.selectAll("line")
          .each(function(d, i) {
            var selection = d3.select(this)
            selection.attr('x1', function(d) {
                return that.gib.nodes[d.source].cx
              })
              .attr('y1', function(d) {
                return that.gib.nodes[d.source].cy
              })
              .attr('x2', function(d) {
                return that.gib.nodes[d.target].cx
              })
              .attr('y2', function(d) {
                return that.gib.nodes[d.target].cy
              })
          })
        d3.selection.prototype.moveToFront = function() {
          return this.each(function() {
            this.parentNode.parentNode.appendChild(this.parentNode);
          })
        }
        d3.select('circle').moveToFront()
        return d3.selectAll("line")
      }
    },
    reBoxes: function() {
      var that = this
      if (that.gib) {
        d3.selectAll('rect').remove()
      	d3.selectAll('text').remove()

        let x_margin = 5
        let y_margin = 12
        d3.select('svg').append('g')
          .attr('class', 'groupName')
          .selectAll('text')
          .data(that.gib.groups)
          .enter().append("text")
          .text(function(d, num) {
            return d.name
          })
          .attr('x', function(d, num) {
            return d.x + x_margin
          })
          .attr('y', function(d, num) {
            return d.y + y_margin
          })
          .attr("font-family", "sans-serif")
          .attr("font-size", "10px")
          .attr("fill", "black");

        d3.select("svg").append("g")
          .attr("class", "rect")
          .selectAll("rect")
          .data(that.gib.groups)
          .enter().append("rect")
          .attr("stroke", "black")
          .attr("stroke-width", 1)
          .attr("fill", 'transparent')

        return d3.selectAll('rect')
          .each(function(d, i) {
            if (d['dx'] !== that.settings.svgWigth || d['dy'] !== that.settings.svgHeight) {
              var selection = d3.select(this)
                .attr('index', i)
                .attr('x', d['x'])
                .attr('y', d['y'])
                .attr('width', d['dx'])
                .attr('height', d['dy'])
            }
          })
      }
		},
    selectNode: function(d, i){
      let that = this
      let preference = d.id
      let groupOfSelected = d.group
      let select_number = d.id
      if ($.inArray(d, that.selected) < 0){
        let relLinks = []
        let relNodes = []
        for (let i=0; i < that.gib.links.length; i++){
          if ((d.id === that.gib.links[i].source) || (d.id === that.gib.links[i].target)){
            relLinks.push(that.gib.links[i])
          }
        }
        for (let n=0; n < relLinks.length; n++){
          if (relLinks[n].source === d.id){
            relNodes.push(relLinks[n].target)
          } else if (relLinks[n].target === d.id){
            relNodes.push(relLinks[n].source)
          }
        }
        d3.selectAll("circle")
          .each(function(nd, ni) {
            var selection = d3.select(this)
            if (relLinks.length !== 0) {
              for (let n=0; n<relNodes.length; n++){
                if (nd.id == relNodes[n]) {
                  that.related[parseInt(relNodes[n])].push(select_number)
                  if ($.inArray(nd, that.selected) < 0){
                    selection.attr('r', that.relatedSize)
                  }
                }
                else if (nd.id === preference) {
                  selection.attr('r', that.selectSize)
                  selection.attr('stroke', 'yellow')
                  selection.attr('stroke-width', that.selectWidth)
                  if ($.inArray(nd, that.selected) < 0){
                    that.selected.push(nd)
                  }
                }
              }
            } else if (nd.id === preference) {
              selection.attr('r', that.selectSize)
              selection.attr('stroke', 'yellow')
              selection.attr('stroke-width', that.selectWidth)
              if ($.inArray(nd, that.selected) < 0){
                that.selected.push(nd)
              }
            }
          })
        d3.selectAll('line')
          .each(function(ld, li){
            let selection = d3.select(this)
            for (let n=0; n<relLinks.length; n++){
              if (relLinks[n].id === ld.id){
                that.redLinks[parseInt(ld.id)].push(parseInt(select_number))
                selection.attr('stroke', that.groupColors[groupOfSelected])
                selection.attr('stroke-width', 1.5)
                if (that.selected.indexOf(that.gib.nodes[ld.source]) >= 0) {
                  if (that.selected.indexOf(that.gib.nodes[ld.target]) >= 0) {
                    selection.attr('stroke', d3.rgb(255, 135, 180))
                    selection.attr('stroke-width', 3)

                  }
                }
              }
            }
        })
      } else {
        let rmList = []
        for (let n=0; n<that.selected.length; n++){
          if (that.selected[n].id === preference){
            let front = that.selected.slice(0, n)
            let back = that.selected.slice(n+1, that.selected.length)
            that.selected = front.concat(back)
          }
        }
        d3.selectAll("circle")
          .each(function(nd, ni) {
            var selection = d3.select(this)
            if (nd.id === select_number){
              selection.attr('r', that.normalSize)
              selection.attr('stroke-width', 0)
            } else {
              for(let n=0; n < that.related.length; n++){
                let order = $.inArray(select_number, that.related[n])
                if (order > -1){
                  let front = that.related[n].slice(0, order)
                  let back = that.related[n].slice(order+1, that.related[n].length)
                  that.related[n] = front.concat(back)
                  if ((that.related[n].length === 0) && ($.inArray(that.gib.nodes[n], that.selected) < 0)){
                    rmList.push(n)
                  }
                }
              }
            }
          })
        d3.selectAll("circle")
          .each(function(nd, ni) {
            var selection = d3.select(this)
            if ($.inArray(nd.id, rmList) > -1){
              selection.attr('r', that.normalSize)
            }
        })
        // reomve red links
        for (let n=0; n<that.redLinks.length; n++){
          let order = $.inArray(parseInt(select_number), that.redLinks[n])
          if (order > -1) {
            let front = that.redLinks[n].slice(0, order)
            let back = that.redLinks[n].slice(order + 1, that.redLinks[n].length)
            that.redLinks[n] = front.concat(back)
          }
        }
        d3.selectAll('line').each(function(ld, li) {
          let selection = d3.select(this)
          if (that.redLinks[parseInt(ld.id)].length === 0){
            selection.attr('stroke', 'gray')
            selection.attr('stroke-width', 0.4)
          } else if (that.redLinks[parseInt(ld.id)].length === 1) {
            selection.attr('stroke', that.groupColors[that.gib.nodes[that.redLinks[parseInt(ld.id)]].group])
            selection.attr('stroke-width', 1.5)
          }
        })
      }
    }
  }
}
</script>

<style>

.controls {
  text-align: center;
  width: 95%;
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
  font-size: 1.5vw;
}

.el-main {
  box-shadow: 1px 2px 4px rgba(0, 0, 0, .5);
  text-align: center;
}

.svg-container {
  margin-left: auto;
  margin-right: auto;
  display: table;
  border: 0px solid #f8f8f8;
  /* box-shadow: 1px 2px 4px rgba(0, 0, 0, .5); */
}

.controls>*+* {
  margin-top: 1rem;
}
.links line {
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
</style>