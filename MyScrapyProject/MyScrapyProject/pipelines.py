# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from MysqlRW import SQLOS
from itemadapter import ItemAdapter
import pymysql.cursors

class MyscrapyprojectPipeline:
    def process_item(self, item, spider):
        return item

class AddToUserStarImagePPL:
    def __init__(self):
        self.connect=SQLOS.Connect_to_DB()
    def process_item(self,item,spider):
        try:
            with self.connect.cursor() as cursor:
                sqlwrite="INSERT INTO `d_user_star_image`(`userid`,`imageid`,`add_date`)VALUES(%d,%d,%s)"
                cursor.execute(sqlwrite,(item.get("UserID",""),item.get("ImageID",""),item.get("Add_date","")))
            self.connect.commit()
        
        except Exception as e:
             pass
        return item
    def close_spider(self,spider):
        self.connect.close()


class AddToUserStarArtistPPL:
    def __init__(self):
        self.connect=SQLOS.Connect_to_DB()
    def process_item(self,item,spider):
        try:
            with self.connect.cursor() as cursor:
                sqlwrite="INSERT INTO `d_user_star_image`(`userid`,`artistid`,`add_date`)VALUES(%d,%d,%s)"
                cursor.execute(sqlwrite,(item.get("UserID",""),item.get("ArtistID",""),item.get("Add_date","")))
            self.connect.commit()
        
        except Exception as e:
             pass
        return item
    def close_spider(self,spider):
        self.connect.close()



