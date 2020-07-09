# 使用模板，为了将数据以html文档的格式展示出来

import sys

sys.path.append('..')
from MyScrapyProject.MyScrapyProject.MysqlRW import *
from flask_moment import Moment
from flask import Flask
from flask import render_template
from datetime import timedelta
from flask import redirect
import pymysql.cursors
from pixivpy3 import *

app = Flask(__name__)  # 创建一个swgi应用
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=5)
Moment(app)


# 设置一个数据库链接

def get_conn():
    connection = pymysql.connect(host='rm-bp10wr08s7nl319dcyo.mysql.rds.aliyuncs.com',
                                 user='pixiv_rec_staff',
                                 password='!5xDWVQJg4u3C9c',
                                 db='pixiv_user',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


@app.route('/')
def JumpToIndex():
    return redirect('/login')


# 这里需求根据Userid返回一个Useraccount类型，
# 用来显示当前登录的用户，同时为用来确定是否绑定了Pix账号
@app.route('/index/<UserId>')
def index(UserId):
    UserId = int(UserId)
    UserAccount = SQLOS.GetAccountById(UserId)

    return render_template('index.html', UserAccount)


@app.route('/BindPixivID/<userid>,<pixid>')
def BindPixivID(userid, pixid):
    pixid = int(pixid)
    userid = int(userid)
    SQLOS.ChangeUserPixiv(userid, pixid)


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/status')
def status():
    return render_template('status.html')


@app.route('/person')
def person():
    return render_template('person.html')


@app.route('/list')
def list():
    return render_template('list.html')


@app.route('/recommend')
def recommend():
    return render_template('recommend.html')


@app.route('/personinfoedit')
def perinfoedit():
    return render_template('personal_infoedit.html')


@app.route('/idedit')
def id_edit():
    return render_template('id_edit.html')


@app.route('/status1')
def status1():
    return render_template('status1.html')

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
    return redirect('127.0.0.1:19990/index/' + str(UserId))


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
def submittRegister(name, pswd):
    UserId = SQLOS.UserRegist(name, pswd)
    if (UserId == -1):
        return render_template('NameHasBeenRegistered.html')
    if (UserId == 0):
        return render_template('SomeThingWrongWithSQL.html')
    return redirect('127.0.0.1:19990/index/' + str(UserId))


@app.route('/time')
def time():
    return render_template('user/time.html')


if __name__ == '__main__':
    app.run(port=19990, debug=True)