from flask import Blueprint, render_template, request, redirect, url_for, session
from controllers.project_controller import create_project, join_project, get_user_projects, delete_project, set_profile, check_pm
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
@manage_project_bp.route('/create', methods=['POST'])
@login_required
def create_project_view():
    project_name = request.form.get('project_name')
    new_project = create_project(project_name)
    return redirect(url_for('manage_project.project_created_view', project_id=new_project.project_id))

# 프로젝트 생성 완료 로직
@manage_project_bp.route('/project_created', methods=['GET'])
@login_required
def project_created_view():
    project_id = request.args.get('project_id')
    return render_template('project_created.html', project=Project.find_by_id(project_id))

# 프로젝트 링크 유효성 검사 로직
@manage_project_bp.route('/link_check', methods=['GET', 'POST'])
@login_required
def link_check_view():
    if request.method == 'POST':
        project_link = request.form.get('project_link')
        project = Project.find_by_link(project_link)
        if project:
            session['project_id'] = project.project_id
            session['project_name'] = project.project_name
            return render_template('join_project.html', link_check=1)
        else:
            return render_template('join_project.html', link_check=0)
    return render_template('join_project.html', link_check=-1)

# 프로젝트 참여 로직
@manage_project_bp.route('/join', methods=['POST'])
@login_required
def join_project_view():
    project_id = session['project_id']
    join_project(project_id)
    session.pop('project_id', None)
    session.pop('project_name', None)
    return redirect(url_for('manage_project.set_profile_view', project_id=project_id))
    
# 프로젝트 삭제 로직
@manage_project_bp.route('/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project_view(project_id):
    delete_project(project_id)
    return redirect(url_for('manage_project.manage_project_view'))

# 사용자 프로필 설정 로직
@manage_project_bp.route('/<int:project_id>/profile', methods=['GET', 'POST'])
@login_required
def set_profile_view(project_id):
    if request.method == 'POST':
        userproject = UserProject.find_by_user_and_project(current_user.id, project_id)
        current_role = userproject.user_role
        
        set_name = request.form.get('name')
        set_role = request.form.get('role')
        
        # PM이 이미 존재하는지 확인
        if current_role == "Member" and set_role == "PM(기획자)":
            if check_pm(project_id):
                return render_template('profile.html', userproject=UserProject.find_by_user_and_project(current_user.id, project_id), 
                        project=Project.find_by_id(project_id), pm_check=1)
            else:
                set_profile(project_id, set_name, set_role)
        else:
            set_profile(project_id, set_name, set_role)    
        return redirect(url_for('project_main.project_main_view', project_id=project_id))
    return render_template('profile.html', userproject=UserProject.find_by_user_and_project(current_user.id, project_id), 
                        project=Project.find_by_id(project_id), pm_check=0)
