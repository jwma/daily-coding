## 前情回顾
在上一次 [码极系列-05 | 初步搭建前端项目](https://mp.weixin.qq.com/s?__biz=Mzg5ODAwODM0Mg==&mid=2247483703&idx=1&sn=4750129a1008c691a0f3690bcad4d803&chksm=c068554ef71fdc58aa78451a7dbc186f27564f3c96846fcd3f188e482d3c33a1bb51484a7826&token=516286706&lang=zh_CN#rd) 分享中，已经初步搭建好了前端项目的架子了，这次分享则会讲讲如何让这个架子能够真正的动起来。

## 前端项目运行效果
`jump-jump` 的前端项目，主要是用于短链接的管理（新增、更新短链接）。

新增短链接，以及短链接的使用：
![新增短链接，以及短链接的使用](https://mmbiz.qpic.cn/mmbiz_gif/oS1Ryib0qL8WqDVHYjUzvXlHewMJlKUDM21eicheeYL4BsFWkFBRVfvBtFqc7sIpdrb2bvDwofHAlkQ90om8PCmw/0?wx_fmt=gif)

更新短链接设置（如禁用某个短链接）：
![新增短链接，以及短链接的使用](https://mmbiz.qpic.cn/mmbiz_gif/oS1Ryib0qL8WqDVHYjUzvXlHewMJlKUDM0p1ArHjkyqtLiaITkDb3dvSuWiborhKxIicfqG7Xia37GFJd785bggkfsw/0?wx_fmt=gif)

## SPA（单页应用）
上面展示的应用，其实是一个 SPA（single-page application）。

> 单页应用（英语：single-page application，缩写SPA）是一种网络应用程序或网站的模型，它通过动态重写当前页面来与用户交互，而非传统的从服务器重新加载整个新页面。这种方法避免了页面之间切换打断用户体验，使应用程序更像一个桌面应用程序。在单页应用中，所有必要的代码（HTML、JavaScript和CSS）都通过单个页面的加载而检索[1]，或者根据需要（通常是为响应用户操作）动态装载适当的资源并添加到页面。尽管可以用位置散列或HTML5历史API来提供应用程序中单独逻辑页面的感知和导航能力，但页面在过程中的任何时间点都不会重新加载，也不会将控制转移到其他页面。[2]与单页应用的交互通常涉及到与网页服务器后端的动态通信。——维基百科

看完上面的描述，其实能够清楚知道 SPA 的优点和特点，而我们也会用 `Vue全家桶` 来开发一个 SPA：
- `Vue.js` 将会给我们带来不一样的数据交互体验，还让我们的前端工程得以组件化开发；
- `Vue Router` 将会帮我们处理、管理前端路由；
- `Vuex` 将会帮我们更好的处理前端项目运行时的各种状态，同时也让我们更容易在组件间共享数据。

## 撸起袖子就是干
下面就以 `jump-jump` 的前端项目新建短链接功能为例，讲讲我们如何用 `Vue.js` 开发一个 SPA。

这次分享不会从 `Vue.js` 的基础开始说，我相信学习基础部分没有什么地方会比官方文档更好。

### Vue.js 单文件组件
在正式开始动手之前，我们很有必要了解下 `Vue.js` 的`单文件组件`是什么。
![单文件组件](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8WqDVHYjUzvXlHewMJlKUDM7kEgnV5UlP3SetLicXNXzhibE3iaiaZWELs48dfLEgN8nAZeXAicSysQMOA/0?wx_fmt=png)
这就是一个 `Vue.js` 单文件组件，可以看出，文件以 `.vue` 结尾，一个文件内包含了模板、逻辑和样式，仔细想想，我们开发应用的时候，每个独立的组件其实都可能会包含这三部分的内容，而在使用 `Vue.js` 开发时，我们也应该有这组件化的思维，我们在编写组件时，就可以使用`单文件组件`进行开发。

有的人可能会想，不是一直都强调代码应该分层管理吗，逻辑应该写在 `.js` 文件中，样式应该写在 `.css` 文件中，像`单文件组件`难道不是在开历史倒车？

> 一个重要的事情值得注意，关注点分离不等于文件类型分离。在现代 UI 开发中，我们已经发现相比于把代码库分离成三个大的层次并将其相互交织起来，把它们划分为松散耦合的组件再将其组合起来更合理一些。在一个组件里，其模板、逻辑和样式是内部耦合的，并且把他们搭配在一起实际上使得组件更加内聚且更可维护。——Vue.js 官方中文文档

我个人认为，类似于`单文件组件`的形式是更有利于组件化开发的。

### 应用的入口
图片代码中附有注释，一起服用效果更佳。

`src/main.js`
![main.js](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8WqDVHYjUzvXlHewMJlKUDMDmR151jPPboOGINSGUYYWicWwdKUSAVt9bdicp3JH0nOJ4oVm0ZypickQ/0?wx_fmt=png)

`src/App.vue`
![App.vue](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8WqDVHYjUzvXlHewMJlKUDMQ5QnolECacpcHQN1ib1AfluEYK4lVzGZd6P9LSibibepJ6O2s9XZzRAMw/0?wx_fmt=png)

`public/index.html`
![index.html](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8WqDVHYjUzvXlHewMJlKUDMe29Ulh6fWvwbTNAg1Q3iaxiaoC2w53IiaZXRRibKfHdnibIUC2IiaUdJPTzQ/0?wx_fmt=png)

### 实现新建短链接功能
新建 `src/views/Home.vue`，这是实现新建短链接功能的场所。

#### 编写模板
新建短链接，我们只需要通过一个简单的表单提交目标链接 `URL` 和一个用于备注的 `描述`即可，提交后，我们需要显示一个这次提交结果的`提示信息`，所以页面上应该有：
- 两个输入框
- 一个提交按钮
- 一个用于展示提示信息的地方

知道页面上应该有什么之后，我们就可以写出页面的模板了：
![Home template](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8WqDVHYjUzvXlHewMJlKUDMeXy1TrUn416IsdiaM25ITOcIsBX3HwrfuCiaJaEEeDibCrM65VibLznMVA/0?wx_fmt=png)

#### 编写逻辑
有了模板，我们就需要实现应用的逻辑部分了，很明显，我们在点击提交按钮后需要把 `URL` 和`描述`通过接口发送到后台，然后根据后台返回的结果显示一些提示信息给用户：
![Home logic](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8WqDVHYjUzvXlHewMJlKUDMOiaDI4mUpkfZ0MPKibrODXDZK0efAyKDibZ4FDibqd94IJCB8CbfCibHYFw/0?wx_fmt=png)

##### data 的定义
在这个组件中，我们定义了 `data`，它与我们的模板和逻辑紧密关联，当 `data` 的数据变化，如果模板上有关联的部分，也会马上响应这个变化，正正是这种响应式，让我们在处理数据和模板时得到了“质的改变”体验。
这里的 `data` 则包含了我们在编写模板时提到的几个数据，`URL`，`描述`，`提示信息`。

##### 事件处理
我们在提交按钮使用了 `@click="submit"` 进行了事件的绑定，接着我们在组件中声明了 `methods.submit`，下面进行简单的说明：
- 在 `submit` 中，我们可以通过 `this` 获取到当前组件的引用，而 `this.xxx` 则可以获取到当前组件 `data` 定义的数据；
- 在 `43-36` 行代码中，直接判断了用户是否有输入 `URL`，如果没有，前端直接返回，这里也是我们常用的前端表单校验和拦截处理；
- 我们使用了挂到 `Vue` 原型链的 `$http` 对接口进行请求（参考入口文件`src/main.js`）
  - 想想上一次分享中配置的 `devServer`，这里开始就起作用了；
  - `process.env.VUE_APP_API_ADDR`，这是在 `.env` 文件定义的一个环境变量，而具体的值则是 `/api`，为什么是 `/api`，其实是跟 `devServer` 的配置对应，我需要代理 `/api` 开头的接口到特定的地址；
- 在回调中，根据接口数据的不同，设置不同的提示信息到 `tips`，页面上展现 `tips` 数据的地方就会响应这个变化并显示对应的提示信息。

#### 注册路由
![router](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8WqDVHYjUzvXlHewMJlKUDMlLCFZ9Z6FOJmibf7xwAG4HKcgWYJcdiaycyNibrZBaDIM26qkxmGor8JQ/0?wx_fmt=png)

此时如果把应用跑起来，则会看到首页就可以新增短链接了，运行效果和本文最上方的新增短链接图例一样。

## 后面需要做的事情
- 后端搭建一个简单的用户体系，进入管理页面需要身份验证；
- 使用 JWT 进行通信；
- 前端登录状态的维护。

## 写在最后
这次分享，大致梳理了一下开发一个 `Vue` 页面组件的流程，如果你对如何开发 `Vue` 项目还没有了解，希望这对你有帮助。

如果你发现你已经看不懂本文的 `Javascript` 代码了，那真的得赶紧补上了，这就是 `ES2015/ES6`，看看年份，已经是三年前制定的标准了。
