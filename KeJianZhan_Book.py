# -*- coding: utf-8 -*-
import urllib

import os
import requests
from pyquery import PyQuery as pq

def get_index(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # print(response.text)
            return response.text
        else:
            print('请求书本列表页出错：', response.status_code)
            return None
    except Exception as e:
        print('请求书本列表页出现异常：', e.args)
        return None

def parse_index(html):
    doc = pq(html)
    link = doc('#bigimg').attr('src')
    print(link)
    return link

#bigimg
def main():
    urlPrv = 'http://www.kjzhan.com'
    for pagenum in range(2, 120):
        pageUrl = 'http://www.kjzhan.com/dianzikeben/7x_lishi_{pagenum}.html'
        pageUrl = pageUrl.format(pagenum=pagenum)
        print('页面地址：', pageUrl)

        link = parse_index(get_index(pageUrl))
        downLink = urlPrv + link
        print('图片地址：', downLink)

        try:
            response = requests.get(downLink)
            print(response.status_code)
            if response.status_code == 200:
                pagenum = "%03d" % pagenum
                table = str.maketrans("|\\?*<\":>+[]/'", '_' * 13)
                pagenumstr = pagenum.translate(table)
                file_name = os.path.join('e:\\电子课本\\人教版\\历史\\七年级下（2016）\\', pagenumstr + '.jpg')

                isExists = os.path.exists(file_name)
                if not isExists:  # 文件不存在才下载、
                    u = urllib.request.urlopen(downLink)
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

if __name__ == '__main__':
    main()


