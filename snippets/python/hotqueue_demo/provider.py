from q import get_queue

if __name__ == '__main__':
    # 获取test队列
    queue = get_queue('test')

    # 向队列放入项目
    queue.put(1)
    queue.put(2)
    queue.put(3)
