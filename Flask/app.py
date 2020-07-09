# 使用模板，为了将数据以html文档的格式展示出来

import sys
import os
from sys import path
path.append('..')
path.append(os.path.abspath(os.path.dirname(__file__)).split('MyScrapyProject')[0])

print(path)
from MyScrapyProject.MyScrapyProject.spiders.StarSpider import ScrapyForUserStarClass
from MyScrapyProject.MyScrapyProject.MysqlRW import *
from flask_moment import Moment
from flask import Flask,Response
from flask import render_template
from datetime import timedelta
from flask import redirect
import pymysql.cursors
from pixivpy3 import *

app = Flask(__name__)  # 创建一个swgi应用
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=5)
Moment(app)

UserAccount={}
NowRemTag=3
LikedTags={}
LikedTagsForBing={}
bingName=[]
bingName=[]
PicList1=[]
PicList2=[]

@app.route('/')
def JumpToIndex():
    return redirect('/login')


# 这里需求根据Userid返回一个Useraccount类型，
# 用来显示当前登录的用户，同时为用来确定是否绑定了Pix账号
@app.route('/index/<UserId>')
def index(UserId):
    global UserAccount 
    global NowRemTag
    global LikedTagsForBing
    global LikedTags
    global bingName
    global bingNum
    
    bingName=[]
    bingNum=[]
    print(1)
    LikedTagsForBing = SQLOS.GetMostTag(int(UserId),10)
    LikedTags = SQLOS.GetMostTag(int(UserId),20)
    UserAccount = SQLOS.GetUserAccount(UserId)
    print(len(LikedTagsForBing))
    print(len(LikedTags))
    for k,v in LikedTagsForBing.items():
        bingName.append(k)
        bingNum.append(int(v))
        print(k,v)

    return render_template('index.html', UserAccount=UserAccount)

@app.route('/bingtu/<userid>')
def BingTu(userid):
    
    global bingName
    global bingNum
    global UserAccount 
    return render_template('bingtu.html',bingName = bingName,bingNum=bingNum, UserAccount=UserAccount)
@app.route('/BindPixivID/<userid>,<pixid>')
def BindPixivID(userid, pixid):
    pixid = int(pixid)
    userid = int(userid)
    
    SQLOS.ChangeUserPixiv(userid, pixid,'0')
    UserAccount = SQLOS.GetUserAccount(userid)
    spider = ScrapyForUserStarClass()
    spider.GetUserStarPics(userid,pixid)
    return redirect('http://127.0.0.1:19990/index/' + str(userid))


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/status/<userid>')
def status(userid):
    if UserAccount.get('PixivID')==0:
        return render_template('status.html', UserAccount=UserAccount)
    return redirect('http://127.0.0.1:19990/status1/' + userid)


@app.route('/person/<userid>')
def person(userid):
    global UserAccount 
    return render_template('person.html', UserAccount=UserAccount)

@app.route('/list/static/images/<picName>')
def listGetImage(picName):
    image = open(os.path.curdir+"/static/images/{}".format(picName),'rb')
    resp = Response(image, mimetype="image/jpeg")
    return resp
@app.route('/list/<userid>')
def list(userid):
    global UserAccount 
    RankInWeek=[]
    RankInMonth=[]
    RankInWeek = SQLOS.GetRank('week',20)
    for p in range(0,19):
        print('p: ',p)
        if len(RankInWeek[p]['title'])>6:
            RankInWeek[p]['title'] = RankInWeek[p]['title'][:6]+'...'
        if len(RankInWeek[p]['author'])>6:
            RankInWeek[p]['author'] = RankInWeek[p]['author'][:6]+'...'
        RankInWeek[p]['ID']='static/images/'+str(RankInWeek[p]['ID'])+"_p0_square1200.jpg"
        print(RankInWeek[p]['ID'])
    print('Now Catch Rank In Month')
    RankInMonth = SQLOS.GetRank('month',10)
    for p in range(0,10):
        print('p: ',p)
        if len(RankInMonth[p]['title'])>6:
            RankInMonth[p]['title'] = RankInMonth[p]['title'][:6]+'...'
        if len(RankInMonth[p]['author'])>6:
            RankInMonth[p]['author'] = RankInMonth[p]['author'][:6]+'...'
        RankInMonth[p]['ID']='static/images/'+str(RankInMonth[p]['ID'])+"_p0_square1200.jpg"
        print(RankInMonth[p]['ID'])
    
    

    return render_template('list.html', UserAccount=UserAccount,RankInWeek=RankInWeek,RankInMonth=RankInMonth)


############################################最后一项
@app.route('/recommend/static/images/<picName>')
def getRemPicture(picName):
    image = open(os.path.curdir+"/static/images/{}".format(picName),'rb')
    resp = Response(image, mimetype="image/jpeg")
    return resp

@app.route('/recommend/<userid>')
def recommend(userid):
    
    global LikedTagsForBing
    global LikedTags
    global NowRemTag
    global UserAccount 
    TagsForRem=[]
    for tagdic,v in LikedTags.items():
        TagsForRem.append(tagdic)
    if NowRemTag>16:
        NowRemTag=0
    print(TagsForRem[NowRemTag])
    PicList1 = SQLOS.GetImageIdlist(TagsForRem[NowRemTag],20)
    for p in range(0,19):
        if len(PicList1[p]['title'])>6:
            PicList1[p]['title'] = PicList1[p]['title'][:6]+'...'
        if len(PicList1[p]['author'])>6:
            PicList1[p]['author'] = PicList1[p]['author'][:6]+'...'
        PicList1[p]['ID']='static/images/'+str(PicList1[p]['ID'])+"_p0_square1200.jpg"
        print(PicList1[p]['ID'])
    print(len(PicList1))
    NowRemTag+=1
    print(TagsForRem[NowRemTag])
    PicList2 = SQLOS.GetImageIdlist(TagsForRem[NowRemTag],20)
    for p in range(0,19):
        if len(PicList2[p]['title'])>6:
            PicList2[p]['title'] = PicList1[p]['title'][:6]+'...'
        if len(PicList2[p]['author'])>6:
            PicList2[p]['author'] = PicList2[p]['author'][:6]+'...'
        PicList2[p]['ID']='static/images/'+str(PicList2[p]['ID'])+"_p0_square1200.jpg"
        print(PicList1[p]['ID'])
    NowRemTag+=1
    print(len(PicList2))
    
    return render_template('recommend.html', UserAccount=UserAccount,PicList1=PicList1,PicList2=PicList2)

@app.route('/personinfoedit')
def perinfoedit():
    return render_template('personal_infoedit.html')


@app.route('/idedit/<userid>')
def id_edit(userid):
    
    global UserAccount 
    return render_template('id_edit.html',UserAccount=UserAccount)

@app.route('/status1/<userid>')
def status1(userid):
    global UserAccount 
    return render_template('status1.html', UserAccount=UserAccount)


# 检查登录信息是否正确
# 无此账户进入AccountNotFound.html(未写)
# 密码错误进入PswdIsIncorrect.html(未写)
# 登录信息正确则进入对应用户的主界面
@app.route('/LoginCheck/<username>,<userpswd>')
def LoginCheck(username, userpswd):
    info = SQLOS.UserLogin(username, userpswd)
    if info == 0:
        return render_template('AccountNotFound.html')
    if info == -1:
        return render_template('PswdIsIncorrect.html')
    return redirect('http://127.0.0.1:19990/index/' + str(info))


# 跳转到这个页面之后 就下载PicID这个图片
@app.route('/download/<PicID>')
def download(PicID):
    api = AppPixivAPI()
    api.login("CakeBaker.0308@gmail.com", "12138ckC")
    json_result = api.illust_detail(int(PicID))
    illust = json_result.illust
    api.download(illust.image_urls.large)
    print(">>> origin url: %s" % illust.image_urls['large'])
    return 'NowDownloading'


# 跳转到这个页面之后 就在数据库中检查是否有重复并加入数据库
# 成功注册后，就跳转到为这个用户呈现的主页面中
@app.route('/submittRegister/<Name>,<Pswd>')
def submittRegister(Name, Pswd):
    UserId = SQLOS.UserRegist(Name, Pswd)
    if (UserId == -1):
        return render_template('NameHasBeenRegistered.html')
    if (UserId == 0):
        return render_template('SomeThingWrongWithSQL.html')
    return redirect('http://127.0.0.1:19990/index/' + str(UserId))


@app.route('/time')
def time():
    return render_template('user/time.html')


if __name__ == '__main__':
    app.run(port=19990, debug=True)