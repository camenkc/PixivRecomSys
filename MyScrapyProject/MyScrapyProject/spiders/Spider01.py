import scrapy
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
from MyScrapyProject.items import UserStarImage

#完成了登录后可以爬取pixiv收藏页面的功能
#现在写具体图片的Id
#已完成 在PixivRecomSys\MyScrapyProject\MyScrapyProject\spiders目录中调用scrapy crawl ScrapyForUserStar
#即可加载我的P站登录cookies （cookies.json）和需要爬取的账号 （ID.json）
#全部爬取到服务器中

class ScrapyForUserStarClass(scrapy.Spider):
    name = 'ScrapyForUserStar'
    allowed_domains = [
        'quotes.toscrape.com',
        'pixiv.net'
    ]
    
    custom_settings={
        'ITEM_PIPELINES':{'MyScrapyProject.pipelines.AddToUserStarImagePPL':300}
    }
    start_urls = [
        'http://quotes.toscrape.com/',
        #'https://www.pixiv.net/users/45273568/bookmarks/artworks'
    ]
    
    def parse(self, response):
        self.loadID()
        self.isEnd=False
        self.my_proxies={"http":"http://127.0.0.1:1080","https":"https://127.0.0.1:1080"}
        self.item = UserStarImage()
        g=self.get_img_url()
        while self.isEnd==False:
            try:
                tmp = next(g)
                if (tmp['UserID']!=0):
                    yield tmp
            except:
                pass
    
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
                    yield self.item
                    #print(type(self.RemID))
                    #print(type(img_item_data['id']))
                    

     
###############################################################     
#根据图片Id爬取tags的代码也已经完成 pipeline准备完毕之即可取消yield注释
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
        self.loadPicsID()
        self.getPicTags()
        #with requests.Session() as self.s:
        #    print("******  start  ******")
        #    self.login()
        #    self.mainProcess()
    
    def loadPicsID(self):
        with open('PicsId.json') as f:
            s=f.read()
            self.PicList=json.loads(s)
    
    def getPicTags(self):
        self.session=self.get_session()
        item=PicTagsItem()
        for PicID in self.PicList:
            url='https://www.pixiv.net/artworks/'+str(PicID)
            #print(url)
            PageData=self.session.get(url,timeout = 20,verify = False)
            #print(PageData.text)
            soup=BeautifulSoup(PageData.text)
            
            tagHtmlList=soup.head.find_all('meta')[-1]
            
            contentWithTag=json.loads(tagHtmlList['content'])
            
            illusetWithTag=contentWithTag['illust'][str(PicID)]['tags']['tags']
            
            tagList=[]
            for value in illusetWithTag:
                #print(value)
                tagList.append(value['tag'])
                trans=value.get('translation')
                if isinstance(trans,dict):
                    tagList.append(trans['en'])
                
            for tmp in tagList:
                print(tmp)
            s=json.dumps(tagList)
            item['PicTureID']=PicID
            item['Tags']=s
            #yield item
            
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

    
        