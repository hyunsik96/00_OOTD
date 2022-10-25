from distutils.debug import DEBUG
from genericpath import isfile
from flask import *
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from datetime import *
import os
import jwt
import datetime


client = MongoClient('localhost', 27017)
db = client.ootd

app = Flask(__name__)
SECRET_KEY = 'redteam3'

@app.route('/')
def home():

    token_receive = request.cookies.get('jwToken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return render_template('index.html', loginUser=payload['id'])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/register')
def registerPage():
    return render_template('register.html')

@app.route('/registerUser', methods = ['POST'])
def registerUser():

    

    return render_template('add.html')

@app.route('/login.hs', methods = ['POST'])
def login():

    user_id = request.form['id']
    user_pw = request.form['pw']
    payload = {
    'id': user_id,
    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)    #언제까지 유효한지
    }

    access_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    resp = make_response(render_template('index.html'))
    resp.set_cookie(key='jwToken', value=access_token, max_age=3600)
    
    return resp

@app.route('/add.hs')
def addPage():
    return render_template('add.html')

@app.route('/addC.hs', methods = ['POST'])
def addClothes():
    f = request.files['file']
    cate = request.form['cate']
    loginUser = request.form['userId']

    fileName = secure_filename(f.filename)
    f.save(fileName)

    if(cate=='face'):
        originFile = db.ootd.find_one({'id': loginUser, 'cate': 'face'})
        if(isfile(originFile['fileName'])):
            os.remove(originFile['fileName'])
        db.ootd.delete_many({'id': loginUser, 'cate': 'face'})

    image = {'id': loginUser, 'cate': cate, 'fileName': fileName}
    db.ootd.insert_one(image)

    return redirect(url_for('addPage', code=1))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)