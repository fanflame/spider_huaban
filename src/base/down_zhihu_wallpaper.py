import os
import urllib
from urllib import request

import json as js
from bs4 import BeautifulSoup
# import MySQLdb

def getImg(keyword, off_set="20"):
    req = request.Request(
        "https://api.zhihu.com/search_v3?advert_count=0&correction=1&lc_idx=0&limit=20&offset=%s&q=%s&search_hash_id=f72a26207357a4fc4d297a7ebbd6e764&show_all_topics=0&t=general&vertical_info=0,1,1,0,1,0,0,0,0,1"
        % (off_set, urllib.parse.quote(keyword)))
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
    if json["paging"]["is_end"]:
        next_json_url = json["paging"]["next"]
    for data_item in json["data"]:
        soup = BeautifulSoup(data_item["object"]["content"], "lxml")
        for figure in soup.find_all("figure"):
            img_info = figure.noscript.img
            print(img_info["data-default-watermark-src"])

            if int(img_info["data-rawwidth"]) < 720 or int(img_info["data-rawheight"]) < 1280:
                print("jump width = %s;height = %s" % (img_info["data-rawwidth"], img_info["data-rawheight"]))
                continue
            save_name_split_list = str(img_info["data-default-watermark-src"]).split("/")
            length = len(save_name_split_list)
            # _b.jpg是缩略图
            saveImg(str(img_info["data-default-watermark-src"]).replace("_b.jpg", ".jpg"),
                    str(save_name_split_list[length - 1]).replace("_b.jpg", ".jpg"))
        return


def saveImg(url, saved_name="desk_bg", img_path='imgs'):
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    img_name = '{}{}{}'.format(img_path, os.sep, saved_name)
    from urllib.request import urlretrieve
    urlretrieve(url, img_name)
    print("save pic:%s to %s" % (url, img_path))


getImg("手机壁纸")
