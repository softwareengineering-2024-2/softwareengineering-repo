# scrum_view.py
from operator import and_
from models.project_model import UserProject, Project
from flask import Blueprint, redirect, render_template, request, jsonify, url_for
from models.sprint_model import Sprint, SprintBacklog
from models.project_model import UserProject
from controllers.sprint_controller import get_sprints_with_backlogs
from flask_login import current_user
from controllers.project_controller import get_user_projects
from controllers.burnup_controller import update_completed_backlog
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
    
    selected_sprint_id = request.args.get('sprint_id', default=(sprints[0]["sprint_id"] if sprints else None))
    selected_sprint = Sprint.query.get(selected_sprint_id)

    if not selected_sprint:
        # 선택된 스프린트가 존재하지 않는 경우의 처리
        return render_template('scrum.html', message='선택된 스프린트를 찾을 수 없습니다.', project=project, userproject=userprojects, sprints=sprints, backlogs_by_status={})

    # 선택된 스프린트의 백로그 아이템 가져오기, 사용자 정보 포함
    sprint_backlogs = (
        db.session.query(SprintBacklog, UserProject)
        .join(UserProject, and_(
            SprintBacklog.user_id == UserProject.user_id,
            UserProject.project_id == project_id
        ))
        .filter(SprintBacklog.sprint_id == selected_sprint_id)
        .all()
    )
    total_backlogs = len(sprint_backlogs)
    completed_backlogs = sum(1 for item in sprint_backlogs if item[0].status == 'Done')
    completion_percentage = (completed_backlogs / total_backlogs * 100) if total_backlogs > 0 else 0

    statuses = ['To Do', 'In Progress', 'Done']
    backlogs_by_status = {status: [] for status in statuses}
    for backlog, user in sprint_backlogs:
        backlog.user_name = user.user_name
        backlogs_by_status[backlog.status].append(backlog)

    return render_template('scrum.html', project=project, sprints=sprints, selected_sprint=selected_sprint, backlogs_by_status=backlogs_by_status, userproject=userprojects, completion_percentage=completion_percentage)

# 스프린트 백로그 상태 업데이트 API
@scrum_bp.route('/update_sprint_backlog_statuses', methods=['POST'])
def update_sprint_backlog_statuses():
    data = request.get_json()
    updated_backlogs = data.get('updated_backlogs', [])
    done_count = 0 # 'Done'으로 변경된 백로그 수

    for backlog_data in updated_backlogs:
        backlog_id = backlog_data.get('backlog_id')
        new_status = backlog_data.get('new_status')
        
        # 스프린트 백로그 아이템 가져오기
        backlog_item = SprintBacklog.query.get(backlog_id)
        if backlog_item:
            # 'Done'으로 상태가 변경되었는지 확인
            if backlog_item.status != 'Done' and new_status == 'Done':
                done_count += 1
            # 'Done'에서 다른 상태로 변경되었는지 확인
            elif backlog_item.status == 'Done' and new_status != 'Done':
                done_count -= 1
            backlog_item.status = new_status
        else:
            return jsonify({'success': False, 'message': f'Backlog item {backlog_id} not found'}), 404
    
    db.session.commit()

    # 완료된 백로그 수를 업데이트하는 로직 호출
    sprint_id = SprintBacklog.find_by_id(backlog_id).sprint_id
    project_id = Sprint.find_by_id(sprint_id).project_id
    update_completed_backlog(project_id, done_count)
    return jsonify({'success': True})