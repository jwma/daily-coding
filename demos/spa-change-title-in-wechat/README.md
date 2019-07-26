### 事发必有因
近日在微信端开发 SPA（用 Vue.js） 时遇到了点问题，应用有若干页面，每个页面的标题都可能不一样，于是就按照直觉写了如下代码：

```javascript
// 省略...
// 定义页面路由
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

// 实例化路由
const router = new VueRouter({routes})

// 在路由导航之后更新当前页面标题
router.afterEach(route => {
  // 从路由的元信息中获取 title 属性
  if (route.meta.title) {
    document.title = route.meta.title
  }
})
// 省略...
```
如上代码，在大部分 PC 浏览器确实可以正常运行，包括微信官方提供的"微信web开发者工具"也是可以正常更新页面标题的，但恰恰就是 iOS 端的微信有着这个 bug，然后想起，微信年初发布的"iOS WKWebView 网页开发适配指南"中提到了，如果将微信切换到 WKWebView 则可以解决。

> 使用WKWebView，在单页应用中通过document.title多次修改原生title的方法将失效，该问题将于微信3月份发布的版本中解决 —— 截取自微信官方文档

恰巧就是2017年3月27日 iOS 端微信的更新，也恰巧是我今天才遇到这个问题，正是因为这么巧，所以才写了这篇文章。

### 撸起袖子干
虽然更新微信且切换到 WKWebView 之后是可以解决这个问题，但为了适配那些没有更新微信且还用着 UIWebView 的设备，所以还是需要写点 hack 的代码：
```javascript
// 省略...
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
// 省略...
```
上面的写法，可以兼容两种 WebView，在我的 iPhone6s 微信6.5.6 版本中通过测试。

代码比较简单，所以也不做过多的说明了。

### 部署
整个示例项目用 vue-cli 进行安装，模板是 webpack-simple，额外安装了 vue-router。
```
npm install
npm run dev
```