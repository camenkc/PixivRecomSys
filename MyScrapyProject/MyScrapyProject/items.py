# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# 这里所有的UserId 都是我们这个系统的Id 不是p站账户Id


class UserStarPicItem(scrapy.Item):
    UserId = scrapy.Field()
    PicId = scrapy.Field()
    
    
class UserStarArtist(scrapy.Item):
    UserId = scrapy.Field()
    AritstId = scrapy.Field()
