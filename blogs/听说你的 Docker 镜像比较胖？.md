# 听说你的 Docker 镜像比较胖？


减肥，是一个自己心知肚明但却有无能为力的事情，我虽然减不了肥，但我能把我 Docker 镜像的肥减一下，微笑.jpg。

如果有看之前的一篇文章 使用 Docker 搭建 Python 开发环境 的话，你会发现一个很明显的问题，那就是构建出来的镜像太大了，如下图右下角的位置：
![myproject image](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8WcE1tfYuvtAZ50uCtrpvChaHcv3bVYZmcaswlpOE7E3lYdmentjmNH0JqMicDKdLQT6NjGGFcZe3A/0?wx_fmt=png)
足足有 937MB 之大，可以说很肥了，如果你磁盘空间本来就紧张的话，你可能就会破口大骂了，如果你觉得这不是问题的话，再想想如果你需要把这个镜像发布到 Docker Hub 又或是任何一个镜像仓库呢？我相信在你 docker push 的时候会骂街。

### 为什么会这么肥？
Emm...就是平时吃的比较多又不喜欢做运动，躺在床上躺在沙发上贼舒服...

扯远了扯远了，回到正题，在我们聊如何减肥之前，先好好了解一下为什么会肥吧，事出必有因嘛。
上文提到的那个肥大的镜像叫 myproject 镜像，我们先回顾下这个镜像的 Dockerfile 吧：
```
FROM python:3.7
RUN pip install requests
CMD  ["python3"]
```

以我敏锐的直觉，已经发现了问题绝对出在第一行，不要问为什么，让我装 x 一次。

我们先运行下 `docker images python:3.7`，会看到：
![python:3.7](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8XKla5MEE3zx19ykfBicGBQ1lb7vXNsxJUiarnThkoPoYeia82TAmibGA3VSE3jNhKnDic5YLq375IjxXQ/0?wx_fmt=png)

原因是找到了，作为 myproject 的基础镜像 python:3.7 镜像本来就很大，所以我们在这基础上构建的镜像只会更大（不考虑删除基础镜像内部的文件），那 python:3.7 为什么这么大？我们运行 `docker history python:3.7` 来查看这个基础镜像的创建历史：
![python:3.7 history](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8XKla5MEE3zx19ykfBicGBQ1WFJCN8jGVZ9kuMf7oRwfcm1Da7F0QceuicR4UodAUbibKRjEQvgPAC0g/0?wx_fmt=png)
我们能看到，这个镜像创建的历史的每一层，SIZE 比较大的层，都是往镜像塞文件的记录，如果想刚具体每一层都做了什么，可以运行 `docker history --no-trunc python:3.7`，输出虽然不太友好，但能清楚看到的的确确容量大的层都是在往镜像里面塞东西的层，大致分为系统底层、各种用于构建的库和工具、Python 源码包等，再回顾我们的 myproject，我们也在往里面塞我们需要的内容，基础镜像的内容 + 我们写的 Dockerfile 的内容，组合成我们最终的镜像。

我们在 history 中看到，一个镜像的创建历史是一层一层的，有没有感觉像 Git 提交一样，也是一层一层的叠上来？这每一层，都对应了 Dockerfile 的每一行，每一层都是独立的，每一层都有自己的一席之地（容量）。

### 有没有立竿见影的减肥方法？
Emm...对我自己而言，可能没有，但对于 Docker 镜像来说，的确是有的。

我们已经知道 python:3.7 这个基础镜像本身就很肥大，那我们能不能不适用它？答案的当然的，我们完全可以从零自定义自己的镜像，感觉就像是在一台全新的服务器自己去编译安装自己需要的软件、环境，但我们现在是要立竿见影，从零做一个自己的镜像好像有点花时间，所以我们使用 python:3.7-alpine 镜像 去替换 python:3.7 镜像，Dockerfile 的内容更新为：
```
FROM python:3.7-alpine
RUN pip install requests
CMD  ["python3"]
```

然后我们运行 `docker build -t myproject:alpine .` 进行构建，接着来看看这个镜像有多大吧，运行 `docker images myproject` 查看：
![myproject:alpine](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8XKla5MEE3zx19ykfBicGBQ18hicaibc8o7DlUFvMdcTP4kFULrFrKNypunVoSWP0aoCibic7wlNMX40Vg/0?wx_fmt=png)
没看错，myproject:alpine 的容量是 myproject 的近九分之一，只有 107MB，这个效果可谓是立竿见影了。


