# jwt 토큰 생성, 토큰 검증, 로그인/회원가입을 처리하는 파일
from database import db
from flask import Blueprint, jsonify, request, make_response, redirect, url_for, render_template
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, jwt_required, get_jwt_identity

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
        resp_obj = make_response(jsonify(result = 'success'))

        resp_obj.set_cookie('access_token_cookie', access_token, httponly=True, secure=True, samesite="Lax")
        resp_obj.set_cookie('refresh_token_cookie', refresh_token, httponly=True, secure=True, samesite="Lax")
        
        
        return resp_obj
    else:
        #틀렸을때
        return jsonify(result = 'failure')
    


@bp.route('/protected', methods=['GET'])
def protected():
    return jsonify(message="this is protected route")