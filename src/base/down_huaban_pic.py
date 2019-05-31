# coding=utf-8
# 根据关键字从花瓣网下载图片到MyGodData/imgs下。
# 执行完毕之后执行upload_pic_version.py
import os
import shutil
import urllib
from urllib import request

import json as js
from bs4 import BeautifulSoup


def getImg(keyword, imageSaveDir, maxcount=80, page=1):
    req = request.Request("https://huaban.com/search/?q=%s&type=pins&page=%s&per_page=20&wfl=1" % (
        urllib.parse.quote(keyword), page))
    print(req.full_url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/74.0.3729.157 Safari/537.36')
    req.add_header('X-Request', 'JSON')
    req.add_header('Accept', 'application/json')
    req.add_header('X-Requested-With', 'XMLHttpRequest')
    with request.urlopen(req) as f:
        print('status:', f.status, f.reason)
        requset_result = f.read().decode("utf-8")
    soup = BeautifulSoup(requset_result, "lxml")
    json = js.loads(soup.text)
    download_count = 0
    for i in json['pins']:
        width = int(i['file']['width'])
        height = int(i['file']['height'])
        key = i['file']['key']
        if width < 600 or height > 5000:
            print("jump %s:width = %s;height = %s" % (key, width, height))
            continue
        download_count += 1
        saveImg("https://hbimg.huabanimg.com/%s" % key, "%s.jpg" % key, imageSaveDir)
        if download_count >= maxcount:
            return
    getImg(keyword, imageSaveDir,maxcount - download_count,page + 1)


def saveImg(url, saved_name="desk_bg", img_path='imgs'):
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    img_suffix = os.path.splitext(url)[1]
    img_name = '{}{}{}{}'.format(img_path, os.sep, saved_name, img_suffix)
    from urllib.request import urlretrieve
    urlretrieve(url, img_name)
    print("save pic:%s to %s" % (url, img_path))


def readCityCodeJson(my_god_data_path):
    city_code_file = my_god_data_path + "/citycode.json"
    with open(city_code_file) as json_file:
        return js.load(json_file)


# 根据城市码获取图片
def get_images_by_city_code():
    my_god_data_path = os.path.abspath(os.path.join(os.getcwd(), "../../../MyGodData"))
    json = readCityCodeJson(my_god_data_path)
    index = 0
    cityCodeList = []
    for city in json:
        city_name = city["city"]
        city_code = city["cityCode"]
        if city_code in cityCodeList:
            print("jump city :%s" % city_name)
            continue
        cityCodeList.append(city_code)
        print("city: %s" % city_name)
        print("cityCode: %s" % city_code)

        # getImg(city["city"], 20, myGodDataPath + "/images/%s" % city_code)
        getImg(city["city"], 20, my_god_data_path + "/images")
        index += 1
        if index > 3:
            break


def clear_images():
    my_god_data_path = os.path.abspath(os.path.join(os.getcwd(), "../../../MyGodData/images"))
    shutil.rmtree(my_god_data_path)


if __name__ == '__main__':
    clear_images()
    my_god_data_path = os.path.abspath(os.path.join(os.getcwd(), "../../../MyGodData"))
    getImg("儿童节", my_god_data_path + "/images")

print("---------------------finsh------------------------")
