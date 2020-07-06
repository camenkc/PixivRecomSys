#使用模板，为了将数据以html文档的格式展示出来


from flask_moment import Moment
from flask import Flask
from flask import render_template
from datetime import timedelta
from flask import redirect


app = Flask(__name__) #创建一个swgi应用
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=5)
Moment(app)


@app.route('/')
def JumpToIndex():
    return redirect('/index')

@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/time')
def time():
    return render_template('user/time.html')

    
if __name__=='__main__':
    app.run(port = 19990, debug = True)

    