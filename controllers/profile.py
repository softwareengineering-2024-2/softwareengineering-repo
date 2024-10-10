from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
import os

# 블루프린트 생성
profile_bp = Blueprint('profile', __name__)

# 사진파일 업로드를 위한 경로(로직 아직 미완성)
# UPLOAD_FOLDER = 'static/uploads'  # 업로드할 폴더 설정
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # 폴더가 없으면 생성

@profile_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    first_time = request.args.get('first_time', 'false')

    if request.method == 'POST':
        # 프로필 수정 
        name = request.form.get('name')
        role = request.form.get('role')

        # 사진 저장 로직인데 아직 미완성
        # if 'picture' in request.files:
        #     picture = request.files['picture']
        #     if picture:
        #         picture_filename = f"{current_user.id}_profile_pic.jpg"
        #         picture_path = os.path.join('static/uploads', picture_filename)
        #         picture.save(picture_path)

        #         current_user.profile_pic = picture_path

        # 세션 업데이트
        session["user_info"]["name"] = name
        session["user_info"]["role"] = role
        # 사진 저장 로직도 필요

        flash('프로필이 성공적으로 수정되었습니다.')

        if first_time:
            if not session.get('project_name'):
                return redirect(url_for('create_project.create_project'))
            
        return redirect(url_for('index')) # 프로필 수정 시 홈 화면으로

    return render_template('profile.html', current_user=current_user)

@profile_bp.route('/start_project_creation', methods=['POST'])
@login_required
def start_project_creation():
    session['first_project_creation'] = True
    return '', 204 # No content