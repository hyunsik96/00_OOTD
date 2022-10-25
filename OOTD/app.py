from distutils.debug import DEBUG
from flask import *
from flask_jwt_extended import *
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.ootd

app = Flask(__name__)
app.config.update(
    DEBUG = True,
    JWT_SECRET_KEY = 'secret ootd'
)
jwt = JWTManager(app)
admin_id = "1234"
admin_pw = "qwer"

@app.route('/')
def home():

    myname = "OOTD"

    return render_template('index.html', name = myname)

@app.route("/login", methods=['POST'])
def login_proc():
	
	# 클라이언트로부터 요청된 값
	input_data = request.get_json()
	user_id = input_data['id']
	user_pw = input_data['pw']

	# 아이디, 비밀번호가 일치하는 경우
	if (user_id == admin_id and
		user_pw == admin_pw):
		return jsonify(
			result = "success",
			# 검증된 경우, access 토큰 반환
			access_token = create_access_token(identity = user_id,
											expires_delta = False)
		)
	
	# 아이디, 비밀번호가 일치하지 않는 경우
	else:
		return jsonify(
			result = "Invalid Params!"
		)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)