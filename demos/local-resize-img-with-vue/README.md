## 部署

`npm run install` 安装依赖，访问index.html即可。

如果需要运行indexWithHandle.html，则可以运行 `php -S 127.0.0.1:8080` 开启一个PHP服务器，然后在浏览器访问 `localhost:8080/indexWithHandle.html` 即可，PHP处理上传的逻辑都在 upload_handler.php 文件中。


# 为什么要这么做？
在移动Web蓬勃发展的今天，有太多太多的应用需要让用户在移动Web上传图片文件了，正因如此，我们有些困难必须去攻克：

1. 低网速下上传进度缓慢，用户体验差
2. 高并发下，后台处理较大的上传文件压力大
3. 或许有更多...

在攻克上面的一些困难时，我们也可以给自己一些疑问：

1. 真的有必要保存用户上传的原图吗？
2. 用户还能等多久？
3. 或许还有更多...

结合上面的一些困难和疑问，再结合我们实际的案例，我们或许可以这样做 —— 在用户上传图片时，图片被提交到后台之前，就对图片进行压缩处理。图片文件大小减小后，上传速度自然会提升，在同样的并发下，后台处理的速度也会得到提升，用户体验得到提升。

有童鞋可能会说，为什么不使用一些主流CDN的表单功能，直接把文件上传到CDN去？当然，完全可以选择那种方案，我只是在众多的方案中选择了一个来用而已，又或者说这是程序员的天性？

# 准备
上面已经说了 “在用户上传图片时，图片被提交到后台之前，就对图片进行压缩处理。”，那我们马上准备下各种工具吧：

1. [localResizeIMG][1]（核心，用于在前端对图片进行压缩）
2. [Vue.js][2]（处理前端的数据，展现逻辑）
3. [Bootstrap][3]（还要我多说？）

# 怎么做？

 1. 上传项目变更后，使用localResizeIMG进行压缩
 2. 把数据通过自己期望的方式提交到后台
 
localResizeIMG在调用时，就可以指定压缩后图片的宽度高度以及质量（[详细参考文档][4]），至于要怎么把数据提交到后台，可以参考该库的wiki中提到的[方案][5]，一切都很简单。

**[演示地址][6]**

本文的解决方法并不是唯一，也不一定是最好，在使用相关的框架/库时遇到的问题，可以去相应的Github仓库查看issue或者wiki。


  [1]: https://github.com/think2011/localResizeIMG
  [2]: https://github.com/vuejs/vue
  [3]: https://github.com/twbs/bootstrap
  [4]: https://github.com/think2011/localResizeIMG/wiki/2.-%E5%8F%82%E6%95%B0%E6%96%87%E6%A1%A3
  [5]: https://github.com/think2011/localResizeIMG/wiki/1.-%E5%90%8E%E7%AB%AF%E5%A4%84%E7%90%86
  [6]: http://dc.majiawei.com/local-resize-img-with-vue/index.html
