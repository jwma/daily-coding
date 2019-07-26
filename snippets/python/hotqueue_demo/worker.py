from q import worker


@worker('test', timeout=1)
def square_worker(num):
    print(int(num) * int(num))


if __name__ == '__main__':
    square_worker()
