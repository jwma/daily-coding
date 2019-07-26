import random


def rand(strs='0123456789', len=5):
    """在指定字符集中生成指定长度的随机字符串"""
    return ''.join(random.sample(strs, len))


if __name__ == '__main__':
    print(rand())
    print(rand(strs='abcxyz12345', len=6))
