import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

import App from './App.vue'
import Home from './page/Home.vue'
import Articles from './page/Articles.vue'

const routes = [
  {
    path: '/',
    component: Home,
    meta: {
      title: 'Home'
    }
  },
  {
    path: '/articles',
    component: Articles,
    meta: {
      title: 'Articles'
    }
  }
]

const router = new VueRouter({routes})

router.afterEach(route => {
  // 从路由的元信息中获取 title 属性
  if (route.meta.title) {
    document.title = route.meta.title

    // 如果是 iOS 设备，则使用如下 hack 的写法实现页面标题的更新
    if (navigator.userAgent.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/)) {
      const hackIframe = document.createElement('iframe')
      hackIframe.style.display = 'none'
      hackIframe.src = '/robots.txt?r=' + Math.random()

      document.body.appendChild(hackIframe)

      setTimeout(_ => {
        document.body.removeChild(hackIframe)
      }, 300)
    }
  }
})

new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
