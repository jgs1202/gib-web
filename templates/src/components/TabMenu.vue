<template>
  <div>
    <ol>
      <li class="title">
        {{ title }}
      </li>
        <li v-for="(item, index) in items" :key=index class='indexButton'>
           <router-link v-bind:to=item.path>
              {{ item.title }}
           </router-link>
        </li>
    </ol>
    <div class="pad"></div>
  </div>
</template>

<script>
export default {
  name: 'TabMenu',
  data () {
    return {
      title: 'GIB layout',
      items: [
        { title: 'top', path: '/' },
        { title: 'tutorial', path: '/tutorial' },
        { title: 'try!', path: '/try' },
        { title: 'contact', path: '/contact' }
      ]
    }
  },
  mounted: function () {
  }
}
</script>

<style scoped>

ol {
  margin: auto;
  width: 90%;
  display:flex;
  justify-content: center;
  padding: 0;
  list-style: none;
  border-bottom: 1px solid black;
  padding-bottom: 4%
}

li {
  margin-left: 10%;
  margin-right: 10%;
}

.title {
  font-size: 3.5vw;
  max-height: 50px;
  margin-left: 2rem;
  position: relative;
}

@media screen and (min-width: 1000px) {
  .title {
     font-size: 34px;
  }
}

.indexButton {
  width: 100px;
  height: 50px;
  margin-left:10px;
  margin-right:10px;
  font-size: 14px;
  background-color: skyblue;
  border-radius: 8px;
  position: relative;
}

.indexButton:hover {
  width: 100px;
  opacity: 0.4;
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

div.pad {
  padding-bottom: 4%;
}

</style>
