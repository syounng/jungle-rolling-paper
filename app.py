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


@app.route('/')
def home():
   users = db.users.find()
   return render_template('main.html', users = users)



if __name__ == '__main__':  
   app.run('0.0.0.0', port=5000, debug=True)


