import requests


def get_html(url):
    resp = requests.get(url)
    return resp.text


if __name__ == '__main__':
    html = get_html('https://www.baidu.com')
    print(html)
