# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from MyScrapyProject.MysqlRW import SQLOS
from itemadapter import ItemAdapter
import pymysql.cursors
from MyScrapyProject.MysqlRW import SQLOS
import datetime
class MyscrapyprojectPipeline:
    def process_item(self, item, spider):
        return item
#已完成爬取收藏图片ID的所有代码 请勿改变
class AddToUserStarImagePPL:
    def __init__(self):
        pass
    def open_spider(self,spider):
        self.connect=SQLOS.Connect_to_DB()
    def process_item(self,item,spider):
        print('Process Item now')
        try:
            with self.connect.cursor() as cursor:
                if(SQLOS.CheckStarImage(item.get("UserID"),item.get("ImageID"))):
                    pass
                else:
                    sqlwrite="INSERT INTO `d_user_star_image`(`userid`,`imageid`,`add_date`)VALUES(%s,%s,%s)"
                    cursor.execute(sqlwrite,(item.get("UserID"),item.get("ImageID"),datetime.datetime.today()))
                    SQLOS.AddStarImage(item.get("UserID"),item.get("ImageID"))
                cursor.connection.commit()
               
        
        except Exception as e:
            print(e)
        return item
    def close_spider(self,spider):
        self.connect.close()

#暂时不实现
class AddToUserStarArtistPPL:
    def __init__(self):
        pass
    def open_spider(self,spider):
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



