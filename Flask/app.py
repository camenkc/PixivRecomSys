#使用模板，为了将数据以html文档的格式展示出来


from flask_moment import Moment
from flask import Flask
from flask import render_template
from datetime import timedelta
from flask import redirect
import pymysql.cursors
from pixivpy3 import *


app = Flask(__name__) #创建一个swgi应用
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=5)
Moment(app)

#设置一个数据库链接

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

@app.route('/index')
def index():
    connection = get_conn()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `PixivID`, `Pixivpw`,`Username` `Userpw` FROM `d_user_account`"
            cursor.execute(sql)
            user_info = cursor.fetchall()
            return render_template("index.html", user_info = user_info)
    finally:
        connection.close()

    return render_template('index.html')

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



@app.route('/download/<PicID>')
def download(PicID):
    api = AppPixivAPI()
    api.login("CakeBaker.0308@gmail.com", "12138ckC")
    json_result = api.illust_detail(int(PicID))
    illust = json_result.illust
    api.download(illust.image_urls.large)
    print(">>> origin url: %s" % illust.image_urls['large'])
    return 'NowDownloading'

#跳转到这个页面之后 就下载PicID这个图片

    
@app.route('/time')
def time():
    return render_template('user/time.html')

if __name__=='__main__':
    app.run(port = 19990, debug = True)

    