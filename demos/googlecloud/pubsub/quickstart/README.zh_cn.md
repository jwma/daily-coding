# quickstart

### 其他语言
- [英文](README.md "英文 READEMD")

### 构建
`docker-compose up -d --build`

### 启动 Subscriber
`docker-compose run demo python pubsub.py start_subscriber`

打印出接收到的所有消息。

### 发布消息
发布一条 "hello" 消息

`docker-compose run demo python pubsub.py publish hello`

发布一条 "hi" 消息

`docker-compose run demo python pubsub.py publish hi`

### 停止
`docker-compose down -v`
