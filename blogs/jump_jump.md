[![beego默认页面](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8VJVL470Quib1rAC8bLFvjv9OnC629mrq2NXdGVBz4HoO6u4w98jQsSpb8Labia7X7icN63Lrq2kicZkw/0?wx_fmt=png)](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8VJVL470Quib1rAC8bLFvjv9OnC629mrq2NXdGVBz4HoO6u4w98jQsSpb8Labia7X7icN63Lrq2kicZkw/0?wx_fmt=png)
## 唠叨唠叨
看完上一篇文章[让Docker来为你干点事儿](https://mp.weixin.qq.com/s?__biz=Mzg5ODAwODM0Mg==&mid=2247483658&idx=1&sn=7f22ecb5fef010e34232cc1bf68823f4&chksm=c0685573f71fdc65ee91238a07951cfcdc2e6f72de26e973993594560a568feb094c280e7610&token=396541616&lang=zh_CN#rd)后，现在马上使用Docker和Go搭建一个短链接系统。在以前的工作中，我曾为公司开发过一个短链接系统，短链接在很多场景下都非常好用，譬如：
- 便于传播链接；
- 便于生成简单清晰的二维码，二维码图案的复杂度跟URL的复杂度呈正相关关系；
- 可以查看链接的点击次数；
- 可以随时更换短链接所指向的目标链接；
- 可以分析出链接的点击记录进而分析出热点事件范围。

短链接已被自媒体、微商等应用于日常的工作场景中，如微信公众号文章，在文末的阅读原文放一个推广页面，这时使用短链接，除了可以知道点击数以外，还能随时修改这个链接，公众号运营者常常能把阅读原文的链接玩出各种新花样。

### 选择Go的原因
以前开发过的一个短链接系统是使用PHP开发的，当初走的是Symfony2+Redis+MySQL的组合，经历过一次升级后，那个短链接系统到现在为止服务了有2年多了吧，现在还健康的运行着，而这次选择用Go开发，除了程序员天性外，还考虑到Go的性能优势，除了性能优势以外考虑的还是性能优势，当然，Redis也会继续使用，MySQL在这个小系统中就不使用了，所有数据存Redis，通过Redis的AOF模式做数据的持久化，对这个小系统来说，足矣。

## 本文要点
- Go语言Web框架Beego，一个很快可以上手的框架；
- Docker搭建Beego开发环境，再也不用担心同事之间的环境有出入了；
- Docker容器间的连接（暂时不会用到docker compose），怎么能让你的容器孤零零一个。

## 撸起袖子就是干
嘿咻嘿咻！

### 第1步 Docker搭建beego的开发环境
下不同框架在Github上的情况以及实际使用这些框架开发的项目，最终也没有过多的纠结就选择了beego。
```
# 使用1.9的原因是我最后一次使用go的时候是1.9版本
docker pull golang:1.9
```
先把要用到的go语言的镜像pull一个到本地，方便为接下来的操作提速（虽然看起来差不多）。

接着我们需要创建一个自己定制的镜像，这个镜像需要支持Go以及可以运行beego程序，要制作一个镜像，我们需要编写Dockerfile，这货是上一篇文章中没提到的，我相信学习是个循序渐进的过程，上次的内容吸收了，这次我们就加点新的料。
```
# 在你平时用来放自己的项目的地方写一个Dockerfile
vim Dockerfile

# 下面是Dockerfile的内容
FROM golang:1.9

RUN go get github.com/astaxie/beego
RUN go get github.com/beego/bee
RUN go get github.com/go-redis/redis

EXPOSE 8080

CMD ["bee", "run"]
```
由于Dockerfile的语法简单，所以不难看出这个文件做了些写什么事：
- FROM golang:1.9，本镜像是基于golang:1.9的镜像
- 3句 RUN go get xxx，RUN是运行某个命令的意思，后面则是通用的go模块安装语句
- EXPOSE 8080，对外暴露8080端口
- CMD ["bee", "run"]，设置容器启动后默认执行的命令及其参数，但 CMD 能够被`docker run`后面跟的命令行参数替换，这里是启动beego应用的语句，`bee run`，会启动应用并且开始监控项目，当项目中的代码有修改，则会自动重新编译，省去我们手动编译的过程。

```
# 在Dockerfile的目录执行
docker build -t jump-jump-dev .
```
我们使用`docker build`构建了一个名为jump-jump-dev的镜像（jump-jump是我为这个系统取的名字，勿笑）。

```
# 运行如下命令，会发现我们本地多了一个jump-jump-dev的镜像
docker images
```
### 第2步 创建beego应用并验证Docker环境是否可用
上一步中，我们已经有了go和beego的开发时的运行环境了，但我们还不知道是不是真的可用，接下来我们就创建我们的短链接系统应用，然后马上验证下环境是否可以。

下面是一个beego应用程序的目录结构，当然并不一定要是这样的结构，为了生成项目骨架，我们可以使用beego官方提供的bee工具进行生成，[具体看这里](https://beego.me/docs/install/bee.md)。
```
jump-jump
├── conf
│   └── app.conf
├── controllers
│   └── xxx.go
├── main.go
├── models
│   └── models.go
└── routers
    └── router.go
```
光看目录结构，一眼就能看出beego使用的是MVC模型，对于大部分人来说再熟悉不过了，所以上手也很快，起码知道在什么地方该干些什么。

当然，光有目录结构是不足以让项目跑起来的，beego具体的hello world程序[看这儿](https://beego.me/)。

下面我就当大伙儿已经使用了官方的bee工具生成了项目了（任性如我），具体命令`bee new jump-jump`，完了之后会在`$GOPATH/src`目录创建`jump-jump`项目。
```
# 当前目录是jump-jump项目根目录，现在开始用第1步的镜像来运行这个程序
docker run -it --rm \
--name jj-dev \
-p 8080:8080 \
-v $PWD:/go/src/jump-jump \
-w /go/src/jump-jump \
jump-jump-dev
```
这段命令就不做过多的解释了，个别不明意义的参数可以去看看docker官方文档，不出意外，你应该会看到如下图的输出：
[![beego启动图](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8VGLhiazF8e8q9Kevu8HiaYEL2m2gqiawJ6RcxtNoic03ZW6KvorMUwtd3miblTE60cMrXL7qnZ5DAmFyg/0?wx_fmt=png)](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8VGLhiazF8e8q9Kevu8HiaYEL2m2gqiawJ6RcxtNoic03ZW6KvorMUwtd3miblTE60cMrXL7qnZ5DAmFyg/0?wx_fmt=png)
这个时候你就可以通过浏览器访问`http://localhost:8080`，你应该会看到：
[![beego默认页面](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8VGLhiazF8e8q9Kevu8HiaYELmH9vAeekfI9F9JaJhZIDPhvFEzg5XqQjicFibpAIM3icvDlJMJsc0u8gA/0?wx_fmt=png)](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8VGLhiazF8e8q9Kevu8HiaYELmH9vAeekfI9F9JaJhZIDPhvFEzg5XqQjicFibpAIM3icvDlJMJsc0u8gA/0?wx_fmt=png)
如果现在你修改项目里的go文件，在Docker运行的beego程序则会自动重新编译。

### 第3步 编写短链接系统逻辑
其实，整篇文章中，这一部分可以说是最重要也最不重要的，说重要，毕竟这篇文章就是说要做一个短链接系统，说不重要，逻辑这玩意儿大部分人都能自己写出来。这篇文章的重点的确不在这里，毕竟学会了搭环境的思路后，你要写什么系统都是可以的，但是系统源码地址还是得贴出来，[戳这里](https://github.com/jwma/jump-jump)。

如果打开源码仓库，你会发现里面有个Dockerfile，这个Dockerfile是用来把jump-jump打包成镜像的，也就是说运行镜像生成的容器就可以直接启动jump-jump了：
```
# 通过Dockerfile生成应用镜像
git clone https://github.com/jwma/jump-jump.git
cd jump-jump
docker build -t jump-jump .
```
这样，本地就生成了一个jump-jump镜像了，下面运行这个镜像试试看：
```
docker run -it --rm \
--name j2-prod \
--link mj-redis:mj-redis \
-p 8080:8080 \
-e J2RunMode="prod" \
-e J2RedisAddr="mj-redis:6379" \
jump-jump
```
你会想`--link mj-redis:mj-redis`是什么意思，这个其实是我本地启动的一个Redis服务容器，跟上一篇文章提到的MySQL数据库服务容器一个意思，怎么跑起来的就交给大家自己操作了，Docker通过`--link`，就可以搭建容器间的连接，这样jump-jump起的容器就可以访问Redis了，通过这种方式，其实你可能已经有点体会了，Docker把每个可以单独运行的服务都通过容器来运行，然后提供了相应的连接方式，让容器间可以互相通信，稍微搭建一下，你可能就能拉出一张一定规模的服务网来。

虽然具体业务逻辑没说，但我在短短的几个小时的开发过程中，也踩了些坑也领悟到了beego的一些“真谛”，这些或许下次再写一篇文章分享吧，如果对jump-jump感兴趣，可以继续留意仓库的更新哦。

## 啰里啰嗦
Emm...我目前还没有把这个系统部署到自己的服务器进行使用，因为我发现自己没有一个比较短的域名，用起来不够酷。
