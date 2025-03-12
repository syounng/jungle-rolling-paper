from database import db
from flask import Blueprint, jsonify, request, make_response, render_template
import gridfs
from bson import ObjectId
import io

fs = gridfs.GridFS(db)

bp_upload = Blueprint('bp_upload', __name__)

@bp_upload.route('/upload-profile-picture', methods=['POST'])
def upload_profile_picture():
    if 'profilePicture' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['profilePicture']
    user_name = request.form.get('user_name')  # 'user_name'을 받아옴

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # 파일을 GridFS에 저장
    file_id = fs.put(file, filename=file.filename)

    db.users.update_one({"name": user_name}, {'$set': {"photo": file_id}})

    return jsonify({"message": "Upload successful", "file_id": str(file_id)}), 200