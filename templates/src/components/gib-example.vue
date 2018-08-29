<template>
  <div id="4layouts">
    <p class='explain'>You can EASILY access 4 GIB layous.</p>
    <ol class='images'>
      <li>
        <img id='stgib'>
      </li>
      <li>
        <img id='cdgib'>
      </li>
    </ol>
    <ol class='logos'>
      <li>
        ST-GIB &emsp; &emsp; Size is easy to see
      </li>
      <li>
        CD-GIB &emsp; &emsp; Inter-connection are considered
      </li>
    </ol>
    <ol class='images'>
      <li>
        <img id='fdgib'>
      </li>
      <li>
        <img id='trgib'>
      </li>
    </ol>
    <ol class='logos'>
      <li>
        FD-GIB &emsp; &emsp; Using force-directed layout
      </li>
      <li>
        TR-GIB &emsp; &emsp; Optimized the link distance
      </li>
    </ol>
  </div>
</template>

<script>
import $ from 'jquery'
export default {
  name: 'gib-example',
  data () {
    return {
      sample: 'aiu',
      stgib: null,
      cdgib: null,
      fdgib: null,
      trgib: null
    }
  },
  mounted: function() {
    this.stgib = $('#stgib')[0]
    this.cdgib = $('#cdgib')[0]
    this.fdgib = $('#fdgib')[0]
    this.trgib = $('#trgib')[0]
    this.downloadImage()
  },
  method: {
    downloadImage: function() {
      $.ajax({
        url: 'http://35.200.124.149/image/stgib.png'
      }).done((data, status, jqXHR) => {
        let downloadData = new Blob([data])
        let filename = 'stgib.png'
        if (window.navigator.msSaveBlob) {
          window.navigator.msSaveBlob(downloadData, filename)
        } else {
          let downloadUrl = (window.URL || window.webkitURL).createObjectURL(downloadData)
          let link = document.createElement('a')
          link.href = downloadUrl
          link.download = filename
          link.click()
          (window.URL || window.webkitURL).revokeObjectURL(downloadUrl)
        }
      }).fail((data, statujs, jqXHR) => {
        alert('Image download fail!')
      })
    }
  }
}
</script>

<style scoped>

ol {
  margin: auto;
  width: 100%;
  display:flex;
  justify-content: center;
  padding: 0;
  list-style: none;
}

li {
  margin-left: 2%;
  margin-right: 2%;
  width: 100%;
}

.images img {
  width: 100%;
  padding-bottom: 3%;
}

.logos {
  padding-bottom: 4%;
  font-size: ;
}

p.explain {
  font-size: 2.5vw;
  padding-bottom: 2%;
}

@media screen and (min-width: 1000px) {
  p.explain {
     font-size: 30px;
  }
}

</style>
