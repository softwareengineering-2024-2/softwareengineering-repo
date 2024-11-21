from models.project_model import UserProject, Project
from flask import Blueprint, redirect, render_template, request, jsonify, url_for
from models.sprint_model import Sprint, SprintBacklog
from controllers.sprint_controller import ( get_sprints_with_backlogs
)
from flask_login import current_user
from controllers.project_controller import get_user_projects
from database import db

# Blueprint 객체 생성
scrum_bp = Blueprint('scrum', __name__)

@scrum_bp.route('/<int:project_id>', methods=['GET'])
def scrum_view(project_id):
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))  # 로그인 페이지로 리디렉트
    
    project = Project.query.get(project_id)
    userprojects = get_user_projects()
    sprints = get_sprints_with_backlogs(project_id)
    
    # 선택된 스프린트 ID 가져오기 (쿼리 파라미터로 받거나 첫 번째 스프린트로 기본 설정)
    if not sprints:
        # 스프린트가 없는 경우 처리
        return render_template('scrum.html', message='현재 프로젝트에 스프린트가 없습니다.', project=project, userproject=userprojects)
    
    selected_sprint_id = request.args.get('sprint_id', default=(sprints[0].sprint_id if sprints else None))
    selected_sprint = Sprint.query.get(selected_sprint_id)

    if not selected_sprint:
        # 선택된 스프린트가 존재하지 않는 경우의 처리
        return render_template('scrum.html', message='선택된 스프린트를 찾을 수 없습니다.', project=project, userproject=userprojects, sprints=sprints, backlogs_by_status={})
    
    # 선택된 스프린트의 백로그 아이템 가져오기
    sprint_backlogs = SprintBacklog.query.filter_by(sprint_id=selected_sprint_id).all()
    
    # 상태별로 그룹화
    sprint_backlogs = SprintBacklog.query.filter_by(sprint_id=selected_sprint_id).all()
    statuses = ['To Do', 'In Progress', 'Done']
    backlogs_by_status = {status: [] for status in statuses}
    for backlog in sprint_backlogs:
        backlogs_by_status[backlog.status].append(backlog)

    return render_template('scrum.html', project=project, sprints=sprints, selected_sprint=selected_sprint, backlogs_by_status=backlogs_by_status, userproject=userprojects)

# 스프린트 백로그 상태 업데이트 API
@scrum_bp.route('/update_sprint_backlog_status', methods=['POST'])
def update_sprint_backlog_status():
    data = request.get_json()
    backlog_id = data.get('backlog_id')
    new_status = data.get('new_status')
    
    # 스프린트 백로그 아이템 가져오기
    backlog_item = SprintBacklog.query.get(backlog_id)
    if backlog_item:
        backlog_item.status = new_status
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Backlog item not found'}), 404