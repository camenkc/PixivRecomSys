import sys
import os
from sys import path
path.append(os.path.abspath(os.path.dirname(__file__)).split('MyScrapyProject')[0])

import requests
import json
import os
import re
from bs4 import BeautifulSoup
from datetime import timedelta
from datetime import datetime
from MyScrapyProject.MyScrapyProject.MysqlRW import SQLOS
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class ScrapyForUserStarClass():

    def GetUserStarPics(self,UserId,PixUserId):
        
        self.loadID(UserId,PixUserId)
        self.isEnd=False
        self.my_proxies={"http":"http://127.0.0.1:1080","https":"https://127.0.0.1:1080"}
        
        self.open_spider()
        
        self.get_img_url()
        
        self.close_spider()
    def loadID(self,UserId,PixUserId):

        self.RemID=UserId
        self.PixID=PixUserId
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
            #session.proxies={"http":"http://127.0.0.1:1080","https":"https://127.0.0.1:1080"}
            collection_data = session.get(collection_url,timeout = 20,verify = False,proxies=self.my_proxies).json()
        except Exception as e:
            print(e)
            print('收藏夹第{}页获取失败'.format(page+1))
            return False
        else:
            print('请求第{}页成功'.format(page+1))
            return collection_data
        
    
    def get_img_url(self):
        print('getting img IDs')
        img_url_list = []
        session = self.get_session()
        
        now =datetime.now()
        self.item={}
        self.item['Add_date']=now.strftime('%Y-%m-%d')
        for page in range(100):
            collection_data = self.get_collection(page)
            if collection_data == False:
                pass
            else:
                total = collection_data['body']['total']
                works = collection_data['body']['works']
                if len(works)==0 :
                    self.isEnd=True
                    self.item['UserID']=0;
                    break
                for img_item_data in works:
                    self.item['UserID']=self.RemID
                    self.item['ImageID']=int(img_item_data['id'])
                    self.process_item(self.item)
                    #print(type(self.RemID))
                    #print(type(img_item_data['id']))
                    

    def open_spider(self):
        self.connect=SQLOS.Connect_to_DB()
    def process_item(self,item):
        print('Process Item now')
        try:
            with self.connect.cursor() as cursor:
                if(SQLOS.CheckStarImage(item.get("UserID"),item.get("ImageID"))):
                    pass
                else:
                   
                    SQLOS.AddStarImage(item.get("UserID"),item.get("ImageID"))
               
        
        except Exception as e:
            print(e)
        return item
    def close_spider(self):
        self.connect.close()
     