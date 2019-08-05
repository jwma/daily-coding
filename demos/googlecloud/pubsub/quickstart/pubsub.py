import sys
import time

from google.cloud import pubsub_v1
from google.api_core.exceptions import AlreadyExists
from google.cloud.pubsub_v1.subscriber.message import Message

publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()


def get_topic_path(name: str):
    return f'projects/demo/topics/{name}'


def get_subscription_path(name: str):
    return f'projects/demo/subscriptions/{name}'


def create_topic(name: str):
    publisher.create_topic(get_topic_path(name))


def publish_message(topic: str, text_msg: str):
    publisher.publish(get_topic_path(topic), text_msg.encode('utf-8'))


def create_subscription(topic: str, name: str):
    subscription_name = get_subscription_path(name)
    subscriber.create_subscription(name=subscription_name, topic=get_topic_path(topic))
    return subscription_name


def callback(message: Message):
    print('Receive text message: ' + message.data.decode('utf8'))
    message.ack()


def subscribe(name: str):
    subscriber.subscribe(get_subscription_path(name), callback=callback)


if __name__ == '__main__':
    action = sys.argv[1]

    topic = 'test'
    subscription = 'test'
    try:
        create_topic(topic)
        create_subscription(topic, subscription)
    except AlreadyExists as e:
        # print(e.message)
        # print('skip...')
        pass

    if action == 'publish':
        text_msg = sys.argv[2]
        publish_message(topic, text_msg)
        print(f'Publish text message: {text_msg}')

    elif action == 'start_subscriber':
        subscribe(subscription)
        while True:
            time.sleep(60)
