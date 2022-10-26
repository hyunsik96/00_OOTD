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
        return render_template('main.html', loginUser=payload['id'])
    except jwt.ExpiredSignatureError:
        return render_template('index.html')
    except jwt.exceptions.DecodeError:
        return render_template('index.html')

@app.route('/register')
def registerPage():
    return render_template('register.html')

@app.route('/registerUser', methods = ['POST'])
def registerUser():

    id = request.form['id']
    pw = request.form['pw']
    if(db.user.find_one({'id': id}) is not None):
        return render_template('register.html', msg="중복된 아이디가 있습니다.")
    else:
        db.user.insert_one({'id': id, 'pw': pw})
        return render_template('index.html', msg='회원가입 성공!')

@app.route('/login.hs', methods = ['POST'])
def login():

    user_id = request.form['id']
    user_pw = request.form['pw']

    if(db.user.find_one({'id': user_id}) is not None):
        if(db.user.find_one({'id': user_id})['pw']==user_pw):
            payload = {
            'id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)    #언제까지 유효한지
            }

            access_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            resp = make_response(redirect(url_for('mainOotd')))
            resp.set_cookie(key='jwToken', value=access_token, max_age=3600)
            
            return resp
    return render_template('index.html', msg='회원정보 조회 실패!')

@app.route('/main.hs')
def mainOotd():
    token_receive = request.cookies.get('jwToken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return render_template('main.html', loginUser=payload['id'])
    except jwt.ExpiredSignatureError:
        return render_template('main.html')
    except jwt.exceptions.DecodeError:
        return render_template('main.html')

@app.route('/add.hs')
def addPage():
    token_receive = request.cookies.get('jwToken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return render_template('add.html', loginUser=payload['id'])
    except jwt.ExpiredSignatureError:
        return render_template('index.html')
    except jwt.exceptions.DecodeError:
        return render_template('index.html')

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

    return redirect(url_for('mainOotd', code=1))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)