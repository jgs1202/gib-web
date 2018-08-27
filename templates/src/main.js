// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import {
  Row,
  Col,
  Alert,
  Select,
  Radio,
  RadioButton,
  RadioGroup,
  Input,
  Option,
  Dropdown,
  DropdownMenu,
  DropdownItem,
  Button,
  Form,
  FormItem,
  Slider,
  Container,
  Aside,
  Header,
  Main,
  Footer
} from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
Vue.use(Row)
Vue.use(Col)
Vue.use(Alert)
Vue.use(Select)
Vue.use(Input)
Vue.use(Radio)
Vue.use(RadioButton)
Vue.use(RadioGroup)
Vue.use(Option)
Vue.use(Dropdown)
Vue.use(DropdownMenu)
Vue.use(DropdownItem)
Vue.use(Button)
Vue.use(Form)
Vue.use(FormItem)
Vue.use(Slider)
Vue.use(Container)
Vue.use(Aside)
Vue.use(Header)
Vue.use(Main)
Vue.use(Footer)

Vue.config.productionTip = false
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
