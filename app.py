from flask import Flask, render_template, request, make_response, redirect, url_for, jsonify, Response
from pymongo import MongoClient
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from auth import bp
from database import db
from blueprints.collmemo import bp_callmemo  # collmemo Blueprint 가져오기
from blueprints.mymemo import mymemo_bp #mymemo Blueprint 가져오기
from blueprints.signup import bp_signup
from blueprints.upload import bp_upload
from bson import ObjectId
import gridfs

fs = gridfs.GridFS(db)
app = Flask(__name__)

#secretkey 설정
app.config['JWT_SECRET_KEY'] = 'secret_key'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']  # 쿠키에서 토큰을 추출
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 1800 # 15분 (900초)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 604800  # 7일 (604800초)
jwt = JWTManager(app)

#블루프린트 등록
app.register_blueprint(bp, url_prefix='/auth')
app.register_blueprint(bp_callmemo, url_prefix='/memo')
app.register_blueprint(mymemo_bp, url_prefix='/mymemo')
app.register_blueprint(bp_signup)
app.register_blueprint(bp_upload)

#db.memos.insert_one({'from_id': 'kdanny99naver.com@gmail.com', 'to_id':'jkh1447@gmail.com', 'nickname':'adb', 'content': 'ewfeca', 'name': '김대원', 'quiz': 'default'})

@app.route('/', methods=['GET'])
def home():
   return render_template('login.html')


@app.route('/join', methods=['GET'])
def join():
   return render_template('join.html')

@app.route('/join', methods=['POST'])
def join_confirm():
    
    name = request.form.get('name')
    id = request.form.get('id')
    pwd = request.form.get('pwd')

    id_is_exists = db.users.find_one({'id': id})
    print('아이디 중복 찾기 완료')
    print(id_is_exists)

    if id_is_exists:
        #아이디 이미 존재
        return jsonify(result = 'fail', message='같은 아이디가 이미 존재합니다.')
    
    #TODO; 비밀번호 해싱

    #사용자 저장
    new_user = {
        'name': name,
        'id': id,
        'pwd': pwd,
        'likes' : 0,
        'photo' : None
    }

    db.users.insert_one(new_user)

    # 회원가입 성공 반환
    return jsonify(result = 'success', message='회원가입이 완료되었습니다.')
    
    
@app.route('/mypage', methods=['GET'])
@jwt_required()
def mypage():
    current_user_id = get_jwt_identity()
    user_name = db.users.find_one({'id': current_user_id}, {'_id': False})['name'] # db에서 사용자 이름 가져오기
    memos_count = db.memos.count_documents({'_id': current_user_id})
    

    return render_template('myPage.html', user_name=user_name, memos_count=memos_count)

@app.route('/get-profile-picture/<user_name>')
def get_profile_picture(user_name):
   user = db.users.find_one({'name': user_name})
   if not user or 'photo' not in user:
        return jsonify({"error": "User or profile picture not found"}), 404

   file_id = user['photo']

   try:
        file = fs.get(ObjectId(file_id))
        return Response(file.read(), mimetype='image/png')  # MIME 타입을 맞춰서 반환
   except Exception as e:
      return jsonify({"error": str(e)}), 500
    

@app.route('/mainpage', methods=['GET'])
@jwt_required()
def mainpage():
#    token_receive = request.cookies.get('access_token')
   current_user = get_jwt_identity()
   users = db.users.find({}, {'_id':False, 'photo':False})
   current_user = db.users.find_one({'id': current_user})['name']

   return render_template('main.html', users = users, current_user = current_user)


if __name__ == '__main__':  
   app.run('0.0.0.0', port=5001, debug=True)