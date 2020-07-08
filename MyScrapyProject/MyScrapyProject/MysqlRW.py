from MyScrapyProject.items import UserAccount
from itemadapter import ItemAdapter

import pymysql.cursors

import datetime
from MyScrapyProject.spiders.PureSpiders import ScrapyForPicTagsClass
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
        newdict={}
        for tag in taglist:
            if(userdict.__contains__(tagdict[tag])):
                newdict[tagdict[tag]]=userdict[tagdict[tag]]+1
            else:
                newdict[tagdict[tag]]=1
        return newdict#输入用户tagdict,需要添加的taglist，和完整的tagdict



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
    
    def UpdateUsertag(userid,userdict):
        db=SQLOS.Connect_to_DB()
        cursor=db.cursor()
        try:
            for tagid,tagcount in userdict.items():
                if(cursor.execute("SELECT * FROM d_user_tag WHERE`userid`=%s AND `tagid`=%s",(userid,tagid))):
                    if tagcount==0:
                        cursor.execute("DELETE FROM d_user_tag WHERE `userid`=%s AND `tagid`=%s",(userid,tagid))#删除count为零的记录
                    else:
                        cursor.execute("UPDATE d_user_tag SET `count`=%s WHERE `userid`=%s AND `tagid`=%s ",(tagcount,userid,tagid))#更新tag
                else:
                    cursor.execute("INSERT INTO d_user_tag (`userid`,`tagid`,`count`) VALUE (%s,%s,%s)",(userid,tagid,tagcount))#没有数据的话插入一条新的数据
            db.commit()
            db.close()
            return 1
        except:
            db.rollback()
            db.close()
            return 0 #更新数据库中user的tag列表

                

    def AddStarImage(Userid,Imageid):
        if(SQLOS.CheckStarImage(Userid,Imageid)):
            return -1#数据库已有收藏的话 略过
        else:
            UserTag=SQLOS.GetUserTagDic(Userid) #从数据库拖数据下来
            #print(111)
            TagDict=SQLOS.GetTagDict() #从数据库拖dict下来
            #print(222)

            spider=ScrapyForPicTagsClass()
            pictag=spider.GetTagList(Imageid) #爬取图片tag
#            print(333)
            addtaglist=MYF.DictDif1(TagDict,pictag)#有哪些tag是没有的 组成一个list
 #           print(444)
            newdict=MYF.FullfillTag(TagDict,addtaglist)#更新本地tagdict为完整的tag（dict形式
  #          print(555)
            updatedict=MYF.DictDif2(TagDict,newdict) #需要补充进taglist的tag（dict形式）
   #         print(666)
    #        print(UserTag)
            newusertag=MYF.AddUserTag(UserTag,pictag,newdict)#更新本地用户的tagdict
     #       print(777)
            SQLOS.UpdateOneStarImage(Userid,Imageid) #更新数据库用户收藏列表
      #      print(888)
            SQLOS.UpdateTaglist(updatedict) #更新数据库Tag列表
       #     print(999)
            SQLOS.UpdateUsertag(Userid,newusertag) #更新数据库用户tag分析列表
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
    

          
   


