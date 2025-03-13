from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from bson import ObjectId
mymemo_bp = Blueprint('mymemo', __name__)
@mymemo_bp.route('/memos/me/<to_id>', methods=['GET'])
@jwt_required()
def get_my_memos(to_id):
    current_user = get_jwt_identity()
    # :흰색_확인_표시: 해당 사용자의 메모 조회
    memos = list(db.memos.find({"to_id": current_user}, {"_id": 1, "nickname": 1, "name": 1, "content": 1, "quiz": 1}))
    # ObjectId를 문자열로 변환
    for memo in memos:
        memo["_id"] = str(memo["_id"])
    return jsonify(memos=memos), 200

@mymemo_bp.route('/rollingpaper/me', methods=['GET'])
@jwt_required()
def my_rolling_paper():
    current_user = get_jwt_identity()
    user = db.users.find_one({'id': current_user})
    if not user:
        return jsonify({"error": "User not found"}), 404
    user_name = user['name']
    return render_template('myList.html', to_id=user_name)

@mymemo_bp.route('/updateQuizState', methods=["POST"])
def updateQuizState():
    current_id = request.form.get('id')
    quiz_state = request.form.get('quizState')

    db.memos.update_one({'_id': ObjectId(current_id)}, {'$set': {'quiz': quiz_state}})
    return jsonify({'result': quiz_state})