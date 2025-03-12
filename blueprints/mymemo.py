from flask import Blueprint, jsonify, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db  # database.py에서 MongoDB 객체 가져오기

# Blueprint 객체 생성
mymemo_bp = Blueprint('mymemo', __name__, url_prefix='/mymemo')

# 내가 받은 메모 가져오기 (JWT 필요)
@mymemo_bp.route('/memos/me', methods=['GET'])
@jwt_required()  # JWT 보호 추가
def get_my_memos():
    """ 현재 로그인한 사용자가 받은 메모 조회 """
    current_user = get_jwt_identity()  #현재 로그인한 사용자 ID 가져오기

    # MongoDB에서 해당 사용자의 메모만 조회
    memos = list(db.memos.find({"to_id": current_user}, {"_id": 0}))

    return jsonify(memos=memos), 200

# 내가 받은 롤링페이퍼 페이지 (JWT 필요)
@mymemo_bp.route('/rollingpaper/me')
@jwt_required()  # JWT 보호 추가
def my_rolling_paper():
    current_user = get_jwt_identity()  #현재 로그인한 사용자 ID 가져오기
    return render_template('myList.html', to_id=current_user)
