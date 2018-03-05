# -*- coding: utf-8 -*-
import requests
import os
import urllib

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


# headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

def main():


    for pagenum in range(1, 500):
        quickUrl = 'http://d.yuwenziyuan.com/rjb/UploadFile/dzkb/6s/{pagenum}.jpg'
        pagenum = "%03d" % pagenum
        quickUrl = quickUrl.format(pagenum=pagenum)
        print(quickUrl)

        try:
            response = requests.get(quickUrl, headers=header)
            print(response.status_code)
            # response.encoding = 'gb2312'
            if response.status_code == 200:
                table = str.maketrans("|\\?*<\":>+[]/'", '_' * 13)
                pagenum = pagenum.translate(table)
                file_name = os.path.join('e:\\电子课本\\人教版\\语文\\六年级上\\', pagenum + '.jpg')

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


if __name__ == '__main__':
    main()