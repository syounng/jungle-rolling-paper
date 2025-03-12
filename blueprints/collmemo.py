from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db  # database.py에서 MongoDB 객체 가져오기

# Blueprint 객체 생성
collmemo_bp = Blueprint('collmemo', __name__, url_prefix='/collmemo')

# 특정 동료의 메모 가져오기 (JWT 필요)
@collmemo_bp.route('/memos/<to_id>', methods=['GET'])
@jwt_required()  #JWT 보호 추가
def get_memos(to_id):
    """ 특정 동료(to_id)에게 남긴 메모 조회 """
    memos = list(db.memos.find({"to_id": to_id}, {"_id": 0}))  # _id 제외
    return jsonify(memos=memos), 200

# ✅ 메모 등록 (JWT 필요)
@collmemo_bp.route('/regist/memo', methods=['POST'])
@jwt_required()  #JWT 보호 추가
def regist_memo():
    """ 메모 저장 (로그인한 사용자만 가능) """
    data = request.get_json()
    to_id = data.get("to_id")
    nickname = data.get("nickname", "익명")  # 닉네임이 없으면 "익명" 사용
    content = data.get("content")
    from_id = get_jwt_identity()  # ✅ JWT에서 현재 사용자 ID 가져오기

    # 필수값 체크
    if not to_id or not content:
        return jsonify({"msg": "to_id와 content는 필수 입력 항목입니다."}), 400

    # MongoDB에 저장
    db.memos.insert_one({
        "from_id": from_id,  # JWT 사용자 ID 저장
        "to_id": to_id,
        "nickname": nickname,
        "content": content
    })

    return jsonify({"msg": "메모 등록 완료!"}), 201

# 특정 동료의 롤링페이퍼 화면 (JWT 필요)
@collmemo_bp.route('/rollingpaper/<to_id>')
@jwt_required()  # JWT 보호 추가
def rolling_paper(to_id):
    return render_template('colleagueList.html', to_id=to_id)
