import scrapy
import requests
import re
from bs4 import BeautifulSoup
class Myscrapy01Spider(scrapy.Spider):
    name = 'MyScrapy01'
    allowed_domains = [
        'quotes.toscrape.com',
        'pixiv.net'
    ]
    start_urls = [
        'https://www.pixiv.net/',
        'https://www.pixiv.net/users/45273568/bookmarks/artworks'
    ]

    def parse(self, response):
        with requests.Session() as self.s:
            print("******  start  ******")
            self.login()
            self.mainProcess()
        
        
    def login(self):
        print("正在请求登录页面...")
        login_page_url = "https://accounts.pixiv.net/login"
        login_html = self.s.get(login_page_url)
        print("正在解析")
        post_key = self.get_post_key(login_html.text)

        login_url = "https://accounts.pixiv.net/login"
        pixiv_id, password = ('CakeBaker.0308@gmail.com','12138ckC')#get_account()
        login_data = self.s.post(url=login_url, data={
            "pixiv_id": pixiv_id,
            "password": password,
            "captcha": "",
            "g_recaptcha_response": "",
            "post_key": post_key,
            "source": "accounts",
            "ref": "",
            "return_to": "http://www.pixiv.net/"
        })
        print (login_data.text)
    def get_post_key(self,login_html):
        reg = r'name="post_key" value="(.*?)"'
        key_re = re.compile(reg)
        key_list = re.findall(key_re, login_html)
        if len(key_list) == 1:
            return key_list[0]
        else:
            raise Exception("post key can not found")
    
    def get_account():
    #"""
    #config example:{"password": "123", "pixiv_id": "123@qq.com"}
    #:return:
    #"""
        try:
            file = open('config', 'r')
            str_data = file.read()
            file.close()
            data = json.loads(str_data)
            return data['pixiv_id'], data['password']
        except IOError:
            raise Exception("user config error")
    
    def mainProcess(self):
        self.get_user_bookmark(45273568)
        pass
    
    
    def get_user_bookmark(self,user_id):
    #"""
    #获取用户收藏的作品，并根据收藏作品的创作者id加入user_id(需要判断是否已经在user_ids里)末尾
    #:param user_id:
    #:return:
    #"""
        print("****** 开始获取用户（%d）的收藏作品 ******" % user_id)

        i = 1
        count = 0
        while True:
            try:
                print('尝试下载用户页面')
                url_tmp_s="https://www.pixiv.net/users/"+str(user_id)+"/bookmarks/artworks"
                print(url_tmp_s)
                res = self.s.get(url_tmp_s)
                print(res.text)
                print('尝试使用BF4')
                soup = BeautifulSoup(res.text, "html.parser")
                all_img = soup.find_all('img', class_="ui-scroll-view")
            except self.e:
                print(self.e)
            
        # 如果未找到，则说明已到最大页数
            if not all_img:
                break

        # 查找收藏图片的作者id
            all_a = soup.find_all('a', class_="ui-profile-popup")
            for a in all_a:
                c_user_id = a['data-user_id']
                add_glob_user_ids(c_user_id)

            print("用户（%d）收藏，已存：%d，新增：%d" % (user_id, count, len(all_img)))
            for img in all_img:
                target_url = img['data-src']
                try:
                    if not download("bookmarks", target_url):
                        console("ERROR:" + " bookmarks " + target_url)
                        save_error(user_id, target_url)
                except IndexError as e:
                    print (e)
                    print(target_url)

            count += len(all_img)
            i += 1
    
    
    
    
    
    
    
    def main(self):
        global user_ids, index
        user_ids, index, work_or_mark = _get_ckpt()

        if not user_ids:
            console("start get user ids")
            user_ids = _get_user_ids()
        else:
            console("read from ckpt. users count: %d, index: %d" % (len(user_ids), index))

        console("开始遍历 user。 start index : " + str(index))

        first = True
        while index < len(user_ids):
            if not (first and work_or_mark):
                console("从用户的作品开始")
                _save_ckpt(0)
                # 抓取该用户的作品
                get_user_work(user_ids[index])
            else:
                console("从用户收藏的作品开始")

            _save_ckpt(1)
            # 抓取该用户收藏的作品
            get_user_bookmark(user_ids[index])

            first = False
            index += 1

        console("全部抓取完成，用户总数：" + str(len(user_ids)))
        
        