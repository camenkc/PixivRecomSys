from MyScrapyProject.items import UserAccount
from itemadapter import ItemAdapter
import pymysql.cursors

class SQLOS():
    def __init__(self):
        pass



    def Connect_to_DB():
        connection = pymysql.connect(host='rm-bp10wr08s7nl319dcyo.mysql.rds.aliyuncs.com',
                        user='pixiv_rec_staff',
                        password='!5xDWVQJg4u3C9c',
                        db='pixiv_user',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)
        return connection

    def AddUserAccount(UserAccount):
        db=SQLOS.Connect_to_DB()
        cursor=db.cursor()
        sql_write = "INSERT INTO d_user_account (`PixivID`,`Pixivpw`,`Username`,`Userpw`,`Usermode`,`create_date`,`lastlogindate`,`lastloginip`,`logincount`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
       
        try:
    
            cursor.execute(sql_write,(UserAccount.get("PixivID",""),UserAccount.get("Pixivpw",""),UserAccount.get("Username",""),UserAccount.get("Userpw",""),UserAccount.get("Usermode",""),UserAccount.get("Create_date",""),UserAccount.get("Lastlogindate",""),UserAccount.get("Lastloginip",""),UserAccount.get("Logincount","")))
        
      
            db.commit()
            return 1
        except:
        
            db.rollback()
            return 0
         
        db.close()#参数为UserAccount 向表中添加一个对象，如果成功返回1，失败返回0
    def EditUserAccount(ID,UserAccount):
        db=SQLOS.Connect_to_DB()
        cursor=db.cursor()
        if cursor.execute("SELECT * from d_user_account WHERE `ID`=%s",ID):

             try:
                cursor.execute("UPDATE d_user_account SET `PixivID`=%s,`Pixivpw`=%s,`Username`=%s,`Userpw`=%s,`Usermode`=%s,`lastlogindate`=%s,`lastloginip`=%s,`logincount`=%s WHERE ID=%s",(UserAccount.get("PixivID",""),UserAccount.get("Pixivpw",""),UserAccount.get("Username",""),UserAccount.get("Userpw",""),UserAccount.get("Usermode",""),UserAccount.get("Lastlogindate",""),UserAccount.get("Lastloginip",""),UserAccount.get("Logincount",""),ID))
                db.commit()
                return 1
             except:
                db.rollback()
                print(333)
                return 0
        else:
            return -1#更改制定ID的用户账户信息，成功返回1，失败返回0，未找到ID返回-1
    def GetUserAccount(ID):#得到制定ID的用户账户信息，成功返回账户信息，未找到ID返回-1
        db=SQLOS.Connect_to_DB()
        cursor=db.cursor()
        UserAC=UserAccount()
        if cursor.execute("SELECT * from d_user_account WHERE `ID`=%s",ID):
            DataFromSQL=cursor.fetchall()
            UserAC['ID']=DataFromSQL[0]['ID']
            UserAC['PixivID']=DataFromSQL[0]['PixivID']
            UserAC['Pixivpw']=DataFromSQL[0]['Pixivpw']
            UserAC['Username']=DataFromSQL[0]['Username']
            UserAC['Userpw']=DataFromSQL[0]['Userpw']
            UserAC['Usermode']=DataFromSQL[0]['Usermode']
            UserAC['Create_date']=DataFromSQL[0]['create_date']
            UserAC['Lastlogindate']=DataFromSQL[0]['lastlogindate']
            UserAC['Lastloginip']=DataFromSQL[0]['lastloginip']
            UserAC['Logincount']=DataFromSQL[0]['logincount']
            return UserAC
        else:
            return -1
        db.close()
