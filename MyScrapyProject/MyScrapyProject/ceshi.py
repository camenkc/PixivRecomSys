from MysqlRW import SQLOS
from items import UserAccount
import datetime
import pymysql
import socket


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

SQLOS.GetUserAccount(6)

