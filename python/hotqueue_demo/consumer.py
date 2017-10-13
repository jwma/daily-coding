from q import get_queue

q = get_queue('test')

# 通过这种方式，程序会一直等待下一个可消费的项目被获取
for item in q.consume():
    print(item)
