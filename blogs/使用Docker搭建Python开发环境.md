# 使用 Docker 搭建 Python 开发环境

我们知道，Docker 能为我们创造出一个个相对独立且又能互相通信的容器环境，我们把自己的应用放在里面，就能达到快速部署的目的，没错，我们的确是常常使用 Docker 来打包和部署我们的应用，但今天要分享的是花费绝大部分程序员最多时间的开发环节的内容，适合有如下需求的同学阅读：
- 想要或需要多版本环境开发；
- 优化团队项目开发环境管理；
- 不想污染“本地”环境；
- 喜欢 Docker。

## 由浅入浅
谈到开发，除了不同语言的运行环境外，另一个不得不谈的就是开发时使用的各种编辑器或是 IDE，无论选用哪一种工具，我们的目的都应该是提高生产力。本文使用的是 PyCharm（题外话，最近我又续费了我的个人账户，由于我用了好几款不同的 IDE，所以我买的是全家桶，一年下来大概在 1800 RMB 左右，算一下其实还是很值得的）。

### 搭建一个最基础的环境
我们先尝试使用 Python 官方镜像作为最基础的开发环境吧，这个例子中我使用的是 python:3.7 这个镜像。
如果你本地没有这个镜像，可以先运行 `docker pull python:3.7` 再回来看这篇文章。

在你喜欢的目录下创建一个新的项目目录，例如 ~/Desktop/myproject，然后使用 PyCharm 打开这个目录，然后可参考如下步骤：
1. 添加 Docker
![添加 Docker](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8WcE1tfYuvtAZ50uCtrpvChpQRrgjJN8mWAsFiadOAxOibQsxcic3kH8Dkb2vFyglzkDn01Gm3WRcXcw/0?wx_fmt=png)
2. 添加 Project interpreter
![添加 Project interpreter](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8WcE1tfYuvtAZ50uCtrpvChSvHOM9u0Jbvmx0uqYKFtKOpzHpcpWmd9hcZtkmjMeOvaztFJrEv48Q/0?wx_fmt=png)
![添加 Project interpreter](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8WcE1tfYuvtAZ50uCtrpvChmdoQib5kpF1KwAicGl0XqEFf13hnpr1OchUEOCIHmbMXCld4ZKTL6wzw/0?wx_fmt=png)

完成上面的步骤后，等待 IDE 处理完毕，然后这个项目就会使用 python:3.7 这个镜像作为运行环境了。

我们写个程序验证一下是否能正常运作吧：
1. 运行 app.py
![Run hello world](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8WcE1tfYuvtAZ50uCtrpvChibnGvib5ROBauuC7qMNxcckhXpGswwicbgJh3J1ZJofEmAqmL2B6A2lxg/0?wx_fmt=png)
2. Debug app.py
![Debug hello world](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8WcE1tfYuvtAZ50uCtrpvCho7ajPib0FpGmVMlaFKUwUcV8eTibaVdFwhqHcfSXX82UDJbYojn4hia2w/0?wx_fmt=png)

现在 myproject 这个项目就可以正常运作了，但我们一般会在开发时会使用各种不同的框架或者库，那么此时我们就需要去自定义一个镜像，然后使用自定义镜像作为开发环境了。

### 使用自定义镜像搭建环境
假如，我们现在需要做一个简单的爬虫，那么我们就需要 requests 库，也就是说我们的镜像就需要预先安装 requests 库以供使用，下面是自定义镜像的 Dockerfile 内容：
```
FROM python:3.7   

RUN pip install requests

CMD ["python3"]
```
文件内容很简单，我们只是基于 python:3.7 镜像去自定义我们自己的镜像，使用 `RUN pipinstall requests` 安装了 requests 库。
接着我们需要构建出自己的镜像，这里我们把镜像名字定位 myproject，所以我们运行 `docker build -t myproject .`，稍等片刻，我们就得到了一个自定义镜像了，可以运行 `docker images` 查看：
![myproject image](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8WcE1tfYuvtAZ50uCtrpvChaHcv3bVYZmcaswlpOE7E3lYdmentjmNH0JqMicDKdLQT6NjGGFcZe3A/0?wx_fmt=png)
此时，我们回到 PyCharm，按照上文中的 添加 Project interpreter 步骤，在选择镜像时改成 myproject 镜像即可。

写个简单的程序验证一下：
![run spider.py](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8WcE1tfYuvtAZ50uCtrpvChFeTiaHHIaCcucibXwgiblHR8pH1mye1SU6SueWvmUAibaEyld0XLiaEXMjQ/0?wx_fmt=png)
可以看出，我们能够使用 myproject 镜像内的 requests 库为我们服务了（如果 IDE 提示说没有 requests 库，可以重启一下  IDE，就可以正确加载出来了）。

至此，用 Docker 搭建 Python 开发环境的套路就完毕了，但我想会有一些同学说实际开发过程中，环境往往比这个复杂很多，这种玩具不顶用呀。的确，就我个人而言，我几乎没有使用过这种方式来搭建正式项目的开发环境，但稍安勿躁，我会在另外一篇文章中分享更适合正式项目的开发环境搭建，敬请期待。
