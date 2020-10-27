让Docker来为你干点事儿
===

## 唠叨唠叨
程序员常常会为搭建开发环境而重复劳动，如新同事入职后配的新电脑，啥软件都没有更别说开发环境了，往往要搭建一套符合公司开发要求的开发环境需要花费一定时间，又如前端开发的童鞋和后端开发的童鞋需要的开发环境不一样，麻烦事比能看到的往往要多很多，虽然没有银弹，但每个团队都可以使用合适的工具（Docker）来减少这些麻烦事。

Docker在我看来，已经到了不得不会的地步了，适用的场景很多，本文讲的是用Docker来创建一个MySQL数据库服务，用MySQL来举例的原因有3个：
1. 无论是什么语言，随便写一个小项目其实都需要用到数据库；
2. Docker上有MySQL官方提供的镜像，看到官方二字感觉很放心；
3. 不要以为Docker离自己很远。


## 撸起袖子就是干
默认大家的前置知识都有，有啥看不懂的回头赶紧补起来。

### Docker的安装
这种重要的说明，我觉得还是交给Docker官方文档比较稳，这里就不说了。

### Docker的一些基础概念
- 镜像（Image），不解释你懂的；
- 容器（Container），通过镜像启动，里面可以是运行环境，可以是你的应用程序，甚至可以是...
- 镜像仓库（Registry），官方提供了一个放着很多镜像的一个仓库，你可以从上面找镜像，也可以贡献镜像到上面去。

### 创建MySQL服务
如果一些概念的东西还没弄懂，不如一起先来看看实际怎么操作吧。

#### 第1步 搜索和拉取MySQL镜像：
搜索mysql镜像，你会看到一个列表结果，列表中OFFICIAL这一列是OK的，则表明是官方镜像。
```
docker search mysql
```
从镜像仓库拉取mysql:5.7，`:5.7`是指明要拉取这个镜像的哪个tag的版本，具体有哪些版本，可以到这个镜像的官网页面看看。
```
docker pull mysql:5.7
```
大部分刚安装完Docker还没有进行任何配置的童鞋，或许会说拉取镜像怎么这么慢，这个时候配置一个国内镜像仓库的地址即可，官方的阿里的网易的都可以，Mac端的童鞋可以按照下图来配置：
[![配置镜像仓库源](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8VJVL470Quib1rAC8bLFvjv9mNBmblrv3ibKNicwQs5fHPgBbgT5DfvtBOkEd0ff8Hspic5MOtEbyxic4Q/0?wx_fmt=png)](https://mmbiz.qpic.cn/mmbiz_png/oS1Ryib0qL8VJVL470Quib1rAC8bLFvjv9mNBmblrv3ibKNicwQs5fHPgBbgT5DfvtBOkEd0ff8Hspic5MOtEbyxic4Q/0?wx_fmt=png)

#### 第2步 启动MySQL服务容器
```
docker run --name db -e MYSQL_ROOT_PASSWORD=your_password -p 3306:3306 -d mysql:5.7
```
使用`docker run`启动容器，这个命令可以接收的参数项有很多，运行`docker run --help`你或许会吓一跳，但别紧张，目前用到的只是一小部分而且很好理解：
- `--name db`，指明这个容器的名称为db；
- `-e MYSQL_ROOT_PASSWORD=your_password`，为具体的环境变量赋值，这里是设置root用户的密码；
- `-p 3306:3306`，端口映射，格式为：宿主机端口:容器端口，这里是把宿主机的3306端口映射到容器的3306端口；
- `-d`，后台运行这个容器，并返回这个容器的ID；
- 最后的mysql:5.7就是这个容器所用到的镜像。

到这里，其实我们已经使用Docker启动了一个MySQL服务了，如果我们使用一些数据库GUI工具或者是使用某个编程语言对刚刚起动的MySQL数据库进行连接，会发现是可以正常运作了。

但我们的工作到这里还没结束，我们先利用数据库GUI工具在数据库上创建一些数据库、数据表、插入一些数据，这个时候我们把容器停了，然后我们再按照刚刚的命令启动一个db容器，我们再打开GUI，你会发现，刚刚对数据库的所有操作都没了，其实这很好理解，因为Docker的容器是不会为你保存运行时的改动的，除非你自己对一个容器进行commit，那么要怎么办？

在解决刚刚那个问题前，先来看看怎么停止一个容器吧。
```
# 查看所有运行过的容器
docker ps -a

# 得到一个如下的数据表格
CONTAINER ID    IMAGE       COMMAND     CREATED     STATUS      PORTS       NAMES

# 可以通过CONTAINER ID或者NAMES来停止某个容器
docker stop db
```
此时再次运行`docker ps -a`，会发现db容器还在，只是状态已经不是运行中，想清理干净点，可以运行`docker rm db`进行删除。

#### 第3步 存储数据
既然容器不会保存运行时的数据，那么我们只要把数据单独保存不就好了？
```
# 在宿主机合适的位置创建一个存放这个MySQL服务的数据的目录
cd ~ && mkdir my_db

docker run --name db -v ~/my_db:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=your_password -p 3306:3306 -d mysql:5.7
```
在启动容器的时候，只是多加了`-v ~/my_db:/var/lib/mysql`，意思是把宿主机的`~/my_db`目录挂载到容器的`/var/lib/mysql`目录。

当容器启动完成，我们可以去`~/my_db`目录查看一下，会发现里面生成了MySQL数据库运行的数据文件及其他所需文件，现在我们再去对数据库做操作后把容器停止，所有数据都还会被保存在宿主机，一切看起来都是那么简单自然。

## 再唠唠叨叨
其实，要使用Docker创建一个MySQL数据库服务真的很简单，甚至我可以把上文的3个步骤合成一步，即只运行第3步的那条命令，Docker就会自动为你拉取镜像，然后按部就班的帮你启动容器挂载数据目录等等，本文啰啰嗦嗦的也只是为了把其中的步骤拆解开来好让第一次接触Docker的童鞋比较好理解。

到这里，不难发现Docker在解决本文最开头的场景简直再合适不过了，只要用好Docker，我相信很多麻烦的问题都会得到解决。

