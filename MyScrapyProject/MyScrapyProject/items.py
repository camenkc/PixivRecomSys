# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

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
    Logincount=scrapy.Field()


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


    
    

