<template>
  <div id="4layouts">
    <p class='explain'>You can EASILY access 4 GIB layous.</p>
    <ol class='images'>
      <li>
        <img src="../assets/stgib.png">
      </li>
      <li>
        <img src="../assets/cdgib.png">
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
        <img src="../assets/fdgib.png">
      </li>
      <li>
        <img src="../assets/trgib.png">
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
export default {
  name: 'gib-example',
  data () {
    return {
      sample: 'aiu'
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
