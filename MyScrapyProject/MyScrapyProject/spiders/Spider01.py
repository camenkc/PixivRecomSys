import scrapy
import requests
import re
class Myscrapy01Spider(scrapy.Spider):
    name = 'MyScrapy01'
    allowed_domains = [
        'quotes.toscrape.com',
        'pixiv.net'
    ]
    start_urls = [
        'https://www.pixiv.net/'
        #'https://www.pixiv.net/users/45273568/bookmarks/artworks'
    ]

    def parse(self, response):
        with requests.Session() as self.s:
            print("******  start  ******")
            self.login()
            self.main()
        print('now Downloading the page')
        
        
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
    
    def main(self):
        
        