# 来，跨个域看看 (CORS)

CORS 即跨资源共享，是一种机制，它使用额外的 HTTP 头来告诉浏览器  让运行在一个 origin (domain) 上的 Web 应用被准许访问来自不同源服务器上的指定的资源。
简单来说，出于安全原因，浏览器会限制从脚本内发起的跨域请求，如 XMLHttpRequest 和 Fetch。也就是说，在 Javascript 中，当我们想发起一个跨域的 Ajax 请求，会受到浏览器的限制导致请求失败。

举个例子：
在 http://mysite.com/index.html 中，发起一个 Ajax 请求到 http://api.yoursite.com/article/all/ ，会失败，如果打开控制台看日志，会看到类似如下的输出：
```
Access to XMLHttpRequest at 'http://api.yoursite.com/article/all/' from origin 'http://mysite.com' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

在现在开发常规 Web 项目的时候，即使在正式上线后使用统一域名访问项目，也很难说在开发和联调过程中也使用统一域名，所以掌握跨域请求的处理还是很有必要的。

### 实现跨域请求的途径
跨域请求的处理方法除了 **CORS** 外，还有 **代理服务器**、**JSONP**。

#### 代理服务器
一说到使用服务器的方式，我们可以马上想到一个流行的反向代理服务器 Nginx，的确，我们可以使用 Nginx 的 `proxy_pass` 指令实现代理的目的，但这种方法往往很不直观，且一般也需要前端同学在本地搭建相关环境才可以运作，可以说是一个不怎么样的选择。

除了 Nginx 外，前端的同学可能会说现在很多流行的框架都集成有这样的功能，如 Vue.js 的 `devServer`，前端同学可以在项目中编写熟悉的 Javascript 代码以实现请求的代理，最终实现跨域请求，方便联调，但也局限于开发时使用。

#### JSONP
JSONP 是利用了 src 引用静态资源时不受跨域限制的机制，前端会先定义一个回调函数用来处理请求成功后的逻辑，并在请求服务端时告知服务端这个回调函数的名字，而服务端只需要把需要返回的数据按照 Javascript 的语法，放进回调函数中即可。
大概像这样子：
```html
<!-- http://mysite.com/index.html -->
<script>
function callback(data) {
    // 处理 data
    console.log(data)
}
</script>
<script src="http://api.yoursite.com/article/all/?callbackFunc=callback"></script>
```
的确，JSONP 可以成果获取到数据，且回调函数也会被正确执行，但在使用 JSONP 之前，它的缺点你需要先了解：
- 只能用 HTTP Get 请求；
- 错误处理不完善，我们很难对请求时发生的错误进行处理；
- 安全问题；
- 等等。

说实话，现在在开发项目时已经很少使用 JSONP 了，这里只是给同学们了解了解。

#### CORS
CORS 机制，允许 Web 应用服务器进行跨域访问控制，从而使跨域数据传输得以安全。

这里以 Nginx 为例，看看要怎样才能做到跨域访问控制。
我们来看看如何配置吧：
```
http {
  # 省略其他...
  server {
    listen 80;
    server_name api.yoursite.com;
    charset utf-8;
    location / {
      include /usr/local/nginx/conf/cors;
      // 省略其他...
    }
  }
}
```
这样，我们 http://api.yoursite.com/ 下的 API 就支持跨域请求了（不考虑程序代码有限制的情况）。

重点是 `include /usr/local/nginx/conf/cors;` ，下面来看看 cors 文件里面的内容吧：
![cors](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8WcE1tfYuvtAZ50uCtrpvChwwaBNOtSvdOVpzibhOAlwiaxkBPLlW6JibJqmPZUdVPic1ZQqczBUbeFMA/0?wx_fmt=png)

其核心的部分，是加入了 `Access-Control-Allow-Origin` HTTP 头，而其他部分的内容，则是更细粒度的控制，如不同的请求方法也可以设置不同的 HTTP 头达到控制的目的。
搭配 Nginx 的 `location` 指令，我们则可以控制某些路径下才开启 CORS，以达到更细粒度的控制。

大家可以在 https://enable-cors.org/server_nginx.html 获得 cors 文件的内容。这个文件内容只是一个范本，并不是唯一的写法，大家在实际使用时按照需求自行修改即可。

如果你想更深入了解 CORS 机制，可以访问 https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Access_control_CORS

### 不用 Nginx 行不行？
理解了 CORS 机制的原理的话，这种问题不在话下。

这个网址提供了不同服务器、Web 框架、编程语言的实现方式，https://enable-cors.org/server.html 。

忍不住吐槽，里面偏偏没有 Django 的实现方式，Django 的话，可以使用 `django-cors-headers`，在使用 Django 开发后端时，前端也能愉快的发起跨域请求了。

### 选择 CORS
从技术的革新角度也好，从使用的便捷度也好，CORS 是一个更好的跨域请求的选择。只需要（一般是）后端人员配置好，前端可以不需要做任何额外的改变，就可以调用后端 API 了。这种方法，无论是开发时或是正式上线后，都可以使用，无需考虑过大的差异性问题。

还没有用过 CORS 的同学，赶紧尝试一波吧。
