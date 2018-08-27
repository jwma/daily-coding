## 相关内容
- [让Docker来为你干点事儿](https://mp.weixin.qq.com/s?__biz=Mzg5ODAwODM0Mg==&mid=2247483658&idx=1&sn=7f22ecb5fef010e34232cc1bf68823f4&chksm=c0685573f71fdc65ee91238a07951cfcdc2e6f72de26e973993594560a568feb094c280e7610&token=347835602&lang=zh_CN#rd)
- [Docker+Go搭建短链接系统](https://mp.weixin.qq.com/s?__biz=Mzg5ODAwODM0Mg==&mid=2247483668&idx=1&sn=79b0660cf04b42e3b60a0f69d30e9bf4&chksm=c068556df71fdc7b6b70d8aab3711be205d6d5e6ec4a748c521e0671786f80926a31bee86c8e&token=347835602&lang=zh_CN#rd)

## 唠叨唠叨
如果看了之前两篇关于 Docker 的文章，我相信对一些童鞋而言已经解决了一些在搭建项目的开发环境的麻烦事儿了，但，这远远不够的。

前两篇文章的内容，的确改变了我们以往开发环境搭建的方式，但在实际项目中，还是存在着一些不便利的地方：
1. 镜像是通过 Dockerfile 写好了，但是在 `docker run` 启动容器时还需要加入一大堆参数，在开发过程中如需频繁运行这些命令，这无疑是一个让人抓狂的事情；
2. 虽然感觉自己比过往优秀了，但为什么有种刀耕火种的感觉？在某个项目中，我需要启动数据库服务容器、缓存服务容器，最后到应用服务容器，如果项目依赖的服务越多，你就越会有这种感觉。

既然有这些让人抓狂的问题，那么我们就需要一个合适的工具来解决这些问题，而 Docker 也正是为了解决这些问题（不止上文提到的问题），于是 Compose 就被生了出来。

## Docker Compose
在了解了 Compose 能够解决什么问题之后，我们再来上手 Compose 就简单很多了。
这里先祭出 Compose 的官方文档地址（https://docs.docker.com/compose），学习开源技术，最靠谱的还是看官方文档。

简单来说，Compose 就是一个用来定义和运行多个 Docker 容器的应用，而我们可以通过编写 `docker-compose.yml`（默认名字）来定义我们的服务，这些服务就组成了一个项目（`project`），有了写好的 `docker-compose.yml` 后，我们就可以通过 `docker-compose` 来启动、停止我们的这组容器了。

Compose 的配置文件是 YAML 文件，相信绝大部分童鞋都用过这种文件了，如果还没尝试用过 YAML 文件的童鞋，还真得去补一下了。

## 撸起袖子就是干
嘿咻嘿咻！

Compose 的安装方法，本文就不说了，官方文档提供了各个平台的安装方法，总有一种适合你！

说时迟那时快，我已经把 [Docker+Go搭建短链接系统](https://mp.weixin.qq.com/s?__biz=Mzg5ODAwODM0Mg==&mid=2247483668&idx=1&sn=79b0660cf04b42e3b60a0f69d30e9bf4&chksm=c068556df71fdc7b6b70d8aab3711be205d6d5e6ec4a748c521e0671786f80926a31bee86c8e&token=347835602&lang=zh_CN#rd) 的 `jump-jump` 项目改造了，现在可以通过 Compose 来快速创建开发环境和生成环境了，源码地址（https://github.com/jwma/jump-jump）。

接下来讲讲 `jump-jump` 如何使用 Compose 来快速搭建开发环境吧。

### 第1步 修改开发环境的 Dockerfile
`jump-jump`开发环境的 Dockerfile 名字为 Dockerfile-dev，内容如下：
```
FROM golang:1.9   
RUN go get github.com/astaxie/beego github.com/beego/bee github.com/go-redis/redis
WORKDIR /go/src/github.com/jwma/jump-jump/app
# EXPOSE 8080 
# CMD ["bee", "run"]
```
这里修改的地方，是把 `EXPOSE` 和 `CMD` 都去掉了，这两行我们后面就交给 Compose 来处理了。

### 第2步 编写 docker-compose.yml 文件
`jump-jump`开发环境的 `docker-compose.yml` 名字为 `docker-compose-dev.yml`，内容如下：

[![docker-compose-dev.yml](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8V0p3KlEaFEKlelM25LibmNyx3b07lIOkvZlkHTGUE3HY4enDOAjz5MPg2D9wymFyLbTUBNzmKYFyA/0?wx_fmt=png)](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8V0p3KlEaFEKlelM25LibmNyx3b07lIOkvZlkHTGUE3HY4enDOAjz5MPg2D9wymFyLbTUBNzmKYFyA/0?wx_fmt=png)
得益于 YAML 文件的格式，我们可以马上看到 `services` 内包含着 `web` 和 `redis`，而这，正是上文提到的这个 `project` 的服务组成部分，这个 `project` 由 `web` 容器和 `redis` 容器组成，而每个容器，又可以设置自己独立的配置：
- 可以指定某个容器是通过 Dockerfile 产生，也可以是通过某个镜像直接产生；
- 可以指定某个容器对于其他容器的依赖关系，例如 `web` 依赖于 `redis`；
- 可以指定容器名称；
- 可以把宿主机的指定端口映射到容器的指定端口；
- 可以设置环境变量；
- 可以挂载卷；
- 可以设置 `entrypoint`。

有了 Compose，我们可以清晰的描述我们的项目的容器，不再是每个容器都单独的跑起来，且定义的这组容器可以互相通信，通过 `redis` 服务的这个名称，`web` 容器可以直接用在Redis的连接地址上。

### 第3步 通过 Compose 启动项目
万事俱备，现在只需要在命令行上敲一条简单的命令就能把过去需要输入 N 条命令才能干的事情给干了：
```
docker-compose -f docker-compose-dev.yml up
```
运行成功后，会看到如下图的输出：
[![docker-compose up](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8V0p3KlEaFEKlelM25LibmNyIzCTt9qicJs2tLssQNcPcB67MVmNe0KmAgBZ1FHlANiazx0FFFIEmgzw/0?wx_fmt=png)](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8V0p3KlEaFEKlelM25LibmNyIzCTt9qicJs2tLssQNcPcB67MVmNe0KmAgBZ1FHlANiazx0FFFIEmgzw/0?wx_fmt=png)
这个时候我们去访问 `http://localhost:8081`，`jump-jump`已经正常运作了。

如果想停掉这个项目：
```
docker-compose -f docker-compose-dev.yml down --volumes
```

到这里，我们已经使用 Compose 把 `jump-jump` 的开发环境搭建方式升级了，使用起来简单，一句 `up` 一句 `down`，如果 Compose 的配置文件是默认名字的话，命令会更简单：
```
# 启动
docker-compose up --build

# 停止并清除容器
docker-compose down --volumes
```
## 死不断气，再唠叨两句
Compose 已经让我们在搭建环境的时候多了几分自信，更多的使用技巧得靠自己去发掘了。

每个工具或是应用，都有自己的适用场景，（https://docs.docker.com/compose/overview/#common-use-cases）是官方给出的 Compose 的适用场景，本文还没有100%把 Compose 用上，怎么说呢，对症下药，着眼实际问题，实用，这些一向是我的做事方式（很酷.gif）。

得赶紧买一个短域名把`jump-jump`给用上才行。
