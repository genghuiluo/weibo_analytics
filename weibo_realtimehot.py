#!/usr/bin/env python
# encoding=utf-8

################################################################
#   Copyright (C) 2017 All rights reserved.
#
#   Filename：weibo_realtimehot.py
#   Creator：Mark Luo
#   Created Date：03/09/2017
#   Description：
#
#   Modified History：
#
################################################################

import requests
from bs4 import BeautifulSoup
import re
import pymysql
import time

URL = "http://s.weibo.com/top/summary?cate=realtimehot"

def download_page(url):
    return requests.get(url, headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
        }).text

def parse_keyword(html):
    soup = BeautifulSoup(html,'lxml')
    scripts = soup.find_all('script')
    for script in scripts:
        matchParts = re.match(r'^(.+pl_top_realtimehot.+\"html\"\:\")(.+)\"\}\)$',script.text)
        if matchParts:
            #print( matchParts.group(2) )
            embed_html_in_js = matchParts.group(2)
            embed_html_in_js = embed_html_in_js.replace('\\n','').replace('\\/','/').replace('\\"','"')
            soup = BeautifulSoup(embed_html_in_js,'lxml')
            #print( soup )
            keywords = soup.find_all('tr',attrs={'action-type':'hover'})
            print("captured: ",len(keywords))
            key_rank = 1
            for keyword in keywords:
                key_text = keyword.find('p',attrs={'class':'star_name'}).find('a').text.encode('ascii').decode('unicode-escape')
                key_num = keyword.find('p',attrs={'class':'star_num'}).text
                #print(key_text,key_num)
                sql="INSERT INTO weibo_realtimehot(key_text,key_num,key_rank,capture_time) \
                    VALUES ('%s', %d, %d, now());" % \
                    (key_text, int(key_num), int(key_rank))
                try:
                    cursor.execute(sql)
                    db.commit()
                except pymysql.Error as e:
                    print ("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
                    db.rollback()

                key_rank += 1

try:
    db=pymysql.connect('localhost','root','1234','test',charset='utf8')
    cursor = db.cursor()

    html =  download_page(URL)

    parse_keyword (html)

    print("weibo_realtimehot.py successed ",time.asctime(time.localtime()))
except AttributeError as e:
    print("weibo_realtimehot.py failed ",time.asctime(time.localtime()))
    print(e)

"""
CREATE TABLE weibo_realtimehot( seq bigint not null auto_increment, key_text varchar(100) character set utf8, key_num bigint, key_rank integer, capture_time datetime, primary key (seq));
"""
