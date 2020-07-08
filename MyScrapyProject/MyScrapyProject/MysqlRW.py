import sys
sys.path.append('../')
from items import UserAccount
from itemadapter import ItemAdapter

import pymysql.cursors

import datetime
from spiders.PureSpiders import ScrapyForPicTagsClass
Logtype=("登录","注册","修改个人信息","绑定","添加收藏","移除收藏","添加关注","移除关注")

class MYF():
    def __init__(self):
        pass
    def DictDif2(dict1,dict2):
        dict3={}
        for key,value in dict2.items():
            if dict1.__contains__(key):
                pass
            else:
                dict3[key]=value
        return dict3 #输入两个dict，返回第二个dict减去第一个dict的dict
    def DictDif1(dict1,list1):
        Needadd=[]
        for tag in list1:
            if dict1.__contains__(tag):
                pass
            else:
                Needadd.append(tag)
        return Needadd #输入一个dict一个list，返回第一个dict中所没有第二个list的元素组成的list
    def FullfillTag(tagdict,taglist):
        lastmaxnum=len(tagdict)+1
        newdict=tagdict.copy()
        for tag in taglist:
            newdict[tag]=lastmaxnum
            lastmaxnum-=-1
        return newdict #输入原tag的dict和需要补充进去tag的list，返回新生成的tagdict
    def AddUserTag(userdict,taglist,tagdict):
        for tag in taglist:
            if(userdict.__contains__(tagdict[tag])):
                userdict[tagdict[tag]]-=-1
            else:
                userdict[tagdict[tag]]=1
        return userdict#输入用户tagdict,需要添加的taglist，和完整的tagdict



class SQLOS():
    def __init__(self):
        pass

    def WritetoLog(Userid,type,LogCentent):
        db=SQLOS.Connect_to_DB()
        cursor=db.cursor()
    
        sql_write="INSERT INTO d_log (`userid`,`logtype`,`logcontent`,`logtime`) VALUES(%s,%s,%s,%s)"
        try:
           
            cursor.execute(sql_write,(Userid,Logtype[type],LogCentent,datetime.datetime.today()))
          
            db.commit()
        except:
            
            db.rollback()
        db.close()#生成日志用函数，传入三个参数，用户ID、日志类别、日志信息

    def Connect_to_DB():
        connection = pymysql.connect(host='rm-bp10wr08s7nl319dcyo.mysql.rds.aliyuncs.com',
                        user='pixiv_rec_staff',
                        password='!5xDWVQJg4u3C9c',
                        db='pixiv_user',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)
        return connection

    def CheckStarImage(Userid,Imageid):
        db=SQLOS.Connect_to_DB()
        cursor=db.cursor()
        if cursor.execute("SELECT * from d_user_star_image WHERE `userid`=%s",Userid):
            if cursor.execute("SELECT * from d_user_star_image WHERE `imageid`=%s",Imageid):
                db.close()
                return 1
        db.close()
        return 0#查看是否已有 已有返回1 否则返回0
    def UpdateTaglist(AddTagDict):
        db=SQLOS.Connect_to_DB()
        cursor=db.cursor()
        try:
            for tagname,tagid in AddTagDict.items():
                cursor.execute("INSERT INTO d_tag_list (`TagName`,`TagID`) VALUES (%s,%s)",(tagname,tagid))
            db.commit()
            db.close()
            return 1
        except:
            db.rollback()
            return 0#向数据库中补充tag 传入一个dict
    
    def UpdateOneStarImage(Userid,Imageid):
        db=SQLOS.Connect_to_DB()
        cursor=db.cursor()
        try:
            cursor.execute("INSERT INTO d_user_star_image(`userid`,`imageid`,`add_date`) VALUES (%s,%s,%s)",(Userid,Imageid,datetime.datetime.today()))
            db.commit()
            db.close()
            return 1
        except:
            db.rollback()
            db.close()
            return 0 #向数据库中填入一条收藏数据
    
    def UpdateUsertag(userid,pictags):
        db=SQLOS.Connect_to_DB()
        cursor=db.cursor()
        try:
            for tag in pictags:
                #对于每一个新收藏图片的tag 先检查再taglist中有没有这个tag：
                sqlSelect='select `tagid` from `d_tag_list` where `tagname`= %s'
                info = cursor.execute(sqlSelect,(tag))
                if info ==0 : #说明这个tag不存在与tagList中
                    sqlInsert='insert into `d_tag_list`(`tagname`) values(%s)'
                    cursor.execute(sqlInsert,(tag))
                    info = cursor.execute(sqlSelect,(tag))
                info = cursor.fetchall()
                tagid=info[0]['tagid']
                #下面对这些tag在UserTag计数器中+1
                
                #首先判断是否存在于其中
                sqlSelect='select `count` from `d_user_tag` where `userid` = '+str(userid)+'  and `tagid` = '+str(tagid)+''
                info = cursor.execute(sqlSelect)
                if info==0:#说明这个tag不存在这个用户的收藏tag中
                    sqlInsert='insert into `d_user_tag`(`userid`,`tagid`,`count`) values(%s,%s,%s)'
                    cursor.execute(sqlInsert,(str(userid),str(tagid),str(1)))
                    countNumber=1
                else : #说明在这个tag中 需要把count+1
                    info = cursor.fetchall()
                    countNumber=info[0]['count']
                    countNumber=int(countNumber)+1
                    sqlUpdate='UPDATE `d_user_tag` SET `count`='+str(countNumber)+' WHERE `userid`='+str(userid)+' and `tagid`= '+str(tagid)
                    cursor.execute(sqlUpdate)
                #print('TagID：'+str(tagid)+' 已经成功更新 '+' 计数为：'+str(countNumber))
            db.commit()
            db.close()
            return 1
        except Exception as e:
            print(e)
            db.rollback()
            db.close()
            return 0 #更新数据库中user的tag列表

                

    def AddStarImage(Userid,Imageid):
        if(SQLOS.CheckStarImage(Userid,Imageid)):
            return -1#数据库已有收藏的话 略过
        else:
            spider=ScrapyForPicTagsClass()
            pictag=spider.GetTagList(Imageid) #爬取图片tag 
            SQLOS.UpdateOneStarImage(Userid,Imageid) #更新数据库用户收藏列表
            SQLOS.UpdateUsertag(Userid,pictag) #更新数据库用户tag分析列表 传入UserID和他新收藏的这张图片的tags
            SQLOS.WritetoLog(Userid,4,("添加收藏: %s"%Imageid))
            return 1 #向数据库中添加一条收藏记录，并更新tag_list与user_tag

            
        
    def AddUserAccount(UserAccount):
        db=SQLOS.Connect_to_DB()
        cursor=db.cursor()
        sql_write = "INSERT INTO d_user_account (`PixivID`,`Pixivpw`,`Username`,`Userpw`,`Usermode`,`create_date`,`lastlogindate`,`lastloginip`,`logincount`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
       
        try:
         
            cursor.execute(sql_write,(UserAccount.get("PixivID",""),UserAccount.get("Pixivpw",""),UserAccount.get("Username",""),UserAccount.get("Userpw",""),UserAccount.get("Usermode",""),UserAccount.get("Create_date",""),UserAccount.get("Lastlogindate",""),UserAccount.get("Lastloginip",""),UserAccount.get("Logincount","")))
            cursor.execute("SELECT LAST_INSERT_ID() from d_user_account as ID")
            flag=cursor.fetchall()
           
            print(db)
            db.commit()
            db.close()
            SQLOS.WritetoLog(flag[0]['LAST_INSERT_ID()'],1,"注册成功!")
            
      
           
            return 1
        except:
            print(444)
            db.rollback()
            db.close()
            return 0  #参数为UserAccount 向表中添加一个对象，如果成功返回1，并向日志中写一条注册成功日志。失败返回0
            
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
    

    def GetUserStarImage(ID):
        db=SQLOS.Connect_to_DB()
        cursor=db.cursor()
        StarImage=[]
        if cursor.execute("SELECT * from d_user_star_image WHERE `userid`=%s",ID):
            DataFromSQL=cursor.fetchall()
            for onedate in DataFromSQL:
                StarImage.append(onedate['imageid'])
            return StarImage
        else:
            return -1#得到指定ID的收藏图片列表，返回一个list

    def GetUserStarArtist(ID):
        db=SQLOS.Connect_to_DB()
        cursor=db.cursor()
        StarArtist=[]
        if cursor.execute("SELECT * from d_user_star_artist WHERE `userid`=%s",ID):
            DataFromSQL=cursor.fetchall()
            for onedate in DataFromSQL:
                StarImage.append(onedate['artistid'])
            return Artist
        else:
            return -1#得到指定ID的关注用户列表，返回一个list

    def GetUserTagDic(ID):
        db=SQLOS.Connect_to_DB()
        cursor=db.cursor()
        TagDict={}
        if cursor.execute("SELECT * from d_user_tag WHERE `userid`=%s",ID):
            DataFromSQL=cursor.fetchall()
            TagDict={}
            for onedate in DataFromSQL:
                TagDict[onedate['tagid']]=onedate['count']
            return TagDict
        else:
            return {}#得到指定ID的Tag分析列表，返回一个dict

    def GetTagDict():
        db=SQLOS.Connect_to_DB()
        cursor=db.cursor()
        cursor.execute("SELECT * from d_tag_list")
        DataFromSQL=cursor.fetchall()
        TagDict={}
        for onedate in DataFromSQL:
            TagDict[onedate['TagName']]=onedate['TagID']
        return TagDict#得到数据库储存Tag列表，返回一个dict 键值为tag

    def ChangeUserPixiv(ID,pixivID,pixivpw):
        User=SQLOS.GetUserAccount(ID)
        User['PixivID']=pixivID
        User['Pixivpw']=pixivpw
        SQLOS.EditUserAccount(ID,User)
        SQLOS.WritetoLog(ID,3,("修改绑定P站账号为 %s"%pixivID))#更改账户绑定p站账户，并向日志中写入一条记录
    
    def GetUserAccount(ID):
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
        db.close()#得到制定ID的用户账户信息，成功返回账户信息，未找到ID返回-1

    def SwitchUserMode(ID):
        User=SQLOS.GetUserAccount(ID)
        User['Usermode']=not User['Usermode']
        SQLOS.EditUserAccount(ID,User) #更改用户模式
        SQLOS.WritetoLog(ID,2,("修改账户类型为 %s"% (not User['Usermode'])))#更改账户类型，并向日志中写入一条记录
    

          
   


