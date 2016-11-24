#部署
既然是微信小程序，请自行下载其开发工具，并添加项目。

接口部分都放到了 app.php，在 app.php 所在的目录运行 `php -S 127.0.0.1:8080` 即可。

微信小程序公测也有段时间了，但是里面的坑踩了一个又一个，心也是够累的。本文说说关于 wx.request 和 wx.uploadFile 对请求响应的不同表现。

### [wx.request][1]
使用 wx.request 发出请求，在对接口的响应做处理时，官方提供了三个回调函数，分别是 success，fail，complete，看了官方文档，其实也很清晰什么时候用什么回调，在这里也不多赘述了。

### [wx.uploadFile][2]
使用 wx.uploadFile 可以上传文件，并可以携带一些额外的信息，在对接口的响应做处理时，和 wx.request 一样，也提供了同样的三个回调函数，在官方文档中，其描述几乎是一样的（除了success）。

在对这两个接口有了一定的了解后，说说这两个接口对请求的相应的不同表现。

先上张图体会下：
![图片描述][3]

wx.request 发出请求后，无论请求接口返回的 HTTP 状态码（200也好，500也好）是什么，都会进入 success 回调，和一般认为的 500 会进入 fail 回调不一样。
（吐槽：对，接口是微信开发团队定的，按照这个规律，我们只能遵循，然后我就遵循这一规律继续写）

wx.uploadFile 发出请求后，如果请求接口返回的 HTTP 状态码为200时，会进入 success 回调，而返回其他状态码（如400、405、500等）时，会进入 fail 回调（黑人问号.jpg）。

虽然这不是啥大问题，但在微信小程序的开发过程中，上面提到的问题还是会让人一下子摸不着路子。个人觉得接口保持一致性还是很重要的，不过游戏的制定者不是我们，只能希望越改越好吧。

  [1]: https://mp.weixin.qq.com/debug/wxadoc/dev/api/network-request.html
  [2]: https://mp.weixin.qq.com/debug/wxadoc/dev/api/network-file.html#wxuploadfileobject
  [3]: https://sfault-image.b0.upaiyun.com/390/440/3904405494-5836936ab082b_articlex