from flask import Flask, jsonify, request, render_template, Blueprint, redirect, url_for
from pymongo import MongoClient
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, decode_token

# Flask 앱 설정
bp_callmemo = Blueprint('bp_callmemo', __name__)

# MongoDB 연결 (로컬 DB 사용)
client = MongoClient("mongodb://localhost:27017/")
db = client.jungle9
# ✅ 1. 특정 동료의 메모 가져오기
@bp_callmemo.route('/memos/<to_id>', methods=['GET'])
def get_memos(to_id):
    print(to_id)
    """ 특정 동료(to_id)에게 남긴 메모 조회 """
    id = db.users.find_one({'name':to_id})['id']
    memos = list(db.memos.find({"to_id": id}, {"_id": 0}))  # _id는 제외하고 가져오기
    return jsonify(memos=memos), 200



# ✅ 2. 메모 등록 (JWT 없이 누구나 가능)
@bp_callmemo.route('/regist/memo', methods=['POST'])
def regist_memo():
    cookies = request.cookies  # 요청에서 받은 쿠키 확인
    access_token = cookies.get("access_token_cookie")  # 특정 쿠키 값 확인
    
    if access_token:
        decoded_token = decode_token(access_token)
        from_id = decoded_token.get('sub')
        data = request.get_json()

        tmp = data.get("to_id")
        received_to_id = db.users.find_one({'name': tmp})['id']


        to_id = received_to_id
        nickname = data.get("nickname", "익명")  # 닉네임이 없으면 "익명" 사용
        content = data.get("content")
        from_id = from_id  # from_id는 고정된 값

        writer = db.users.find_one({'id': from_id})['name']

        # 필수값 체크
        if not to_id or not content:
            return jsonify({"msg": "to_id와 content는 필수 입력 항목입니다."}), 400

        # MongoDB에 저장
        db.memos.insert_one({
            "from_id": from_id,
            "to_id": to_id,
            "nickname": nickname,
            "content": content,
            "name": writer,
            "quiz": 'default',
        })

        return jsonify({"msg": "메모 등록 완료!"}), 201
        
    else:
        return jsonify({"msg": "쿠키가 포함되지 않았음"}), 400
    # current_user = get_jwt_identity()
    """ 메모 저장 (누구나 가능) """

# ✅ 3. 특정 동료의 롤링페이퍼 화면
@bp_callmemo.route('/rollingpaper/<to_id>')
@jwt_required()
def rolling_paper(to_id):
    current_user = get_jwt_identity()
    real_id = db.users.find_one({'name':to_id})['id']

    if current_user == real_id:
        return redirect(url_for('mymemo.my_rolling_paper'))
    else:
        return render_template('colleagueList.html', to_id=to_id)

