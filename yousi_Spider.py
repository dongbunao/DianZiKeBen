# -*- coding: utf-8 -*-
import re

import os
import urllib

import requests
from pyquery import PyQuery as pq

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


def get_startPage(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print('请求书本列表页出错：', response.status_code)
            return None
    except Exception as e:
        print('请求书本列表页出现异常：', e.args)
        return None

def parse_startPage(html):
    doc = pq(html)
    items = doc('body > div.jf-teach > div.jf-box > ul > li').items()
    for item in items:
        yield {
            'link': item.find('a').attr('href')
        }

def get_bookPage(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print('请求书本页出错：', response.status_code)
            return None
    except Exception as e:
        print('请求书本页出现异常：', e.args)
        return None

def parse_bookPage(html):
    doc = pq(html)
    downUrl = doc('#ifrPage').attr('src')
    bookName = doc('body > div.jf-chapter > div > div.right.fn-right > div > div > div.top > a').text()

    pattern0 = re.compile('.*电子教材：(.*)')
    bookName = re.findall(pattern0, bookName)[0]

    pattern = re.compile('.*.com%2F(.*)')
    downUrl = re.findall(pattern, downUrl)[0]

    return bookName, downUrl

def save_book(downUrl, bookName):
    quickUrl = downUrl
    pagenum = bookName
    try:
        response = requests.get(quickUrl)
        print(response.status_code)
        # response.encoding = 'gb2312'
        if response.status_code == 200:
            table = str.maketrans("|\\?*<\":>+[]/'", '_' * 13)
            pagenum = pagenum.translate(table)
            file_name = os.path.join('e:\\电子课本\\外研版\\英语\\', pagenum + '.pdf')

            isExists = os.path.exists(file_name)
            if not isExists:  # 文件不存在才下载

                u = urllib.request.urlopen(quickUrl)
                f = open(file_name, 'wb')

                block_sz = 8192
                while True:
                    buffer = u.read(block_sz)
                    if not buffer:
                        break

                    f.write(buffer)
                f.close()
                print("Sucessful to download" + " " + file_name)
            else:
                print(file_name + '文件已经存在，不再重复下载。')
        else:
            print('请求页面出错了,可能是结束了', response.status_code)
            return None
    except Exception as e:
        print('请求页面出现异常', e.args)
        return None

def main():
    downUrlPrv = 'http://jfpdf.yousi.com/'
    baseUrl = 'http://jiaofu.yousi.com'

    startUrl = 'http://jiaofu.yousi.com/l-33-11-118-0/'
    startPage = get_startPage(startUrl)
    books = parse_startPage(startPage)
    for book in books:
        print(book)
        bookUrl = baseUrl + book['link']
        bookName, downUrl = parse_bookPage(get_bookPage(bookUrl))
        downUrl = downUrlPrv + downUrl

        print('PDF文件地址：', downUrl)
        print('课本名：', bookName)

        save_book(downUrl, bookName)

if __name__ == '__main__':
    main()