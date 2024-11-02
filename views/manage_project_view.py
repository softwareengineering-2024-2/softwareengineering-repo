from flask import Blueprint, render_template, request, redirect, url_for, flash
from controllers.project_controller import create_project, join_project_by_link, get_user_projects, delete_project, set_profile
from models.project_model import UserProject, Project
from flask_login import login_required, current_user

# Blueprint 객체 생성
manage_project_bp = Blueprint('manage_project', __name__)

# 관리 페이지 로직 (사용자의 프로젝트 목록 모두 불러오기)
@manage_project_bp.route('/', methods=['GET'])
@login_required
def manage_project_view():
    userprojects = get_user_projects()
    return render_template('manage_project.html', userprojects=userprojects)

# 프로젝트 생성 로직
@manage_project_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_project_view():
    if request.method == 'POST':
        project_name = request.form.get('project_name')
        new_project = create_project(project_name)
        return redirect(url_for('manage_project.project_created_view', project_id=new_project.project_id))
    return render_template('create_project.html')

# 프로젝트 생성 완료 로직
@manage_project_bp.route('/project_created', methods=['GET'])
@login_required
def project_created_view():
    project_id = request.args.get('project_id')
    return render_template('project_created.html', project=Project.find_by_id(project_id))

# 프로젝트 참여 로직
@manage_project_bp.route('/join', methods=['GET', 'POST'])
@login_required
def join_project_view():
    if request.method == 'POST':
        project_link = request.form.get('project_link')
        message = join_project_by_link(project_link)
        flash(message)
        return redirect(url_for('manage_project.set_profile_view', project_id=Project.find_by_link(project_link).project_id))
    return render_template('join_project.html')

# 프로젝트 삭제 로직
@manage_project_bp.route('/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project_view(project_id):
    message = delete_project(project_id)
    flash(message)  # 프로젝트 삭제 결과 메시지를 플래시 메시지로 전달
    return redirect(url_for('manage_project.manage_project_view'))

# 사용자 프로필 설정 로직
@manage_project_bp.route('/<int:project_id>/profile', methods=['GET', 'POST'])
@login_required
def set_profile_view(project_id):
    if request.method == 'POST':
        user_name = request.form.get('name')
        user_role = request.form.get('role')
        message = set_profile(project_id, user_name, user_role)
        flash(message)
        return redirect(url_for('project_main.project_main_view', project_id=project_id))
    return render_template('profile.html', userproject=UserProject.find_by_user_and_project(current_user.id, project_id))
