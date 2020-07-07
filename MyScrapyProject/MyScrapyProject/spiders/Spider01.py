import scrapy
import requests
import json
import os
import re
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from MyScrapyProject.items import UserStarItem

#完成了登录后可以爬取pixiv收藏页面的功能
#现在写具体图片的Id


class ScrapyForUserStarClass(scrapy.Spider):
    name = 'ScrapyForUserStar'
    allowed_domains = [
        'quotes.toscrape.com',
        'pixiv.net'
    ]
    start_urls = [
        'https://www.pixiv.net/',
        #'https://www.pixiv.net/users/45273568/bookmarks/artworks'
    ]
    
    def parse(self, response):
        self.loadID()
        self.install_img()
        #with requests.Session() as self.s:
        #    print("******  start  ******")
        #    self.login()
        #    self.mainProcess()
    
    def loadID(self):
        with open('ID.json','r',encoding='utf-8') as f:
            s=f.read()
            tmp=json.loads(s)
            self.RemID=tmp['RemID']
            self.PixID=tmp['PixID']
        print(self.RemID)
        print(self.PixID)
    
    def cookies_load(self):
        cookies_json = {}
        try:
            cookies = json.load(open('cookies.json','r',encoding = 'utf-8'))  #使用load方法将文件中的json格式的资料读取出来
        except:
            print('cookies读取失败')
        else:
            for cook in cookies:
                if cook['domain'] == '.pixiv.net':
                    cookies_json[cook['name']] = cook['value']
            return cookies_json
        
        
        
    def get_session(self):
        self.head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': '',
        'Referer': 'https://www.pixiv.net/',
        }

        self.cookies_json = self.cookies_load()       #若是从请求头中获取cookie的，就不用使用cookies_load方法

        session = requests.session()
        session.headers = self.head
        requests.utils.add_dict_to_cookiejar(session.cookies,self.cookies_json)

        return session    
        
    def get_collection(self,page):
        session = self.get_session()
        collection_url = 'https://www.pixiv.net/ajax/user/{}/illusts/bookmarks?tag=&offset={}&limit=48&rest=show'.format(self.PixID,page*48) #将id改为你的账户uid
        print(collection_url)
        try:
            collection_data = session.get(collection_url,timeout = 20,verify = False).json()
        except:
            print('收藏夹第{}页获取失败'.format(page+1))
            return False
        else:
            print('请求第{}页成功'.format(page+1))
            return collection_data
        
    
    def get_img_url(self):
        img_url_list = []
        session = self.get_session()
        for page in range(1):
            collection_data = self.get_collection(page)
            if collection_data == False:
                pass
            else:
                total = collection_data['body']['total']
                works = collection_data['body']['works']
                item = UserStarItem()
                for img_item_data in works:
                    item['RemID']=self.RemID
                    item['PicTureID']=img_item_data['id']
                    #yield item
                    print(self.RemID)
                    print(img_item_data['id'])
                    
                    

    def install_img(self):
        head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': '',
        'Referer': 'https://www.pixiv.net/',
        }
        
        session = self.get_session()
        img_url_list = self.get_img_url()
        

class ScrapyForPicTagsClass(scrapy.Spider):
    name = 'ScrapyForPicTags'
    allowed_domains = [
        'quotes.toscrape.com',
        'pixiv.net'
    ]
    start_urls = [
        'https://www.pixiv.net/',
        #'https://www.pixiv.net/users/45273568/bookmarks/artworks'
    ]
    
    def parse(self, response):
        self.loadID()
        self.install_img()
        #with requests.Session() as self.s:
        #    print("******  start  ******")
        #    self.login()
        #    self.mainProcess()
    

    
        