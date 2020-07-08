from MysqlRW import SQLOS
from MysqlRW import MYF
from items import UserAccount
import datetime
import pymysql
import socket
from spiders.PureSpiders import ScrapyForPicTagsClass

#spider=ScrapyForPicTagsClass()
#taglist=spider.GetTagList(79562473)
#print(taglist)
item=UserAccount()
item['PixivID']=777
item['Pixivpw']="gaiguodemima"
item['Username']="Username345"
item['Userpw']="Usermima321"
item['Create_date']=datetime.datetime.today()
item['Lastlogindate']=datetime.datetime.today()
item['Lastloginip']=socket.gethostbyname(socket.gethostname())
item['Logincount']=3
item['Usermode']=4

#print(MYF.AddUserTag({1:3,2:1,5:5},['轮船','车'],{'轮船':1,'车':4}))
#print(MYF.DictDif2({'数':1},{'数':1,'车':2}))
#SQLOS.UpdateTaglist({'东方':7})
#SQLOS.UpdateUsertag(1,{4:1,6:1,20:5})
for a in range(82121012,82121020):
    SQLOS.AddStarImage(1,a)
