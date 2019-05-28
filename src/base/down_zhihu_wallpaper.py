import os
import urllib
from urllib import request
import json as js
from bs4 import BeautifulSoup
import pymysql


def getImg(keyword, max=20, off_set=20):
    req = request.Request(
        "https://api.zhihu.com/search_v3?advert_count=0&correction=1&lc_idx=0&limit=20&offset=%s&q=%s&search_hash_id"
        "=f72a26207357a4fc4d297a7ebbd6e764&show_all_topics=0&t=general&vertical_info=0,1,1,0,1,0,0,0,0,1 "
        % (str(off_set), urllib.parse.quote(keyword)))
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
    down_pics_count = 0
    for data_item in json["data"]:
        soup = BeautifulSoup(data_item["object"]["content"], "lxml")
        for figure in soup.find_all("figure"):
            img_info = figure.noscript.img
            print(img_info["src"])

            if int(img_info["data-rawwidth"]) < 720 or int(img_info["data-rawheight"]) < 1280:
                print("jump width = %s;height = %s" % (img_info["data-rawwidth"], img_info["data-rawheight"]))
                continue
            save_name_split_list = str(img_info["src"]).split("/")
            length = len(save_name_split_list)
            # _b.jpg是缩略图
            url = str(img_info["src"]).replace("_b.jpg", ".jpg");
            if not insert_table(url):
                down_pics_count += 1
                saveImg(url, str(save_name_split_list[length - 1]).replace("_b.jpg", ".jpg"))
                if down_pics_count >= max:
                    return
    off_set += 20
    getImg(keyword, max - down_pics_count, off_set)


def insert_table(url):
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='fanqiang', db='zhihupics')
    cur = conn.cursor()
    cur.execute("insert ignore into zhihuTable (url)  values (%s)", url)
    print("insert result:" + str(cur.rowcount))
    rowcount = cur.rowcount == 0
    conn.commit()
    cur.close()
    conn.close()
    return rowcount


def select_all_from_table(url):
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='fanqiang', db='zhihupics')
    cur = conn.cursor()
    cur.execute("select * from zhihuTable where url = '%s'" % url)
    print("select result: %s" % cur)
    result = len(cur) == 0
    cur.close()
    conn.close()
    return result


def saveImg(url, saved_name="desk_bg", img_path='imgs'):
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    img_name = '{}{}{}'.format(img_path, os.sep, saved_name)
    from urllib.request import urlretrieve
    urlretrieve(url, img_name)
    print("save pic:%s to %s" % (url, img_path))
    insert_table(url)


def create_table():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='fanqiang', db='zhihupics')
    cur = conn.cursor()
    cur.execute("create table if not exists zhihuTable (id int auto_increment, url varchar(90),primary key(id),"
                "unique(url))")
    cur.close()
    conn.close()


create_table()
getImg("手机壁纸")
