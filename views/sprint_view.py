# views/sprint_view.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from controllers.sprint_controller import (
    assign_backlogs_to_sprint, create_sprint, delete_backlog, get_sprints_with_backlogs, get_unassigned_product_backlogs, get_users_by_project_id, move_incomplete_backlogs_to_next_sprint, update_backlog_details, update_backlog_status, update_sprint, delete_sprint,
    get_all_product_backlogs, create_sprint_backlog
)
from controllers.calendar_controller import create_schedules, update_sprint_schedules, delete_sprint_schedules
from controllers.burnup_controller import increment_total_backlog, decrement_total_backlog
from controllers.burnup_controller import increment_total_backlog, decrement_total_backlog
from models.project_model import Project, UserProject
from flask_login import current_user, login_required
from models.calendar_model import Calendar

# 블루프린트 생성
sprint_bp = Blueprint('sprint', __name__)

@sprint_bp.route('/<int:project_id>', methods=['GET'])
@login_required 
def get_product_backlogs_view(project_id):
    if not current_user.is_authenticated:
        flash('로그인이 필요합니다.')  # 사용자에게 로그인이 필요하다는 메시지를 표시
        return redirect(url_for('auth.login'))  # 로그인 페이지로 리디렉트
    sprints = get_sprints_with_backlogs(project_id)
    backlogs = {
        'all_backlogs': get_all_product_backlogs(project_id),
        'unassigned_backlogs': get_unassigned_product_backlogs(project_id)
    } 
    users = get_users_by_project_id(project_id)
    return render_template('sprint.html', 
                           project=Project.find_by_id(project_id),
                           userproject=UserProject.find_by_user_and_project(current_user.id, project_id),
                           backlogs=backlogs, sprints=sprints, users=users, project_id=project_id)

# 스프린트 추가
@sprint_bp.route('/add-sprint', methods=['POST'])
@login_required 
def add_sprint():
    project_id = request.form['project_id']
    sprint_name = request.form['sprint_name']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    status = request.form.get('status', None)
    selected_backlogs = request.form.getlist('backlogs')
    # 쉼표로 구분된 문자열을 리스트로 변환
    selected_backlogs = [int(backlog_id) for item in selected_backlogs for backlog_id in item.split(',')]

    new_sprint, error = create_sprint(project_id, sprint_name, start_date, end_date, status)
    if new_sprint:
        assign_backlogs_to_sprint(new_sprint.sprint_id, selected_backlogs)
        create_schedules(current_user.id,project_id, sprint_name, None, start_date, end_date, True, 0, None, True)
        return redirect(url_for('sprint.get_product_backlogs_view', project_id=project_id, status=1))
    else:
        return redirect(url_for('sprint.get_product_backlogs_view', project_id=project_id, status=-1, error_message=error))

# 스프린트 수정
@sprint_bp.route('/edit-sprint/<int:sprint_id>/<int:project_id>', methods=['POST'])
def edit_sprint(sprint_id, project_id):
    sprint_name = request.form['sprint_name']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    selected_backlogs = request.form.getlist('backlogs')
    updates = {
        'name': sprint_name,
        'start_date': start_date,
        'end_date': end_date
    }
    
    updated_sprint = update_sprint(sprint_id, updates)
    if updated_sprint:
        assign_backlogs_to_sprint(sprint_id, selected_backlogs)
        update_sprint_schedules(project_id, sprint_name, start_date, end_date)    
        flash('스프린트가 성공적으로 수정되었습니다.')
    else:
        flash('스프린트 수정에 실패했습니다.')

    if project_id:
        return redirect(url_for('sprint.get_product_backlogs_view', project_id=project_id))
    else:
        # project_id가 None이면 기본 페이지로 리다이렉트
        return redirect(url_for('sprint.default_view'))

# 스프린트 삭제
@sprint_bp.route('/delete-sprint/<int:sprint_id>', methods=['POST'])
def delete_sprint_route(sprint_id):
    deleted_sprint = delete_sprint(sprint_id)
    if deleted_sprint:
        flash('스프린트가 성공적으로 삭제되었습니다.')
        delete_sprint_schedules(deleted_sprint.project_id, deleted_sprint.sprint_name)
        return redirect(url_for('sprint.get_product_backlogs_view', project_id=deleted_sprint.project_id))
    else:
        flash('스프린트 삭제에 실패했습니다.')
        return redirect(url_for('sprint.get_product_backlogs_view', project_id=sprint_id))
    

# 스프린트 백로그 생성
@sprint_bp.route('/create-sprint-backlog/<int:sprint_id>/<int:product_backlog_id>', methods=['POST'])
def add_sprint_backlog(sprint_id, product_backlog_id):
    content = request.form.get('content')
    user_id = request.form.get('user_id')
    backlog, error = create_sprint_backlog(sprint_id, product_backlog_id, content, user_id) 
    increment_total_backlog(request.form.get('project_id')) # 백로그 생성 시 총 백로그 수 증가

    if backlog:
        flash('스프린트 백로그가 성공적으로 추가되었습니다.')
    else:
        flash('스프린트 백로그 추가에 실패했습니다: ' + error)

    return redirect(url_for('sprint.get_product_backlogs_view', project_id=request.form.get('project_id')))

# 스프린트 백로그 수정
@sprint_bp.route('/edit-backlog-details/<int:backlog_id>', methods=['POST'])
def edit_backlog_details_view(backlog_id):
    content = request.form.get('content')
    user_id = request.form.get('user_id')
    success, message, project_id = update_backlog_details(backlog_id, content, user_id)
    flash(message)
    if success:
        return redirect(url_for('sprint.get_product_backlogs_view', project_id=project_id))
    return redirect(url_for('sprint.get_product_backlogs_view'))

@sprint_bp.route('/edit-backlog-status/<int:backlog_id>', methods=['POST'])
def edit_backlog_status_view(backlog_id):
    status = request.form.get('status')  
    success, message, project_id = update_backlog_status(backlog_id, status)
    flash(message)
    if success:
        return redirect(url_for('sprint.get_product_backlogs_view', project_id=project_id))
    return redirect(url_for('sprint.get_product_backlogs_view'))


@sprint_bp.route('/delete-backlog/<int:backlog_id>', methods=['POST'])
def delete_backlog_view(backlog_id):
    success, message, project_id = delete_backlog(backlog_id)
    flash(message)
    if not project_id or not success:
        flash("Invalid project ID or deletion failed.")
        return redirect(url_for('sprint.dashboard'))
    if success:
        decrement_total_backlog(project_id) # 백로그 삭제 시 총 백로그 수 감소
    return redirect(url_for('sprint.get_product_backlogs_view', project_id=project_id))

@sprint_bp.route('/move-backlogs/<int:sprint_id>/<int:project_id>', methods=['POST'])
def move_backlogs(sprint_id, project_id):
    success, message = move_incomplete_backlogs_to_next_sprint(sprint_id, project_id)
    if success:
        return jsonify({'message': '백로그가 다음 스프린트로 이전되었습니다.'}), 200
    else:
        return jsonify({'error': '백로그 이전 중 오류가 발생했습니다: ' + message}), 500

