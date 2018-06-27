Docker笔记
===

## Hello docker
```
docker run ubuntu:15.10 /bin/echo "Hello docker"
```
以上命令完整的意思可以解释为：Docker 以 ubuntu15.10 镜像创建一个新容器，然后在容器里执行 bin/echo "Hello world"，然后输出结果。

当运行容器时，使用的镜像如果在本地中不存在，docker 就会自动从 docker 镜像仓库中下载，默认是从 Docker Hub 公共镜像源下载。

### 运行交互式的容器
```
docker run -i -t ubuntu:15.10  /bin/bash
```
- `-t` 在新容器内指定一个伪终端或终端
- `-i` 允许你对容器内的标准输入进行交互

## 更多
`docker ps` 查看正在运行的容器

```
docker run --name myapp -d -P xxx python app.py
```
- `--name` 指定了容器的名称，不指定docker会生成随机的名称
- `-d` 让容器后台运行
- `-P` 将容器内部使用的网络端口映射到我们使用的主机上

`docker stop myapp && docker rm myapp` 停止myapp容器，然后删除myapp容器
`docker logs -f myapp` 查看myapp容器日志，`-f`参数效果如同`tail -f`
`docker top myapp` 查看myapp容器内部运行的进程

## 镜像
`docker pull xxx` 拉取一个镜像到本地
`docker search xxx` 查找镜像
