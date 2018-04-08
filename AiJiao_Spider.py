# -*- coding: utf-8 -*-
import os

import re
import urllib

import requests
from pyquery import PyQuery as pq



def get_startPage(url):
    try:
        response = requests.get(url)
        # response.encoding = 'gb2312'
        if response.status_code == 200:
            return response.text
        else:
            print('请求出版社课本列表页出错：', response.status_code)
            return None
    except Exception as e:
        print('请求出版社课本列表页出现异常：', e.args)
        return None


def parse_startPage(html):
    doc = pq(html)
    items = doc('body > div.bj > div.hroup.w > div.module > div.fl > div.mokao_list > div.dzkb_list ul li').items()
    for item in items:
        yield{
            'publisher': item.find('a i').text(),
            'link': item.find('a').attr('href'),
            'sub': item.find('a .nj_km .km').text(),
            'nianji': item.find('a .nj_km .nj').text()
        }


def get_bookPage(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print('请求书本页面出错：', response.status_code)
    except Exception as e:
        print('请求书本页面出现异常：', e.args)
        return None

def parse_bookPage(html):
    doc = pq(html)
    totalPage = doc('body > div.bj > div.hroup.w > div.md_list > div.fr > div:nth-child(1) > div > p:nth-child(5) > span.blue').text()

    return totalPage

def saveBook(keyAdd, totalPage, path):
    totalPage = int(totalPage) + 1
    for pagenum in range(1, totalPage):
        quickUrl = 'http://res.ajiao.com/uploadfiles/Book/{keyAdd}/{pagenum}_838x979.jpg'
        pagenumstr = "%03d" % pagenum  # 数字转字符串 "%d" % pagenum
        quickUrl = quickUrl.format(keyAdd=keyAdd, pagenum=pagenum)
        print(quickUrl)

        try:
            response = requests.get(quickUrl)
            print(response.status_code)
            if response.status_code == 200:
                table = str.maketrans("|\\?*<\":>+[]/'", '_' * 13)
                pagenumstr = pagenumstr.translate(table)
                file_name = os.path.join(path, pagenumstr + '.jpg')

                isExists = os.path.exists(file_name)
                if not isExists:  # 文件不存在才下载、
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
                    response.close()
                else:
                    print(file_name + '文件已经存在，不再重复下载。')
                    response.close()
            else:
                print('请求页面出错了,可能是结束了', response.status_code)
                return None
        except Exception as e:
            print('请求页面出现异常', e.args)
            return None

def main():
    url = 'http://zyk.ajiao.com/dzkb/all-all-8/'
    html = get_startPage(url)
    if html:
        books = parse_startPage(html)
        for book in books:
            print(book)
            xueqi = book['nianji'] + book['sub'][2:]
            print(xueqi)
            path1 = os.path.join('e:\\电子课本\\', book['publisher'], book['sub'][0:2], xueqi)
            isExists = os.path.exists(path1)
            if not isExists:
                os.makedirs(path1)

            pattern = re.compile('.*/(.*).html')
            keyAdd = re.findall(pattern, book['link'])[0]
            print('keyAdd: ', keyAdd)

            bookPage = get_bookPage(book['link'])
            totalPage = parse_bookPage(bookPage)
            print('totalPage', totalPage)

            saveBook(keyAdd, totalPage, path1)


if __name__ == '__main__':
    main()