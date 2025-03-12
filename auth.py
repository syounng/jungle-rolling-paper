# jwt 토큰 생성, 토큰 검증, 로그인/회원가입을 처리하는 파일
from database import db
from flask import Blueprint, jsonify, request, make_response, redirect, url_for, render_template
from flask_jwt_extended import JWTManager, decode_token, create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, jwt_required, get_jwt_identity
from datetime import datetime

bp = Blueprint('bp_auth', __name__)

jwt = JWTManager()

@bp.route('/login', methods=['POST'])
def login():

    id = request.form.get('id')
    pwd = request.form.get('pwd')

    user = db.users.find_one({'id': id, 'pwd': pwd}) #일치하는 유저 찾기
    print('로그인한 유저 : ')
    print(user)
    if user:
        #맞았을때, 토큰발행
        print('토큰 발행 시작')
        access_token = create_access_token(identity=id)
        print('access tocken 발행 완료')
        refresh_token = create_refresh_token(identity=id)
        print('refresh tocken 발행 완료')
        resp_obj = make_response(jsonify(result = 'success'))

        resp_obj.set_cookie('access_token_cookie', access_token, httponly=True, secure=True, samesite="Lax")
        resp_obj.set_cookie('refresh_token_cookie', refresh_token, httponly=True, secure=True, samesite="Lax")
        print('토큰을 쿠키로 전달 완료')
        
        return resp_obj
    else:
        #틀렸을때
        print('로그인 실패')
        return jsonify(result = 'failure')
    

# @bp.route('/refresh', methods=['GET'])
# @jwt_required(optional=True)
# def refresh():
#     # 클라이언트에서 전달한 Refresh Token은 자동으로 쿠키에서 읽힙니다.

#     access_token = request.cookies.get('access_token_cookie')

#     decoded_token = decode_token(access_token)
        
#     # 만료 시간 확인 (exp 값)
#     exp_timestamp = decoded_token.get("exp")  # exp는 UNIX 타임스탬프 형태로 반환
#     if exp_timestamp:
#         exp_datetime = datetime.utcfromtimestamp(exp_timestamp)
#         current_time = datetime.utcnow()

#         # 만료 여부 확인
#         if exp_datetime < current_time:
#             current_user = get_jwt_identity()  # Refresh Token에서 identity 가져오기

#             # 새로운 Access Token 생성
#             access_token = create_access_token(identity=current_user)

#             # 새로운 Access Token을 쿠키에 설정
#             response = make_response(jsonify(result = 'success', access_token="New Access Token Issued"))
#             response.set_cookie("access_token_cookie", access_token, httponly=True, secure=True, samesite="Lax")  # 쿠키에 새로운 Access Token 저장 (15분)
#             print('token refresh')
            
#             return response
            
#         else:
#             return jsonify(message="Access token is valid")
#     else:
#         return jsonify(message="Expiration time (exp) not found in token"), 400
    



@bp.route('/protected', methods=['GET'])
def protected():
    return jsonify(message="this is protected route")