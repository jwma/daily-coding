# quickstart

### Build
`docker-compose up -d --build`

### Start a subscriber
`docker-compose run demo python pubsub.py start_subscriber`

If any message is received, it will be printed out.

### Publish message
Publish "hello" message.
`docker-compose run demo python pubsub.py publish hello`

Publish "hi" message.
`docker-compose run demo python pubsub.py publish hi`

### Down
`docker-compose down -v`
