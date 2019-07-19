## 前言
在上一篇分享（[码极系列-04 | 谈谈前后端分离](https://mp.weixin.qq.com/s?__biz=Mzg5ODAwODM0Mg==&mid=2247483697&idx=1&sn=0b93fb2f83a246c8a008fc74b8f86cf7&chksm=c0685548f71fdc5edf8a45d3d7865dcac3fe086f0b64a050687c9ae75e762228be5e9dbe91ca&token=1098856162&lang=zh_CN#rd)）中，我们已经确定 `jump-jump` 前端项目的方向了，这次分享，则是初步搭建一下前端项目，大部分前端同学应该会很明白我在干嘛，而我希望的是让更多后端的同学明白我在干嘛，希望我能做到吧！

## 谈谈快速发展的前端
相信有一定经（年）验（纪）的开发人员都知道，在很多年前，我们开发一个 Web 项目，前端部分的代码可能都比较随意，重点好像永远都在后端。
但随着互联网时代的发展，特别是移动互联网的发展，各种前端技术得到了快速的发展，有了很多的标准、规范，有更多的人投入到前端这个领域，于是有了很多前端的生产工具、框架类库等等；很多公司和普通用户对前端的要求日益提高，除了功能要实现以外，还要长得好看（UI），还要体验好（UX），这些无疑都是前端快速发展的强大推进力。

有了解前端的人可能会说，前端是在快速发展，但前端领域隔三差五就出一些 A 库 B 框架，让人看得眼花缭乱，而一些想投身于前端领域的人也会因为这样而感到焦虑，感觉要学的东西永远学不完。的确，这也是我自己的亲身体会，但我没有深陷其中，其实面对前端五花八门的技术，我自己会去分析对比主流的部分，不同方向的技术只要掌握合适的就行。

## 开始搭建前端项目
`jump-jump` 的前端项目，是一个 `Vue.js` 项目，我们通过 `@vue/cli` 进行创建，为了减少对前端不太熟的同学的不便，除了使用 `Vue.js` 全家桶以外，我会尽可能少的使用第三方框架。

### 第1步，安装 @vue/cli
我们要创建一个 `Vue.js` 项目，一般有两种途径，第一种是自己搭积木，项目结构、项目依赖、项目配置、项目入口等一一搭好，第二种，使用脚手架工具，通过工具提供的交互式命令行或是 `Web UI` 来进行项目的创建。毫无疑问，我们会使用第二种方式进行项目的创建。

安装的话，老样子看官方文档：
https://cli.vuejs.org/zh/guide/installation.html

### 第2步，创建项目
成功安装了 `@vue/cli` 后，我们现在有两种途径创建项目，这是官方文档：
https://cli.vuejs.org/zh/guide/creating-a-project.html

#### @vue/cli 交互式命令行
打开命令行终端，运行 `vue create my-app`，会得到一个如下图的交互式命令行：
[![vue command line](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8XPPpMXexK5bZFdrk6fwQ2zsicyYib7GJKd6zSoLb3Qj3swcPvqv5JNCj76aWThhq7u39XLLvgss7rA/0?wx_fmt=png)](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8XPPpMXexK5bZFdrk6fwQ2zsicyYib7GJKd6zSoLb3Qj3swcPvqv5JNCj76aWThhq7u39XLLvgss7rA/0?wx_fmt=png)

#### @vue/cli 提供的 Web UI
打开命令行终端，运行 `vue ui`，会在浏览器打开一个图形化界面，这里可以创建项目、也可以管理项目，虽然是 `Beta` 版，但功能还是挺好用的：
[![vue ui](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8XPPpMXexK5bZFdrk6fwQ2zjxaYRvOCaFDNBAp7uy9BcAzrQvEwEgIF1JyHOcnCcfSjtS33I2bnCw/0?wx_fmt=png)](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8XPPpMXexK5bZFdrk6fwQ2zjxaYRvOCaFDNBAp7uy9BcAzrQvEwEgIF1JyHOcnCcfSjtS33I2bnCw/0?wx_fmt=png)

无论你使用上述哪种方式，都能方便的创建出一个 `Vue.js` 的项目，`jump-jump` 的前端项目，在安装的过程中，选择需要的功能有：`Babel`、`Router`、`Vuex`、`Linter / Formatter`。

### 第3步，运行项目
创建完项目，使用命令行终端进入项目目录，运行 `npm run serve`，经过一点编译的时间，就可以在浏览器访问 `http://localhost:8080` ，会看到 `Vue.js` 项目默认的页面。

### 第4步，安装第三方请求库
在 `jQuery` 盛行的时代，我们经常会使用 `$.ajax` 发起 AJAX 请求，在这个项目，我们会借助一个名为 `flyio` 的库进行 AJAX 请求的处理，当然你也可以选用其他库如 `axios` 甚至是自己写 XMLHttpRequest 相关的处理逻辑。

使用命令行终端，在项目目录运行如下命令即可安装  `flyio`：
```shell
npm i -S flyio
```

这个库在之后的分享中会再细讲，简单易用又强大。

### 第5步，配置网络请求代理
这一步，就是为了解决上一篇分享中提到的 前后端联调 问题，通过代理的方式，解决开发过程中接口请求的问题。

在项目目录新建一个名为 `vue.config.js` 的文件，这个文件是 `Vue.js` 项目的一个重要配置文件，这是官方提供的配置参考文档：
https://cli.vuejs.org/zh/config/
可配置项有很多，如果有使用过旧方式开发 `Vue.js` 项目的同学，能够明显看出，现在 `Vue.js` 项目的配置已经比以前简单很多，在苦不堪言的过往，很多人都被 `webpack` 的相关配置给吓跑了。而现在的一切，都是作者和社区的努力，作为使用者，我们应该心存感谢。
```javascript
module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://web:8081',
        changeOrigin: true,
        pathRewrite: { '^/api': '' }
      }
    }
  }
}
```

这个配置的作用就是开发过程中（`npm run serve`），项目中若有发起 AJAX 请求，如 `/api/users` ，则会被代理到 `http://web:8081/users`。试想一下，如后台接口部署在 `http://web:8081`，这是你后端同事的机器，你本地的前端项目则是 `http://localhost:8080`，而你一旦发送符合规则的请求，就会被代理到你后端同事的接口地址，是不是觉得联调起来方便多了。

## 写在最后
这次分享，是为了下一次正式编写前端代码而做的准备，如果着急想知道前端代码的同学，可以到这里查看：
https://github.com/jwma/jump-jump/tree/master/admin-app

得益于 `Vue.js` 完善的生态，我们能够轻易的创建一个 `Vue.js` 项目，我们了解到如何安装第三方库，也知道了怎么配置请求代理，我相信对于一些不太熟悉 `Vue.js` 的同学来说，会是一个好的开始。
