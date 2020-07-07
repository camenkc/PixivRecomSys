#使用模板，为了将数据以html文档的格式展示出来


from flask_moment import Moment
from flask import Flask
from flask import render_template
from datetime import timedelta
from flask import redirect
import pymysql.cursors

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
    return redirect('/index')

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

@app.route('/main')
def login():
    return render_template('main.html')

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/time')
def time():
    return render_template('user/time.html')

if __name__=='__main__':
    app.run(port = 19990, debug = True)

    