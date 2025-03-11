from flask import Flask, jsonify, request, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from pymongo import MongoClient

# Flask 앱 설정
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # JWT 비밀키 설정
jwt = JWTManager(app)

# MongoDB 연결 (로컬 DB 사용)
client = MongoClient("mongodb://localhost:27017/")
db = client.rolling_paper

# 더미 사용자 데이터 (실제 환경에서는 DB 사용)
users = {
    "testuser": {"password": "testpassword", "role": "admin"},
    "anotheruser": {"password": "anotherpassword", "role": "user"}
}

# ✅ 1. 로그인 엔드포인트 (JWT 발급)
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user = users.get(username, None)
    if user and user['password'] == password:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    
    return jsonify({"msg": "Bad username or password"}), 401

# ✅ 2. 특정 동료의 메모 가져오기 (JWT 인증 필요)
@app.route('/memos/<to_id>', methods=['GET'])
@jwt_required()
def get_memos(to_id):

    # 문제가 있을 가능서이 있다.
    """ 특정 동료(to_id)에게 남긴 메모 조회 """
    current_user = get_jwt_identity()  # 현재 로그인한 사용자 ID

    # MongoDB에서 to_id 기준으로 메모 가져오기
    memos = list(db.memos.find({"to_id": to_id}, {"_id": 0}))

    return jsonify(memos=memos, current_user=current_user), 200

# ✅ 3. 메모 등록 엔드포인트 (JWT 인증 필요)
@app.route('/regist/memo', methods=['POST'])
@jwt_required()
def regist_memo():
    data = request.get_json()
    from_id = get_jwt_identity()  # 현재 로그인한 사용자 ID
    to_id = data.get("to_id")
    nickname = data.get("nickname", from_id)  # 닉네임이 없으면 from_id 사용
    content = data.get("content")

    if not content:
        return jsonify({"msg": "메모 내용을 입력하세요"}), 400

    db.memos.insert_one({"from_id": from_id, "to_id": to_id, "nickname": nickname, "content": content})
    return jsonify({"msg": "메모 등록 완료!"}), 201

# ✅ 4. 특정 동료의 롤링페이퍼 화면
# 여기 확인해봐야될 필요있음
@app.route('/rollingpaper/<to_id>')
def rolling_paper(to_id):
    return render_template('colleagueList.html', to_id=to_id)

if __name__ == '__main__':
    app.run(debug=True)