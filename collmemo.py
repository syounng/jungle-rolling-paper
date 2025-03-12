from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient

# Flask 앱 설정
app = Flask(__name__)

# MongoDB 연결 (로컬 DB 사용)
client = MongoClient("mongodb://localhost:27017/")
db = client.rolling_paper

# ✅ 1. 특정 동료의 메모 가져오기
@app.route('/memos/<to_id>', methods=['GET'])
def get_memos(to_id):
    """ 특정 동료(to_id)에게 남긴 메모 조회 """
    memos = list(db.memos.find({"to_id": to_id}, {"_id": 0}))  # _id는 제외하고 가져오기
    return jsonify(memos=memos), 200

# ✅ 2. 메모 등록 (JWT 없이 누구나 가능)
@app.route('/regist/memo', methods=['POST'])
def regist_memo():
    """ 메모 저장 (누구나 가능) """
    data = request.get_json()
    to_id = data.get("to_id")
    nickname = data.get("nickname", "익명")  # 닉네임이 없으면 "익명" 사용
    content = data.get("content")
    from_id = "anonymous"  # from_id는 고정된 값

    # 필수값 체크
    if not to_id or not content:
        return jsonify({"msg": "to_id와 content는 필수 입력 항목입니다."}), 400

    # MongoDB에 저장
    db.memos.insert_one({
        "from_id": from_id,
        "to_id": to_id,
        "nickname": nickname,
        "content": content
    })

    return jsonify({"msg": "메모 등록 완료!"}), 201

# ✅ 3. 특정 동료의 롤링페이퍼 화면
@app.route('/rollingpaper/<to_id>')
def rolling_paper(to_id):
    return render_template('colleagueList.html', to_id=to_id)

# Flask 서버 실행
if __name__ == '__main__':
    app.run(debug=True)
