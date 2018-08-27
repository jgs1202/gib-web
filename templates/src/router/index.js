import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '@/components/HelloWorld.vue'
import tutorial from '../components/tutorial.vue'
import real from '../components/try.vue'
import contact from '../components/contact.vue'
import home from '../components/home.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: home
    },
    {
      path: '/tutorial',
      name: 'tutorial',
      component: tutorial
    },
    {
      path: '/try',
      name: 'real',
      component: real
    },
    {
      path: '/',
      name: 'contact',
      component: contact
    }
  ]
})
