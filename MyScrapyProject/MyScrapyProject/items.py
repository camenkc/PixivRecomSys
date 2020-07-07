# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyscrapyprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class UserStarItem(scrapy.Item):
    RemID=scrapy.Field()#主键
    PicTureID=scrapy.Field()#从键
    
class PicTagsItem(scrapy.Item):
    PicTureID=scrapy.Field()#主键
    Tags=scrapy.Field()  #以一个字符串list构成的json字符串
    
    
    