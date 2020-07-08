# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class UserAccount(scrapy.Item): #虽然你这里写了Item 但是UserAccount
    ID=scrapy.Field()           #这个数据表，是不需要用爬虫的呀！
    PixivID=scrapy.Field()      #在app.py中就可以写注册功能
    Pixivpw=scrapy.Field()
    Username=scrapy.Field()
    Userpw=scrapy.Field()
    Usermode=scrapy.Field()
    Create_date=scrapy.Field()
    Lastlogindate=scrapy.Field()
    Lastloginip=scrapy.Field()
    Logincount=scrapy.Field()


class UserStarImage(scrapy.Item):#这个可以，但是需要从app.py中传入UserID
    UserID=scrapy.Field()        #到spider下面的ID.json
    ImageID=scrapy.Field()       #马上改成无需文件操作，内存传入ID即可
    Add_date=scrapy.Field()

class TagList(scrapy.Item):
    TagID=scrapy.Field()        #这里可以在爬取的过程中把出现过的所有tag
    TagName=scrapy.Field()      #写出到一个json文件中，然后在手动调用写入
                                #数据库的函数，每INSERT一个 就要检查是否存在
                                #所以必须将tag的名称也作为键建立索引
                                #否则不是log(n)的检查，将导致时间效率太低的情况
class UserStarArtist(scrapy.Item):#功能暂时搁置
    UserID=scrapy.Field()
    ArtistID=scrapy.Field()
    Add_date=scrapy.Field()

class UserTag(scrapy.Item):     #这个，只需要在数据库中select出来所有的
    UserID=scrapy.Field()       #收藏图片的ID，和用户ID到内存中，调用爬虫跑一遍，将tags
    TagID=scrapy.Field()        #计数，这里就无需写入文件了，直接全部内存操作
    count=scrapy.Field()        #

class Userlog(scrapy.Item):     #暂时无所谓，但不是爬虫做的事情
    Logid=scrapy.Field()
    UserID=scrapy.Field()
    Logtype=scrapy.Field()
    Logcontent=scrapy.Field()
    Logtime=scrapy.Field()


    
    

