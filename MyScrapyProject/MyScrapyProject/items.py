# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyscrapyprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class UserAccount(scrapy.Item):
    ID=scrapy.Field()
    PixivID=scrapy.Field()
    Pixivpw=scrapy.Field()
    Username=scrapy.Field()
    Userpw=scrapy.Field()
    Usermode=scrapy.Field()
    Create_date=scrapy.Field()
    Lastlogindate=scrapy.Field()
    Lastloginip=scrapy.Field()
    Logincoutn=scrapy.Field()

<<<<<<< HEAD
class UserStarImage(scrapy.Item):
    UserID=scrapy.Field()
    ImageID=scrapy.Field()
    Add_date=scrapy.Field()

class TagList(scrapy.Item):
    TagID=scrapy.Field()
    TagName=scrapy.Field()

class UserStarArtist(scrapy.Item):
    UserID=scrapy.Field()
    ArtistID=scrapy.Field()
    Add_date=scrapy.Field()

class UserTag(scrapy.Item):
    UserID=scrapy.Field()
    TagID=scrapy.Field()
    count=scrapy.Field()

class Userlog(scrapy.Item):
    Logid=scrapy.Field()
    UserID=scrapy.Field()
    Logtype=scrapy.Field()
    Logcontent=scrapy.Field()
    Logtime=scrapy.Field()
=======
class UserStarItem(scrapy.Item):
    RemID=scrapy.Field()#主键
    PicTureID=scrapy.Field()#从键
    
class PicTagsItem(scrapy.Item):
    PicTureID=scrapy.Field()#主键
    Tags=scrapy.Field()  #以一个字符串list构成的json字符串
    
    
    
>>>>>>> 7d9227b39b5ace0ada707b2e5995cc77e3ad1722
