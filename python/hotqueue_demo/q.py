from configparser import ConfigParser
from hotqueue import HotQueue


def get_queue(name):
    """获取一个指定名称的队列"""
    cp = ConfigParser()
    cp.read('./config.ini')
    host = cp.get('redis', 'host')
    password = cp.get('redis', 'password')

    return HotQueue(name, host=host, password=password)


def worker(name, *args, **kwargs):
    """获取一个指定名称队列的worker装饰器"""
    queue = get_queue(name)
    return queue.worker(*args, **kwargs)
