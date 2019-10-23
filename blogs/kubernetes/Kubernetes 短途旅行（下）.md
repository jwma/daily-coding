[Kubernetes 短途旅行（上）](https://juejin.im/post/5dae8154518825044a1309e9)

本文会通过一个中文情绪分析的应用（以下简称 SA）把 K8s 的一些基础概念穿插讲一讲，接着我们会进行一次 UI 的更新以便体验一下 K8s 的滚动更新，最后我们还会进行一次回滚，把 UI 的更新给撤销掉并回滚到上一个版本。

那么接下来就按照这个剧本开始吧。

## 中文情绪分析的应用 SA

_仓库地址：[github.com/jwma/sentiment-analyzer](https://github.com/jwma/sentiment-analyzer)_

SA 分为三个部分：

![](https://user-gold-cdn.xitu.io/2019/10/22/16df1b720207f69c?w=777&h=776&f=png&s=198578)

- sa-frontend，使用 Vue.js 开发的前端应用并部署在 Nginx，提供让用户交互的界面；
- sa-webapp，使用 Go 语言开发的 API 服务，直接面向前端应用；
- sa-logic，使用 Python 开发的情绪分析服务，面向 API 服务，对前端应用不可见。

## 部署到 K8s

如果我们要将 SA 部署到 K8s 集群，我们需要先准备一些必需品：

1. K8s 集群;
2. 容器镜像；
3. Deployment 和 Service 配置文件；
4. 创建 Deployment 和 Service 资源。

### 1. K8s 集群

参考上一篇文章，你会找到适合你自己的途径。这里我会使用 Minikube 为我启动一个本地的单节点集群。

### 2. 容器镜像

容器化的细节本文就不展开了，可以参考项目源码内各部分的 Dockerfile，下面讲讲构建镜像的相关内容。

一般来说，我们会把我们的容器镜像推送到一个镜像仓库如 DockerHub，但由于我们的集群就是在本地，所以我们可以重用 Minikube 内置的 Docker，这样我们就不需要浪费时间去推送镜像和拉取镜像了，便于我们在本地体验。

这样使用时需要注意，在为镜像打 tag 时，需要使用 `:latest` 以外的名字，因为当你使用了 `:latest` 意味着镜像拉取策略也会被修改为 `Always`，在镜像不存在于默认的 Docker 镜像仓库（一般为 DockerHub）时，会引发 `ErrImagePull` 错误。

我们可以这样使用 Minikube 内置的 Docker：

```shell
eval $(minikube docker-env)
```

此时命令行的 Docker 就是 Minikube 的 Docker 了，接着我们就可以构建镜像了：

```shell
# 切换到源码目录
cd /path/to/sentiment-analyzer

# 构建 sa-logic 镜像
docker build -t sa-logic:v1.0.0 sa-logic

# 成功的话会看到如下输出
# Successfully tagged sa-logic:v1.0.0

# 构建 sa-webapp 镜像
docker build -t sa-webapp:v1.0.0 sa-webapp

# 成功的话会看到如下输出
# Successfully tagged sa-webapp:v1.0.0

# 暂时无法构建 sa-frontend
# 因为其依赖了 sa-webapp 暴露的通信地址
# 需要等我们创建了 sa-webapp service 之后再构建
```

### 3.  Deployment 和 Service 配置文件

这一部分内容比较无聊，着急的可以先跳过。

查看源码的 infrastructure 目录，其中包含了 Deployment 和 Service 配置文件。

以 sa-webapp 的 Deployment 举例：

![](https://user-gold-cdn.xitu.io/2019/10/22/16df1b7947e87552?w=1080&h=994&f=png&s=481047)

- **#1**  `apiVersion` 指定了该资源对象所对应的 API 版本，K8s 支持多个 API 版本，K8s 团队选择在 API 级别进行版本化，而不是在资源或字段级别进行版本化，以确保 API 提供清晰，一致的系统资源和行为视图，并控制对已废止的 API 和/或实验性 API 的访问；
- **#2** `kind` 指定了该资源的类型为 Deployment；
- **#3** `metadata` K8s 的资源对象都拥有通用的元数据，这里指定了名称和添加了一个键为 app 值为 sa-webapp 的标签，后续需要用来匹配对应的 Service；
- **#7**  `spec` 描述你期望的 Deployment 的状态；
- **#8** `spec.replicas` 指定期望的 Pod 数量，默认值是 1；
- **#9** `spec.selector` 指定了 Deployment 管理 Pod 的范围，通过标签进行匹配；
- **#12** `spec.template` 指定 PodTemplate，描述了 Pod 的细节，这里为 Pod 添加了一个键为 app 值为 sa-webapp 的标签，也指明了 Pod 的名字及其实用的镜像，为了让容器能正常运行，还设置了容器所需 的环境变量，最后还暴露了容器的端口。

以 sa-webapp 的 Service 举例：

![](https://user-gold-cdn.xitu.io/2019/10/22/16df1b7cda6b82f0?w=1080&h=844&f=png&s=390432)

- **#2** `kind` 指定了该资源的类型为 Service；
- **#8** `spec.selector` 通过标签选择器匹配 sa-webapp Deployment；
- **#10** `spec.type` 指定 Service 类型为 LoadBalancer，也就说来自外部的流量会通过这个 Service 的负载均衡器然后打到匹配的 Pod 上；
- **#11** `spec.ports` 指定端口的映射关系，把负载均衡器的 80 端口映射到 Pod 的 8080 端口。

#### 什么是 Deployment 和 Service?

在本文的例子中，除了认识 Deployment 和 Service 外，你还需要认识 Pod 和 RS（Replica Set），因为他们的互相结合才使得我们能够把 SA 给运作起来。

实质上，它们都是 K8s 的 API 对象，只是他们负责的工作内容不一样而已。

##### Pod

Pod 是 K8s 应用的基础执行单元，它是你创建或部署的最小最简单的 K8s 单元。一个 Pod 通常包含的是一个应用容器（有时候会是多个容器）。结合上文，我们在 Deployment 声明了 PodTemplate，也就是说我们的 Pod 会按照我们的声明运行我们想要运行的容器。

##### RS

RS 保证 Pod 的高可用。结合上文，我们在 Deployment 声明了 `replicas`，我们期望运行两个 Pod，而实际运行中的 Pod 的数量就是通过  RS 进行保障的。

##### Deployment

Deployment 可以创建/更新一个服务，也可以滚动更新服务。我们通过配置文件，可以告诉 K8s 集群我们期望应用的运行状态，结合 Pod 我们能把应用运行起来，结合 RS 我们能保障 Pod 的可用性。一次对 Deployment 的操作，就是通过操作相关的 API 对象来更新应用的运行状态以达到我们的期望。

##### Service

通过上面的几个 API 对象，我们已经保证应用能够正常运作，但没有解决如何访问这些服务的问题，Service 就是用来解决这个问题的。

### 4. 创建 Deployment 和 Service 资源

在 K8s 上创建 API 对象的资源很简单，我们可以使用统一的方式进行创建：

```shell
# 切换到源码目录
cd /path/to/sentiment-analyzer

# 创建 sa-logic 的 Deployment、Service
kubectl apply -f infrastructure/deployment/sa-logic.yaml

# 查看 sa-logic 对应的 Pod 是否正常运作
kubectl get pods -l app=sa-logic

# 创建 sa-logic 的 Service
kubectl apply -f infrastructure/service/sa-logic.yaml

# 查看 sa-logic 对应的 Service
kubectl get service -l app=sa-logic

# 创建 sa-webapp 的 Deployment、Service
kubectl apply -f infrastructure/deployment/sa-webapp.yaml
kubectl apply -f infrastructure/service/sa-webapp.yaml
```

到这里，我们就把 sa-logic 和 sa-webapp 部署到 K8s 集群了，sa-webapp 是一个对外可见的服务，所以我们在部署 sa-frontend 之前，可以使用 postman 或者 curl 来访问以下 sa-webapp 看看。

由于我们使用的是 Minikube，所以为了获取 sa-webapp 服务的通信地址，我们需要：

```shell
minikube service sa-webapp-service --url
```

我们会得到一个 URL，如：`http://192.168.99.105:31861`，接下来我们用 cURL 工具测试下 sa-webapp 的接口：

```shell
# 发送请求
curl --request POST \
  --url http://192.168.99.105:31861/analyse \
  --header 'Content-Type: application/json' \
  --data '{"sentence": "非常棒"}'

# 响应结果
{"sentence":"非常棒","level":9}
```

我们成功的得到了结果。现在我们已经得到了正确的 sa-webapp 的通信地址了，所以我们可以开始构建 sa-frontend 镜像然后部署了：

```shell
# 切换到源码目录
cd /path/to/sentiment-analyzer

docker build -t sa-frontend:v1.0.0 --build-arg VUE_APP_API_HOST=http://192.168.99.105:31861 sa-frontend

kubectl apply -f infrastructure/deployment/sa-frontend.yaml
kubectl apply -f infrastructure/service/sa-frontend.yaml
```

然后我们就可以获取 sa-frontend 的访问 URL 了：

```shell
# 这次不加 --url，会自动在浏览器打开
minikube service sa-frontend-service
```

你也可以像我这样玩一下：


![sa-frontend](https://user-gold-cdn.xitu.io/2019/10/22/16df2b42d9f457dd?w=640&h=428&f=gif&s=817523)

## 滚动更新

在 K8s 上要实现滚动更新是一件非常简单的事情。
我们接下来会更新 sa-frontend，因为我觉得每次提交完一个句子后，Emoji 出现的太突兀，缺乏了一些动感，所以我接下来会使用 animate.css 为 Emoji 加一个动画，让画面看起来更有动感一些。

来看看整个流程吧：

1. 修改代码；
2. 构建一个新的 sa-frontend 镜像；
3. 更新 sa-frontend Deployment 配置文件；
4. 向 K8s 提交 Deployment；
5. 查看结果。

### 1. 修改代码

这里不是重点，就跳过了。

### 2. 构建一个新的 sa-frontend 镜像

我们更新了代码，所以我们也会跟着构建一个新的镜像，镜像版本号取 v1.1.0。

```shell
# 切换到源码目录
cd /path/to/sentiment-analyzer

docker build -t sa-frontend:v1.1.0 --build-arg VUE_APP_API_HOST=http://192.168.99.105:31861 sa-frontend/
```

### 3. 更新 sa-frontend Deployment

```shell
# ...省略
# 镜像修改为刚刚构建好的 v1.1.0
image: sa-frontend:v1.1.0
# ...省略
```

### 4. 向 K8s 提交 Deployment

跟第一次部署 sa-frontend 一样，我们向 K8s 集群提交了我们的 Deployment 配置文件。

```shell
kubectl apply -f infrastructure/deployment/sa-frontend.yaml
```

### 5. 查看结果

我感觉这样就好多了呢。

在这里，你可以不去思考 K8s 的滚动更新是怎么做的，但我认为往后你应该要去了解这件事情，这对你理解 K8s 的各个 API 对象很有帮助。

![](https://user-gold-cdn.xitu.io/2019/10/22/16df2b4a7f99bb70?w=640&h=474&f=gif&s=1157643)

## 回滚

如果你是一个比较安静的孩纸，不喜欢这么动感，你可以回滚到上一个版本：

```shell
kubectl rollout undo deployment sa-frontend-deployment
```

除了回滚到上一个版本，你还能回滚到指定的版本，这里就不展开了，我相信如果要用到的时候你肯定会去翻文档的。

## 短途旅行的终点

我们到达了这次短途旅行的终点，就像真正的旅行一样，这个终点往往会是原点，我们不断的旅行，我们见识到了不同的风景，认识到了不同的朋友，体验了不同的风情，虽然我们又回到了原点，但我们不断积累阅历，让我们面对下一个挑战更具勇气，让我们走得更远看得更广。

希望这两篇文章，能带你走马观花看看 K8s，如果能在你的脑中留下 K8s 好像真的不错哦，我想我就满足了。


![](https://user-gold-cdn.xitu.io/2019/10/22/16df1b8e7b255caf?w=258&h=258&f=png&s=28963)

