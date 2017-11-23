import redis
import time


class SortedQueue(object):
    def __init__(self):
        self.client = redis.StrictRedis(password='asdf-1234')

    def append(self, name, value):
        return self.client.zadd(name, int(round(time.time() * 1000)), value)

    def first(self, name):
        rs = self.client.zrange(name, 0, 0)
        return bytes.decode(rs[0]) if len(rs) > 0 else None

    def remove(self, name, value):
        return self.client.zrem(name, value)

    def index(self, name, value):
        return self.client.zrank(name, value)

    def count(self, name):
        return self.client.zcard(name)


sq = SortedQueue()

name = 'test_queue'
# 往队列中追加新item
sq.append(name, 'item1')
sq.append(name, 'item2')

print(sq.first(name))  # 获取队列中第一个item
print(sq.remove(name, 'item1'))  # 删除刚刚添加的item1
print(sq.index(name, 'item2'))  # 获取item2在队列中的索引
print(sq.count(name))  # 获取队列长度
