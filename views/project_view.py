from flask import Blueprint, render_template, request, redirect, url_for, flash
from controllers.project_controller import create_project, join_project_by_link, get_all_projects, delete_project

# Blueprint 객체 생성
project_bp = Blueprint('manage_project', __name__)

# 관리 페이지 로직
@project_bp.route('/manage_project', methods=['GET'])
def manage_project_view():
    projects = get_all_projects()  # 모든 프로젝트 목록 가져오기
    return render_template('manage_project.html', projects=projects)

# 프로젝트 생성 로직
@project_bp.route('/manage_project/create', methods=['GET', 'POST'])
def create_project_view():
    if request.method == 'POST':
        project_name = request.form.get('project_name')
        message = create_project(project_name)
        flash(message)  # 성공 메시지를 사용자에게 플래시 메시지로 전달
        return redirect(url_for('manage_project.manage_project_view'))  # 리디렉션 대신 템플릿 렌더링
    return render_template('create_project.html')

# 프로젝트 참여 로직
@project_bp.route('/manage_project/join', methods=['GET', 'POST'])
def join_project_view():
    if request.method == 'POST':
        project_link = request.form['project_link']
        message = join_project_by_link(project_link)
        flash(message)
        return redirect(url_for('manage_project.join_project_view'))
    return render_template('join_project.html')

# 프로젝트 삭제 로직
@project_bp.route('/manage_project/<int:project_id>/delete', methods=['POST'])
def delete_project_view(project_id):
    message = delete_project(project_id)
    flash(message)  # 프로젝트 삭제 결과 메시지를 플래시 메시지로 전달
    return redirect(url_for('manage_project.manage_project_view'))