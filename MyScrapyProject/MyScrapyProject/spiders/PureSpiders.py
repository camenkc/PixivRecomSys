import socks
import requests
import json
import os
import re
from bs4 import BeautifulSoup
from datetime import timedelta
from datetime import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class ScrapyForPicTagsClass():
    def GetTagList(self, PicID):
        self.proxies={"http":"http://127.0.0.1:1080","https":"https://127.0.0.1:1080"}
        self.PicID=int(PicID)
        return self.getPicTags()
    
    def getPicTags(self):
        self.session=self.get_session()
        
        url='https://www.pixiv.net/artworks/'+str(self.PicID)
        
        PageData=self.session.get(url,timeout = 20,verify = False,proxies=self.proxies)
        soup=BeautifulSoup(PageData.text,features="lxml")
        tagHtmlList=soup.head.find_all('meta')[-1]
        contentWithTag=json.loads(tagHtmlList['content'])
        illusetWithTag=contentWithTag['illust'][str(self.PicID)]['tags']['tags']
        tagList=[]
        for value in illusetWithTag:
            tagList.append(value['tag'])
            trans=value.get('translation')
            if isinstance(trans,dict):
                tagList.append(trans['en'])
        for tmp in tagList:
            print(tmp)
        return tagList
            
    def cookies_load(self):
        cookies_json = {}
        print('get the cookies')
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

    
        