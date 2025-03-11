from flask import Flask, render_template, request
from pymongo import MongoClient
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from auth import bp
from database import db

app = Flask(__name__)

#secretkey 설정
app.config['JWT_SECRET_KEY'] = 'secret_key'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']  # 쿠키에서 토큰을 추출
jwt = JWTManager(app)

#블루프린트 등록
app.register_blueprint(bp, url_prefix='/auth')


@app.route('/')
def home():
   return render_template('login.html')


@app.route('/main', methods=['GET'])
@jwt_required()
def main():
#    token_receive = request.cookies.get('access_token')

    current_user = get_jwt_identity()
    users = db.users.find()
    current_user = db.users.find_one({'id': current_user})['name']
    print(current_user)
    return render_template('main.html', users = users, current_user = current_user)


if __name__ == '__main__':  
   app.run('0.0.0.0', port=5000, debug=True)


