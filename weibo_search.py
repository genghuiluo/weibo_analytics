# coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pickle
import time
import pymysql
from bs4 import BeautifulSoup
import os

LOGIN_URL="https://login.weibo.cn/login/"

driver = webdriver.Firefox()
localdb=pymysql.connect('localhost',os.environ['MYSQL_USER'],os.environ['MYSQL_PASSWORD'],'test',charset='utf8')
cursor=localdb.cursor()

def login_weibo(username, password):
    print("ready for login weibo.cn...\n")
    driver.get(LOGIN_URL)

    # input username & password
    elem_user = driver.find_element_by_name("mobile")
    elem_user.send_keys(username)
    elem_pwd = driver.find_element_by_xpath("/html/body/div[2]/form/div/input[2]")
    elem_pwd.send_keys(password)

    # manually input verify code (http://login.weibo.cn/login/ mobile phone required)
    time.sleep(30)

    # submit
    elem_sub = driver.find_element_by_name("submit")
    elem_sub.click()

    time.sleep(10)

    if LOGIN_URL in driver.current_url:
        print("login failed...")
        exit(1)
    else:
        #print coockie detail
        print("print Cookie key-value detail:")
        for cookie in driver.get_cookies():
            for key in cookie:
                print(key,cookie[key])
        # write cookie
        pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
        print("login success...\n")


def search_keyword(keyword,max_page_num):
    print("search keyword:",keyword)

    """
    try to read cookie, but not work currently
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    """

    driver.get("https://weibo.cn/search/")
    search_input = driver.find_element_by_xpath("//div[@class='c']/form/div/input")
    search_input.send_keys(keyword)
    search_input.send_keys(Keys.RETURN)   # return

    print("wait for searched result loading ...\n")

    page_num=1

    while page_num <= max_page_num:
        weibo_posts = load_page()
        save_post(weibo_posts,keyword)

        next_page_url = driver.find_element_by_xpath("//div[@id='pagelist']/form/div/a").get_attribute("href")
        driver.get(next_page_url)
        print("next page: ",next_page_url,"...")
        page_num = page_num + 1

def load_page():
    time.sleep(10)
    retry_time=0
    weibo_posts = driver.find_elements_by_xpath("//div[@class='c']")
    comments = driver.find_elements_by_partial_link_text("评论")

    # if load failed, refresh by max 5 times
    while len(comments) == 0 and retry_time < 6:
        retry_time=retry_time+1
        print("page loading failed,",str(retry_time),"th refresh...")
        driver.refresh()
        time.sleep(10)
        comments = driver.find_elements_by_partial_link_text("评论")

    return driver.find_elements_by_xpath("//div[@class='c']")



def save_post(weibo_posts,keyword):
    for weibo_post in weibo_posts:
        div_id=weibo_post.get_attribute("id")
        if (div_id):
            #print(weibo_post.get_attribute("innerHTML"))
            #print(weibo_post.text)

            post_soup = BeautifulSoup(weibo_post.get_attribute("innerHTML"),"lxml")
            poster = post_soup.find('a',attrs={'class':'nk'})
            post_content = post_soup.find('span',attrs={'class':'ctt'})
            comment = post_soup.find('a',attrs={'class':'cc'})
            device = post_soup.find('span',attrs={'class':'ct'})
            """
            print("poster: ",poster.getText())
            print("post content: ",post_content.getText())
            print("comment: ",comment.getText(),comment["href"])
            print("device: ",device.getText())
            print("=============================")
            """

            sql = "INSERT weibo_posts(raw_post_id,raw_post_text,raw_post_html,poster,post_content,comment_cnt,comment_url,device,keyword,search_dt) \
                VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s',now()) ;" % \
                (div_id,weibo_post.text,weibo_post.get_attribute("innerHTML"),poster.getText(),post_content.getText(),comment.getText(),comment["href"],device.getText(),keyword)
            #print(sql)
            try:
                cursor.execute(sql)
                localdb.commit()
            except pymysql.Error as e:
                print ("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
                localdb.rollback()
            """
            create table test.weibo_posts(raw_post_id varchar(50), raw_post_text text character set utf8, raw_post_html text character set utf8, poster varchar(50) character set utf8, post_content varchar(500) character set utf8, comment_cnt varchar(20) character set utf8, comment_url varchar(100), device varchar(100) character set utf8, keyword varchar(50) character set utf8, search_dt datetime, primary key(raw_post_id));
            """


if __name__ == '__main__':

    username = os.environ['WEIBO_USER']  # your username
    password = os.environ['WEIBO_PASSWORD'] # your password

    login_weibo(username, password)

    sel_sql = "SELECT key_text FROM weibo_realtimehot ORDER BY seq DESC LIMIT 50;"
    cursor.execute(sel_sql)
    results = cursor.fetchall()
    for row in results:
        keyword = row[0]
        max_page = 10
        search_keyword(keyword,max_page)


# TBD :
# 1) insert sql escape single quote
# 2) use ML treat verify code
# 3) invalid utf-8 character in raw_post_text
