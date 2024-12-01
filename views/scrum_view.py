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
from flask_login import current_user, login_required

# Blueprint 객체 생성
scrum_bp = Blueprint('scrum', __name__)

@scrum_bp.route('/<int:project_id>', methods=['GET'])
@login_required
def scrum_view(project_id):
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))  # 로그인 페이지로 리디렉트
    
    project = Project.query.get(project_id)
    if not project:
        return render_template(
            'scrum.html',
            message='프로젝트를 찾을 수 없습니다.',
            project=None,
            userproject=[],
            sprints=[],
            backlogs_by_status={},
            completion_percentage=0,
            project_id=project_id
        )
    
    userprojects = get_user_projects()
    sprints = get_sprints_with_backlogs(project_id)

    # 스프린트가 없는 경우 처리
    if not sprints:
        return render_template(
            'scrum.html',
            message='현재 프로젝트에 스프린트가 없습니다.',
            project=project,
            userproject=userprojects,
            sprints=[],
            backlogs_by_status={},
            completion_percentage=0,
            project_id=project_id
        )

    selected_sprint_id = request.args.get('sprint_id', default=(sprints[0]["sprint_id"] if sprints else None))
    if selected_sprint_id is not None:
        selected_sprint_id = int(selected_sprint_id)
    selected_sprint = Sprint.query.get(selected_sprint_id)

    if not selected_sprint:
        # 선택된 스프린트가 존재하지 않는 경우의 처리
        return render_template(
            'scrum.html',
            message='선택된 스프린트를 찾을 수 없습니다.',
            project=project,
            userproject=userprojects,
            sprints=sprints,
            backlogs_by_status={},
            completion_percentage=0
        )
    
    # sprints 리스트에서 selected_sprint의 is_past_due 값을 가져옴
    selected_sprint_dict = next((sprint for sprint in sprints if sprint['sprint_id'] == selected_sprint_id), None)
    is_past_due = selected_sprint_dict['is_past_due'] if selected_sprint_dict else False

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

    return render_template('scrum.html', project=project, sprints=sprints, selected_sprint=selected_sprint, backlogs_by_status=backlogs_by_status, userproject=userprojects, completion_percentage=completion_percentage, is_past_due=is_past_due, project_id=project_id)

# 스프린트 백로그 상태 업데이트 API
@scrum_bp.route('/update_sprint_backlog_statuses', methods=['POST'])
def update_sprint_backlog_statuses():
    data = request.get_json()
    updated_backlogs = data.get('updated_backlogs', [])
    sprint_ids = set()
    done_count_map = {} # 각 스프린트별 'Done' 상태 변경 카운트 초기화
    
    try:
        for backlog_data in updated_backlogs:
            backlog_id = backlog_data.get('backlog_id')
            new_status = backlog_data.get('new_status')
            backlog_item = SprintBacklog.query.get(backlog_id)
            if not backlog_item:
                return jsonify({'success': False, 'message': f'Backlog item {backlog_id} not found'}), 404

            current_status = backlog_item.status
            backlog_item.status = new_status
            if current_status != 'Done' and new_status == 'Done':
                done_count_map[backlog_item.sprint_id] = done_count_map.get(backlog_item.sprint_id, 0) + 1
            elif current_status == 'Done' and new_status != 'Done':
                done_count_map[backlog_item.sprint_id] = done_count_map.get(backlog_item.sprint_id, 0) - 1
            sprint_ids.add(backlog_item.sprint_id)

        for sprint_id in sprint_ids:
            sprint = Sprint.query.get(sprint_id)
            if not sprint:
                return jsonify({'success': False, 'message': f'Sprint {sprint_id} not found'}), 404
            if done_count_map.get(sprint_id, 0) != 0:
                update_completed_backlog(sprint.project_id, done_count_map[sprint_id])

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

    return jsonify({'success': True}), 200