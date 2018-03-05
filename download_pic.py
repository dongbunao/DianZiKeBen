# -*- coding: utf-8 -*-
import requests
import os

url = 'http://www.yuwenziyuan.com/rjb/1s/dzkb/22429.html'
s = requests.session()
s.get(url)

header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    # 'Accept-Encoding': 'gzip, deflate, sdch'
    # 'Accept-Language': 'zh-CN,zh;q=0.8'
    'Connection': 'keep-alive',
    'Cookie': '__guid=92395592.2436537089074879500.1520213412400.8594; monitor_count=6',
    'Host': 'd.yuwenziyuan.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}


def main():
    req = requests.get('http://d.yuwenziyuan.com/rjb/UploadFile/dzkb/1s/001.jpg', headers=header)
    print(req.status_code)
    with open('001.jpg', 'wb') as f:
        f.write(req.content)

if __name__ == '__main__':
    main()