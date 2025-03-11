from flask import Flask, render_template
from pymongo import MongoClient
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token
from auth import bp
from database import db

app = Flask(__name__)

#secretkey 설정
app.config['JWT_SECRET_KEY'] = 'secret_key'
jwt = JWTManager(app)

#블루프린트 등록
app.register_blueprint(bp, url_prefix='/auth')


db.users.insert_one({'name': '정권호', 'id':'jkh1447@gmail.com', 'pwd':'asdf1234', 'likes': 0, 'photo':'none'})
db.users.insert_one({'name': '김대원', 'id': 'kdanny99naver.com@gmail.com', 'pwd':'asdf1234', 'likes':0, 'photo':'none'})
db.memos.insert_one({'id':'jkh1447@gmail.com', 'receiver': 'jkh1447@gmail.com', 'nickname':'abc', 'content':'화이팅!'})

@app.route('/')
def home():
   users = db.users.find()
   return render_template('main.html', users = users)

@app.route('/login')
def login():
   return render_template('login.html')

@app.route('/join')
def join():
   return render_template('join.html')

if __name__ == '__main__':  
   app.run('0.0.0.0', port=5001, debug=True)


