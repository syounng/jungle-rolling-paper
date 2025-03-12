from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient

# Flask 앱 설정
app = Flask(__name__)

# MongoDB 연결 (로컬 DB 사용)
client = MongoClient("mongodb://localhost:27017/")
db = client.rolling_paper

# ✅ 내가 받은 메모 가져오기 (JWT 없이 가능)
@app.route('/memos/me/<to_id>', methods=['GET'])
def get_my_memos(to_id):
    """ 특정 사용자가 받은 메모 조회 (로그인 없이) """
    memos = list(db.memos.find({"to_id": to_id}, {"_id": 0}))  # _id 제외
    return jsonify(memos=memos), 200

# ✅ 내가 받은 롤링페이퍼 페이지 (JWT 없이 가능)
@app.route('/rollingpaper/me/<to_id>')
def my_rolling_paper(to_id):
    return render_template('myList.html', to_id=to_id)

# Flask 서버 실행
if __name__ == '__main__':
    app.run(debug=True)
