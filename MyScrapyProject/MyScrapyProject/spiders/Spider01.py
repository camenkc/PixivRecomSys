import scrapy
#import socks
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

###############################################################     
#根据图片Id爬取tags的代码也已经完成 pipeline准备完毕之即可取消yield注释
