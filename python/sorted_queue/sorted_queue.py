import redis


class SortedQueue(object):
    def __init__(self):
        self.client = redis.StrictRedis()

    def append(self, name, value, score):
        return self.client.zadd(name, score, value)

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

name = 'wzry'
print(sq.append(name, 'a1', 1000))
print(sq.append(name, 'a2', 1010))
print(sq.append(name, 'a3', 3000))

print(sq.first(name))
print(sq.remove(name, sq.first(name)))
