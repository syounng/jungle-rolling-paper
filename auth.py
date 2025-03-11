# jwt 토큰 생성, 토큰 검증, 로그인/회원가입을 처리하는 파일
from database import db
from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token

bp = Blueprint('bp_auth', __name__)

jwt = JWTManager()

@bp.route('/login', methods=['POST'])
def login():

    id = request.form.get('id')
    pwd = request.form.get('pwd')

    user = db.users.find_one({'id': id, 'pwd': pwd}) #일치하는 유저 찾기
    if user:
        #맞았을때, 토큰발행

        access_token = create_access_token(identity=id)
        refresh_token = create_refresh_token(identity=id)
        return jsonify(result = 'success', access_token=access_token, refresh_token=refresh_token)
    else:
        #틀렸을때
        return jsonify(result = 'failure')

@bp.route('/protected', methods=['GET'])
def protected():
    return jsonify(message="this is protected route")