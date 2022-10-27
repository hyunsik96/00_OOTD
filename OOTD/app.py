from flask import *
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from datetime import *
import jwt
import datetime
import time
import random
client = MongoClient('mongodb://test:test@localhost',27017)
# client = MongoClient('localhost', 27017)
db = client.ootd

app = Flask(__name__)
SECRET_KEY = 'redteam3'

@app.route('/')
def home():

    token_receive = request.cookies.get('jwToken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return redirect(url_for('mainOotd'))
    except jwt.ExpiredSignatureError:
        return render_template('index.html')
    except jwt.exceptions.DecodeError:
        return render_template('index.html')

@app.route('/register')
def registerPage():
    token_receive = request.cookies.get('jwToken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return redirect(url_for('mainOotd'))
    except jwt.ExpiredSignatureError:
        return render_template('register.html')
    except jwt.exceptions.DecodeError:
        return render_template('register.html')

@app.route('/registerUser', methods = ['GET', 'POST'])
def registerUser():
    try:
        id = request.form['id']
        pw = request.form['pw']
        if(db.user.find_one({'id': id}) is not None):
            return render_template('register.html', msg="중복된 아이디가 있습니다.")
        else:
            db.user.insert_one({'id': id, 'pw': pw})
            return render_template('index.html', msg='회원가입 성공!')
    except:
        return redirect(url_for('home'))

@app.route('/login.hs', methods = ['POST'])
def login():

    user_id = request.form['id']
    user_pw = request.form['pw']

    if(db.user.find_one({'id': user_id}) is not None):
        if(db.user.find_one({'id': user_id})['pw']==user_pw):
            payload = {
            'id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
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
        userId = payload['id']
        topList = db.ootd.find({'id': userId, 'cate': 'top'}).sort('_id', -1)
        bottomList = db.ootd.find({'id': userId, 'cate': 'bottom'}).sort('_id', -1)
        outerList = db.ootd.find({'id': userId, 'cate': 'outer'}).sort('_id', -1)
        shoesList = db.ootd.find({'id': userId, 'cate': 'shoes'}).sort('_id', -1)
        faceOne = db.ootd.find_one({'id': userId, 'cate': 'face'})

        lookT = db.look.find_one({'id': userId, 'cate': 'top'})
        lookB = db.look.find_one({'id': userId, 'cate': 'bottom'})
        lookO = db.look.find_one({'id': userId, 'cate': 'outer'})
        lookS = db.look.find_one({'id': userId, 'cate': 'shoes'})

        return render_template('main.html', loginUser=userId, top=topList, bottom=bottomList, outer=outerList, shoes=shoesList, face=faceOne, t=lookT, b=lookB, o=lookO, s=lookS)
    except jwt.ExpiredSignatureError:
        return render_template('index.html')
    except jwt.exceptions.DecodeError:
        return render_template('index.html')

@app.route('/deleteLookT.hs', methods= ['GET'])
def deleteLookT():
    token_receive = request.cookies.get('jwToken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        fileName = request.args.get('fn')
        userId = payload['id']
        db.ootd.delete_many({'id': userId, 'cate': 'top', 'fileName': fileName})
        return redirect(url_for('mainOotd'))
    except jwt.ExpiredSignatureError:
        return render_template('index.html')
    except jwt.exceptions.DecodeError:
        return render_template('index.html')

@app.route('/deleteLookB.hs', methods= ['GET'])
def deleteLookB():
    token_receive = request.cookies.get('jwToken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        fileName = request.args.get('fn')
        userId = payload['id']
        db.ootd.delete_many({'id': userId, 'cate': 'bottom', 'fileName': fileName})
        return redirect(url_for('mainOotd'))
    except jwt.ExpiredSignatureError:
        return render_template('index.html')
    except jwt.exceptions.DecodeError:
        return render_template('index.html')

@app.route('/deleteLookO.hs', methods= ['GET'])
def deleteLookO():
    token_receive = request.cookies.get('jwToken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        fileName = request.args.get('fn')
        userId = payload['id']
        db.ootd.delete_many({'id': userId, 'cate': 'outer', 'fileName': fileName})
        return redirect(url_for('mainOotd'))
    except jwt.ExpiredSignatureError:
        return render_template('index.html')
    except jwt.exceptions.DecodeError:
        return render_template('index.html')

@app.route('/deleteLookS.hs', methods= ['GET'])
def deleteLookS():
    token_receive = request.cookies.get('jwToken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        fileName = request.args.get('fn')
        userId = payload['id']
        db.ootd.delete_many({'id': userId, 'cate': 'shoes', 'fileName': fileName})
        return redirect(url_for('mainOotd'))
    except jwt.ExpiredSignatureError:
        return render_template('index.html')
    except jwt.exceptions.DecodeError:
        return render_template('index.html')

@app.route('/addLookT.hs', methods= ['GET'])
def addLookT():
    token_receive = request.cookies.get('jwToken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        fileName = request.args.get('fn')
        nowLook = db.ootd.find_one({'fileName': fileName})
        userId = payload['id']
        db.look.delete_many({'id': userId, 'cate': 'top'})
        db.look.insert_one({'id': userId, 'cate': 'top', 'fileName': fileName})
        return redirect(url_for('mainOotd'))
    except jwt.ExpiredSignatureError:
        return render_template('index.html')
    except jwt.exceptions.DecodeError:
        return render_template('index.html')

@app.route('/addLookB.hs', methods= ['GET'])
def addLookB():
    token_receive = request.cookies.get('jwToken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        fileName = request.args.get('fn')
        nowLook = db.ootd.find_one({'fileName': fileName})
        userId = payload['id']
        db.look.delete_many({'id': userId, 'cate': 'bottom'})
        db.look.insert_one({'id': userId, 'cate': 'bottom', 'fileName': fileName})
        return redirect(url_for('mainOotd'))
    except jwt.ExpiredSignatureError:
        return render_template('index.html')
    except jwt.exceptions.DecodeError:
        return render_template('index.html')

@app.route('/addLookO.hs', methods= ['GET'])
def addLookO():
    token_receive = request.cookies.get('jwToken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        fileName = request.args.get('fn')
        nowLook = db.ootd.find_one({'fileName': fileName})
        userId = payload['id']
        db.look.delete_many({'id': userId, 'cate': 'outer'})
        db.look.insert_one({'id': userId, 'cate': 'outer', 'fileName': fileName})
        return redirect(url_for('mainOotd'))
    except jwt.ExpiredSignatureError:
        return render_template('index.html')
    except jwt.exceptions.DecodeError:
        return render_template('index.html')

@app.route('/addLookS.hs', methods= ['GET'])
def addLookS():
    token_receive = request.cookies.get('jwToken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        fileName = request.args.get('fn')
        nowLook = db.ootd.find_one({'fileName': fileName})
        userId = payload['id']
        db.look.delete_many({'id': userId, 'cate': 'shoes'})
        db.look.insert_one({'id': userId, 'cate': 'shoes', 'fileName': fileName})
        return redirect(url_for('mainOotd'))
    except jwt.ExpiredSignatureError:
        return render_template('index.html')
    except jwt.exceptions.DecodeError:
        return render_template('index.html')

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
    nowTime = time.strftime('%Y%m%d%H%M%S')
    fileName = secure_filename(f.filename)
    ranInt = str(random.randint(1, 10000000000000000000000))
    if('.' in fileName):
        f.save('./static/img/' + ranInt + '.' + fileName.split('.')[1])
        if(cate=='face'):
            originFile = db.ootd.find_one({'id': loginUser, 'cate': 'face'})
            # if(isfile('/static/img/' + originFile['fileName'])):
            #     os.remove('/static/img/' + originFile['fileName'])
            db.ootd.delete_many({'id': loginUser, 'cate': 'face'})
        image = {'id': loginUser, 'cate': cate, 'fileName': ranInt + '.' + fileName.split('.')[1]}
        db.ootd.insert_one(image)
        return redirect(url_for('mainOotd', code=1))

    f.save('./static/img/' + nowTime + ranInt + '.' + fileName)

    if(cate=='face'):
        originFile = db.ootd.find_one({'id': loginUser, 'cate': 'face'})
        # if(isfile('/static/img/' + originFile['fileName'])):
        #     os.remove('/static/img/' + originFile['fileName'])
        db.ootd.delete_many({'id': loginUser, 'cate': 'face'})

    image = {'id': loginUser, 'cate': cate, 'fileName': nowTime + ranInt + '.' + fileName}
    db.ootd.insert_one(image)

    return redirect(url_for('mainOotd', code=1))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)