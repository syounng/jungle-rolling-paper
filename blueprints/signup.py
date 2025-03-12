from flask import Flask, jsonify, request, render_template, Blueprint
from database import db  # database.py에서 MongoDB 객체 가져오기


bp_signup = Blueprint('bp_signup', __name__)

@bp_signup.route('/signup', methods=['GET'])
def signup():
    return render_template('join.html')
    