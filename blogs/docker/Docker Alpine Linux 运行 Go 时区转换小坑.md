# Docker Alpine Linux 运行 Go 时区转换小坑

## 好久不见

拖更王更新了，尴尬而不失礼貌的微笑 :) 感谢那些没有取关的朋友们！你们的坚持是对的！

## 正文

出于各种原因，总会有需要编写时区转换代码的时候，好巧不巧的，最近我刚好在做一个需求的时候就需要做时区转换。

呵，真巧（不踩坑，哪来这篇文章...）。

### 准备工作

下面通过简单的十来行代码给大家做个演示，如果你把代码拷贝到你本地运行，我相信都能够正常运行的。

```go
// main.go
package main

import (
	"fmt"
	"time"
)

func main() {
	now := time.Now()

	fmt.Printf("Time: %v, Location: %v\n", now, now.Location())

	shanghai, err := time.LoadLocation("Asia/Shanghai")

	if err != nil {
		panic(err)
	}

	shanghaiNow := now.In(shanghai)
	fmt.Printf("Time: %v, Location: %v\n", shanghaiNow, shanghaiNow)
}
```

正常运行的话，你大概能看见如下输出：

```
Time: 2020-10-26 18:32:34.63303 +0800 CST m=+0.000066515, Location: Local
Time: 2020-10-26 18:32:34.63303 +0800 CST, Location: 2020-10-26 18:32:34.63303 +0800 CST
```

但，当这个程序放到 Docker alpine 容器运行的时候，就会发生一个你意想不到的错误（心里默念：草率了）。

既然要放在容器运行，那就先看看 Dockerfile：

```dockerfile
FROM golang:1.13 as builder

WORKDIR /app
COPY . .
RUN go build -o timelocation .

FROM alpine:latest

WORKDIR /app
COPY --from=builder /app/timelocation /app

ENTRYPOINT ["./timelocation"]
```

简单来说，就是使用 golang:1.13 来构建出我们的 **timelocation** 程序，然后再拷贝到 alpine（多阶段构建，是一种常用的容器镜像构建手段，这样构建出来的容器镜像就会特别小，易于分发，节省部署时间，这里暂时不展开讲）。

我们的目录现在有这些文件：
```shell
.
├── Dockerfile
└── main.go
```

打开命令行，在项目目录运行 `docker build -t timelocation .`，最终我们会得到一个名为 **timelocation** 的镜像。

### 错误，它来了！

`docker run --rm timelocation` 就是这次的宝藏密码，来吧伙计！运行它！

```shell
➜ docker run --rm timelocation
Time: 2020-10-26 10:33:44.757997 +0000 UTC m=+0.000131401, Location: UTC
panic: unknown time zone Asia/Shanghai

goroutine 1 [running]:
main.main()
        /app/main.go:16 +0x35c
```

错误，它来了！我们能看见，第一个打印语句是能够正常打印，但第二个没打印出来，中间发生了一个 `unknown time zone Asia/Shanghai` 错误，这下你不就急了吗？你心想：不对啊，咋了这是，是 Aisa 不对呀还是 Shanghai 不对，也没打错字呀！看着屏幕来了一句——“我本地明明能够正常运行的呀！”

### 掀起错误的头盖骨！

上面那个慌张的情形，像不像平时写出 BUG 的你？没事儿，既然有错，那必然有原因，我们一起来掀起这个错误的头盖骨，看个究竟！

首先我们非常明确，**Asia/Shanghai** 这个字符串肯定是没错的，但程序却说不认识它，奇怪奇怪。这个错误是由 `time.LoadLocation()` 方法产生的，点开这个方法看一下吧：

```go
// $GOROOT/src/time/zoneinfo.go

// LoadLocation returns the Location with the given name.
//
// If the name is "" or "UTC", LoadLocation returns UTC.
// If the name is "Local", LoadLocation returns Local.
//
// Otherwise, the name is taken to be a location name corresponding to a file
// in the IANA Time Zone database, such as "America/New_York".
//
// The time zone database needed by LoadLocation may not be
// present on all systems, especially non-Unix systems.
// LoadLocation looks in the directory or uncompressed zip file
// named by the ZONEINFO environment variable, if any, then looks in
// known installation locations on Unix systems,
// and finally looks in $GOROOT/lib/time/zoneinfo.zip.
func LoadLocation(name string) (*Location, error) {
	// 省略实际代码...
}
```

问了一下英语课代表，他让我滚...

不闹了，简单说一下吧，前面两种特殊情况，它会直接返回对应的 `*Location`，但如果是其他情况，程序会去时区数据库查询，尝试获得对应的 `*Location`。

我们的 **Asia/Shanghai** 肯定不属于前面两种特殊情况，所以程序会去时区数据库查询，但程序告诉我们不认识这个时区，这里就存在两种可能性，一，时区数据库真的不包含这个名称的时区，一般就是打错字导致的；二，时区数据库根本就不存在，如果说连说数据库本身都不存在，那程序又怎么可能会认识你传过来的名称呢？

到这里我们就可以 99.99% 确定是程序运行时缺少了时区数据库才导致它不认识我们的 **Asia/Shanghai**。

后面还说道——不是所有操作系统都有这个时区数据库，特别是非 Unix 系统（Mac 党表示，都怪自己用 Mac，要不然我早就知道会有这种坑，哼）。到这里就要清楚一点了，Docker alpine 是不包含这个时区数据库的，不要问我为什么要用这个系统，人家整个系统大小能做到仅仅 5MB 左右，你还想怎样！

### 解决这个错误！

既然已经了解了为什么出错，那我们就能够解决它！在 `time.LoadLocation()` 方法文档的最后写道——该方法会去查找 `ZONEINFO` 环境变量指向的目录或是未解压的 zip 文件，如果程序运行时没有找到这个环境变量，那么它就会去一些默认的安装位置找，最后的最后，程序会去 `$GOROOT/lib/time` 找 `zoneinfo.zip`。 

你或许会想，不是还有最后的最后的手段吗？为什么还是找不到？朋友，要醒醒哦，因为你在 alpine 运行程序，alpine 又没有安装 Go，那怎么会有 `$GOROOT` 呢？

既然 alpine 没有这个时区数据库，那么程序去找的所有可能的安装位置都不会存在，所以我们有两种最快的途径去解决这个问题：

#### 一，在系统层级安装时区数据库

因为我不是用这种方法，所以你可以自行去查一下资料，我想无非就是 `apk add xxxx` 吧。

#### 二，构建应用镜像时，加入时区数据库

我用的是这种方法，所以这里可以展开说一下。

更新 Dockerfile：

```dockerfile
FROM golang:1.13 as builder

WORKDIR /app
COPY . .
RUN go build -o timelocation .

FROM alpine:latest

# 设置依赖的环境变量
ENV ZONEINFO=/app/zoneinfo.zip

WORKDIR /app
COPY --from=builder /app/timelocation /app

# 拷贝时区数据库
COPY --from=builder /usr/local/go/lib/time/zoneinfo.zip /app

ENTRYPOINT ["./timelocation"]
```

改动的地方加了注释，首先设置 `time.LoadLocation()` 方法需要使用的环境变量，并设置为稍后时区数据库的路径，然后在 golang 镜像中拷贝时区数据库到我们的应用镜像中，目标路径要和环境变量的路径对上。

解题思路：

1. 我不知道哪里有时区数据库下载怎么办？`time.LoadLocation()` 方法文档告诉你哪里有了；
2. 时区数据库什么时候放进项目合适？非 Docker 运行时不需要，那我们就在镜像构建的时候才拷贝到应用镜像里面去，本地也不会有多余的文件，省心；
3. `ZONEINFO` 环境变量放在 Dockerfile 基本一辈子都不会改动，省力！

当我们重新构建镜像，然后再次运行，就能看见预期的输出结果了，真开心！:)

## 上价值

可能最近脱口秀看多了吧，感觉最后要上价值，才算是一篇完整的文章...

说实话，这个坑是我上周踩的，当时遇到问题到解决问题，前后的时间真的很短，可能我码这篇文章的时间足够我解决这问题上百次了，问题可能很小，解决起来也没啥难度，但思考的过程和思路，我还是想和大家分享一下的。

当你使用新技术、新语言、新框架、新系统都可能会遇到类似的问题，其核心就在于你对其不够了解，又没有花很多时间去摸索，这就好比你去追女生，你喜欢她，但你总是送一些她不喜欢的东西，什么？你说你从来不追女生？哦我的上帝，你当我什么都没有说吧。

下次见，我的朋友们。