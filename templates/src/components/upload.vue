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

<script type="text/javascript" src="./d3-ForceEdgeBundling.js"></script>
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
        svgHeight: 600,
        margin: {
          top: 2,
          right: 2,
          bottom: 2,
          left: 2
        }
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
      normalSize: 3,
      relatedSize: 4.5,
      selectSize: 5,
      selectWidth: 2,
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
    d3.select("svg")
      // .attr("width", that.settings.svgWigth)
      // .attr("height", that.settings.svgHeight)
      .call(that.zoom)
      .append("g")
      .attr("transform", "translate(" + that.settings.margin.left + "," + that.settings.margin.top + ")");

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
      // that.$set(that.links, that.reLinks())
      that.reLinks()
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
          .attr("r", that.normalSize)
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
        // d3.select("svg").append("g")
        //   .attr("class", "links")
        //   .selectAll("line")
        //   .data(that.gib.links)
        //   .enter().append("line")
        //   .attr('stroke', 'gray')
        //   .attr("stroke-width", function(d) {
        //     // return Math.sqrt(d.value);
        //     return 0.4;
        //   })
        // d3.selectAll("line")
        //   .each(function(d, i) {
        //     var selection = d3.select(this)
        //     selection.attr('x1', function(d) {
        //         return that.gib.nodes[d.source].cx
        //       })
        //       .attr('y1', function(d) {
        //         return that.gib.nodes[d.source].cy
        //       })
        //       .attr('x2', function(d) {
        //         return that.gib.nodes[d.target].cx
        //       })
        //       .attr('y2', function(d) {
        //         return that.gib.nodes[d.target].cy
        //       })
        //   })


        //ここから
        let node_data = {}
        for (let i=0; i<that.gib.nodes.length; i++) {
          node_data["" + that.gib.nodes[i].id] = {}
          node_data["" + that.gib.nodes[i].id]["x"] = that.gib.nodes[i].cx
          node_data["" + that.gib.nodes[i].id]["y"] = that.gib.nodes[i].cy
        }
        console.log('bundling...')
        let edge_data = that.gib.links
        let fbundling = that.ForceEdgeBundling()
          .nodes(node_data)
          .edges(edge_data)
          .step_size(0.4)
          .compatibility_threshold(0.7)
        var results = fbundling();
        // var fbundling = that.ForceEdgeBundling()
        //   .step_size(0.2)
        //   .compatibility_threshold(0.9)
        //   .nodes(node_data)
        //   .edges(edge_data);
        // var results = fbundling();

        var d3line = d3.line()
          // .curve(d3.curvelinear)
          .x(function(d){ return d.x; })
          .y(function(d){ return d.y; })
        results.forEach(function(edge_subpoint_data){
        // for each of the arrays in the results
        // draw a line between the subdivions points for that edge

          d3.select("svg")
              .append("path")
              .attr("d", d3line(edge_subpoint_data))
              .style("stroke-width", 1)
              .style("stroke", "#ff2222")
              .style("fill", "none")
              .style('stroke-opacity',0.15);
        })

        d3.selection.prototype.moveToFront = function() {
          return this.each(function() {
            this.parentNode.parentNode.appendChild(this.parentNode);
          })
        }
        d3.select('circle').moveToFront()
        console.log('bundle end')
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
    },
    ForceEdgeBundling: function() {
      var data_nodes = {}, // {'nodeid':{'x':,'y':},..}
            data_edges = [], // [{'source':'nodeid1', 'target':'nodeid2'},..]
            compatibility_list_for_edge = [],
            subdivision_points_for_edge = [],
            K = 0.1, // global bundling constant controlling edge stiffness
            S_initial = 0.1, // init. distance to move points
            P_initial = 1, // init. subdivision number
            P_rate = 2, // subdivision rate increase
            C = 6, // number of cycles to perform
            I_initial = 90, // init. number of iterations for cycle
            I_rate = 0.6666667, // rate at which iteration number decreases i.e. 2/3
            compatibility_threshold = 0.6,
            eps = 1e-6;


        /*** Geometry Helper Methods ***/
        function vector_dot_product(p, q) {
            return p.x * q.x + p.y * q.y;
        }

        function edge_as_vector(P) {
            return {
                'x': data_nodes[P.target].x - data_nodes[P.source].x,
                'y': data_nodes[P.target].y - data_nodes[P.source].y
            }
        }

        function edge_length(e) {
            // handling nodes that are on the same location, so that K/edge_length != Inf
            if (Math.abs(data_nodes[e.source].x - data_nodes[e.target].x) < eps &&
                Math.abs(data_nodes[e.source].y - data_nodes[e.target].y) < eps) {
                return eps;
            }

            return Math.sqrt(Math.pow(data_nodes[e.source].x - data_nodes[e.target].x, 2) +
                Math.pow(data_nodes[e.source].y - data_nodes[e.target].y, 2));
        }

        function custom_edge_length(e) {
            return Math.sqrt(Math.pow(e.source.x - e.target.x, 2) + Math.pow(e.source.y - e.target.y, 2));
        }

        function edge_midpoint(e) {
            var middle_x = (data_nodes[e.source].x + data_nodes[e.target].x) / 2.0;
            var middle_y = (data_nodes[e.source].y + data_nodes[e.target].y) / 2.0;

            return {
                'x': middle_x,
                'y': middle_y
            };
        }

        function compute_divided_edge_length(e_idx) {
            var length = 0;
            for (var i = 1; i < subdivision_points_for_edge[e_idx].length; i++) {
                var segment_length = euclidean_distance(subdivision_points_for_edge[e_idx][i], subdivision_points_for_edge[e_idx][i - 1]);
                length += segment_length;
            }

            return length;
        }

        function euclidean_distance(p, q) {
            return Math.sqrt(Math.pow(p.x - q.x, 2) + Math.pow(p.y - q.y, 2));
        }

        function project_point_on_line(p, Q) {
            var L = Math.sqrt((Q.target.x - Q.source.x) * (Q.target.x - Q.source.x) + (Q.target.y - Q.source.y) * (Q.target.y - Q.source.y));
            var r = ((Q.source.y - p.y) * (Q.source.y - Q.target.y) - (Q.source.x - p.x) * (Q.target.x - Q.source.x)) / (L * L);

            return {
                'x': (Q.source.x + r * (Q.target.x - Q.source.x)),
                'y': (Q.source.y + r * (Q.target.y - Q.source.y))
            };
        }

        /*** ********************** ***/

        /*** Initialization Methods ***/
        function initialize_edge_subdivisions() {
            for (var i = 0; i < data_edges.length; i++) {
                if (P_initial === 1) {
                    subdivision_points_for_edge[i] = []; //0 subdivisions
                } else {
                    subdivision_points_for_edge[i] = [];
                    subdivision_points_for_edge[i].push(data_nodes[data_edges[i].source]);
                    subdivision_points_for_edge[i].push(data_nodes[data_edges[i].target]);
                }
            }
        }

        function initialize_compatibility_lists() {
            for (var i = 0; i < data_edges.length; i++) {
                compatibility_list_for_edge[i] = []; //0 compatible edges.
            }
        }

        function filter_self_loops(edgelist) {
            var filtered_edge_list = [];

            for (var e = 0; e < edgelist.length; e++) {
                if (data_nodes[edgelist[e].source].x != data_nodes[edgelist[e].target].x ||
                    data_nodes[edgelist[e].source].y != data_nodes[edgelist[e].target].y) { //or smaller than eps
                    filtered_edge_list.push(edgelist[e]);
                }
            }

            return filtered_edge_list;
        }

        /*** ********************** ***/

        /*** Force Calculation Methods ***/
        function apply_spring_force(e_idx, i, kP) {
            var prev = subdivision_points_for_edge[e_idx][i - 1];
            var next = subdivision_points_for_edge[e_idx][i + 1];
            var crnt = subdivision_points_for_edge[e_idx][i];
            var x = prev.x - crnt.x + next.x - crnt.x;
            var y = prev.y - crnt.y + next.y - crnt.y;

            x *= kP;
            y *= kP;

            return {
                'x': x,
                'y': y
            };
        }

        function apply_electrostatic_force(e_idx, i) {
            var sum_of_forces = {
                'x': 0,
                'y': 0
            };
            var compatible_edges_list = compatibility_list_for_edge[e_idx];

            for (var oe = 0; oe < compatible_edges_list.length; oe++) {
                var force = {
                    'x': subdivision_points_for_edge[compatible_edges_list[oe]][i].x - subdivision_points_for_edge[e_idx][i].x,
                    'y': subdivision_points_for_edge[compatible_edges_list[oe]][i].y - subdivision_points_for_edge[e_idx][i].y
                };

                if ((Math.abs(force.x) > eps) || (Math.abs(force.y) > eps)) {
                    var diff = (1 / Math.pow(custom_edge_length({
                        'source': subdivision_points_for_edge[compatible_edges_list[oe]][i],
                        'target': subdivision_points_for_edge[e_idx][i]
                    }), 1));

                    sum_of_forces.x += force.x * diff;
                    sum_of_forces.y += force.y * diff;
                }
            }

            return sum_of_forces;
        }


        function apply_resulting_forces_on_subdivision_points(e_idx, P, S) {
            var kP = K / (edge_length(data_edges[e_idx]) * (P + 1)); // kP=K/|P|(number of segments), where |P| is the initial length of edge P.
            // (length * (num of sub division pts - 1))
            var resulting_forces_for_subdivision_points = [{
                'x': 0,
                'y': 0
            }];

            for (var i = 1; i < P + 1; i++) { // exclude initial end points of the edge 0 and P+1
                var resulting_force = {
                    'x': 0,
                    'y': 0
                };
                let spring_force = apply_spring_force(e_idx, i, kP);
                let electrostatic_force = apply_electrostatic_force(e_idx, i, S);

                resulting_force.x = S * (spring_force.x + electrostatic_force.x);
                resulting_force.y = S * (spring_force.y + electrostatic_force.y);

                resulting_forces_for_subdivision_points.push(resulting_force);
            }

            resulting_forces_for_subdivision_points.push({
                'x': 0,
                'y': 0
            });

            return resulting_forces_for_subdivision_points;
        }

        /*** ********************** ***/

        /*** Edge Division Calculation Methods ***/
        function update_edge_divisions(P) {
            for (var e_idx = 0; e_idx < data_edges.length; e_idx++) {
                if (P === 1) {
                    subdivision_points_for_edge[e_idx].push(data_nodes[data_edges[e_idx].source]); // source
                    subdivision_points_for_edge[e_idx].push(edge_midpoint(data_edges[e_idx])); // mid point
                    subdivision_points_for_edge[e_idx].push(data_nodes[data_edges[e_idx].target]); // target
                } else {
                    var divided_edge_length = compute_divided_edge_length(e_idx);
                    var segment_length = divided_edge_length / (P + 1);
                    var current_segment_length = segment_length;
                    var new_subdivision_points = [];
                    new_subdivision_points.push(data_nodes[data_edges[e_idx].source]); //source

                    for (var i = 1; i < subdivision_points_for_edge[e_idx].length; i++) {
                        var old_segment_length = euclidean_distance(subdivision_points_for_edge[e_idx][i], subdivision_points_for_edge[e_idx][i - 1]);

                        while (old_segment_length > current_segment_length) {
                            var percent_position = current_segment_length / old_segment_length;
                            var new_subdivision_point_x = subdivision_points_for_edge[e_idx][i - 1].x;
                            var new_subdivision_point_y = subdivision_points_for_edge[e_idx][i - 1].y;

                            new_subdivision_point_x += percent_position * (subdivision_points_for_edge[e_idx][i].x - subdivision_points_for_edge[e_idx][i - 1].x);
                            new_subdivision_point_y += percent_position * (subdivision_points_for_edge[e_idx][i].y - subdivision_points_for_edge[e_idx][i - 1].y);
                            new_subdivision_points.push({
                                'x': new_subdivision_point_x,
                                'y': new_subdivision_point_y
                            });

                            old_segment_length -= current_segment_length;
                            current_segment_length = segment_length;
                        }
                        current_segment_length -= old_segment_length;
                    }
                    new_subdivision_points.push(data_nodes[data_edges[e_idx].target]); //target
                    subdivision_points_for_edge[e_idx] = new_subdivision_points;
                }
            }
        }

        /*** ********************** ***/

        /*** Edge compatibility measures ***/
        function angle_compatibility(P, Q) {
            return Math.abs(vector_dot_product(edge_as_vector(P), edge_as_vector(Q)) / (edge_length(P) * edge_length(Q)));
        }

        function scale_compatibility(P, Q) {
            var lavg = (edge_length(P) + edge_length(Q)) / 2.0;
            return 2.0 / (lavg / Math.min(edge_length(P), edge_length(Q)) + Math.max(edge_length(P), edge_length(Q)) / lavg);
        }

        function position_compatibility(P, Q) {
            var lavg = (edge_length(P) + edge_length(Q)) / 2.0;
            var midP = {
                'x': (data_nodes[P.source].x + data_nodes[P.target].x) / 2.0,
                'y': (data_nodes[P.source].y + data_nodes[P.target].y) / 2.0
            };
            var midQ = {
                'x': (data_nodes[Q.source].x + data_nodes[Q.target].x) / 2.0,
                'y': (data_nodes[Q.source].y + data_nodes[Q.target].y) / 2.0
            };

            return lavg / (lavg + euclidean_distance(midP, midQ));
        }

        function edge_visibility(P, Q) {
            var I0 = project_point_on_line(data_nodes[Q.source], {
                'source': data_nodes[P.source],
                'target': data_nodes[P.target]
            });
            var I1 = project_point_on_line(data_nodes[Q.target], {
                'source': data_nodes[P.source],
                'target': data_nodes[P.target]
            }); //send actual edge points positions
            var midI = {
                'x': (I0.x + I1.x) / 2.0,
                'y': (I0.y + I1.y) / 2.0
            };
            var midP = {
                'x': (data_nodes[P.source].x + data_nodes[P.target].x) / 2.0,
                'y': (data_nodes[P.source].y + data_nodes[P.target].y) / 2.0
            };

            return Math.max(0, 1 - 2 * euclidean_distance(midP, midI) / euclidean_distance(I0, I1));
        }

        function visibility_compatibility(P, Q) {
            return Math.min(edge_visibility(P, Q), edge_visibility(Q, P));
        }

        function compatibility_score(P, Q) {
            return (angle_compatibility(P, Q) * scale_compatibility(P, Q) * position_compatibility(P, Q) * visibility_compatibility(P, Q));
        }

        function are_compatible(P, Q) {
            return (compatibility_score(P, Q) >= compatibility_threshold);
        }

        function compute_compatibility_lists() {
            for (var e = 0; e < data_edges.length - 1; e++) {
                for (var oe = e + 1; oe < data_edges.length; oe++) { // don't want any duplicates
                    if (are_compatible(data_edges[e], data_edges[oe])) {
                        compatibility_list_for_edge[e].push(oe);
                        compatibility_list_for_edge[oe].push(e);
                    }
                }
            }
        }

        /*** ************************ ***/

        /*** Main Bundling Loop Methods ***/
        var forcebundle = function () {
            var S = S_initial;
            var I = I_initial;
            var P = P_initial;

            initialize_edge_subdivisions();
            initialize_compatibility_lists();
            update_edge_divisions(P);
            compute_compatibility_lists();

            for (var cycle = 0; cycle < C; cycle++) {
                for (var iteration = 0; iteration < I; iteration++) {
                    var forces = [];
                    for (var edge = 0; edge < data_edges.length; edge++) {
                        forces[edge] = apply_resulting_forces_on_subdivision_points(edge, P, S);
                    }
                    for (var e = 0; e < data_edges.length; e++) {
                        for (var i = 0; i < P + 1; i++) {
                            subdivision_points_for_edge[e][i].x += forces[e][i].x;
                            subdivision_points_for_edge[e][i].y += forces[e][i].y;
                        }
                    }
                }
                // prepare for next cycle
                S = S / 2;
                P = P * P_rate;
                I = I_rate * I;

                update_edge_divisions(P);
                //console.log('C' + cycle);
                //console.log('P' + P);
                //console.log('S' + S);
            }
            return subdivision_points_for_edge;
        };
        /*** ************************ ***/


        /*** Getters/Setters Methods ***/
        forcebundle.nodes = function (nl) {
            if (arguments.length === 0) {
                return data_nodes;
            } else {
                data_nodes = nl;
            }

            return forcebundle;
        };

        forcebundle.edges = function (ll) {
            if (arguments.length === 0) {
                return data_edges;
            } else {
                data_edges = filter_self_loops(ll); //remove edges to from to the same point
            }

            return forcebundle;
        };

        forcebundle.bundling_stiffness = function (k) {
            if (arguments.length === 0) {
                return K;
            } else {
                K = k;
            }

            return forcebundle;
        };

        forcebundle.step_size = function (step) {
            if (arguments.length === 0) {
                return S_initial;
            } else {
                S_initial = step;
            }

            return forcebundle;
        };

        forcebundle.cycles = function (c) {
            if (arguments.length === 0) {
                return C;
            } else {
                C = c;
            }

            return forcebundle;
        };

        forcebundle.iterations = function (i) {
            if (arguments.length === 0) {
                return I_initial;
            } else {
                I_initial = i;
            }

            return forcebundle;
        };

        forcebundle.iterations_rate = function (i) {
            if (arguments.length === 0) {
                return I_rate;
            } else {
                I_rate = i;
            }

            return forcebundle;
        };

        forcebundle.subdivision_points_seed = function (p) {
            if (arguments.length == 0) {
                return P;
            } else {
                P = p;
            }

            return forcebundle;
        };

        forcebundle.subdivision_rate = function (r) {
            if (arguments.length === 0) {
                return P_rate;
            } else {
                P_rate = r;
            }

            return forcebundle;
        };

        forcebundle.compatibility_threshold = function (t) {
            if (arguments.length === 0) {
                return compatibility_threshold;
            } else {
                compatibility_threshold = t;
            }

            return forcebundle;
        };

        /*** ************************ ***/

        return forcebundle;
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
  font-size: 1vw;
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