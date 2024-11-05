from flask import Blueprint, render_template, request, redirect, url_for, flash
from controllers.calendar_controller import get_all_schedules, get_schedules_of_team_or_individual, create_schedule, update_schedule, delete_schedule
from models.project_model import UserProject
from models.calendar_model import Calendar
from flask_login import login_required, current_user

# Blueprint 객체 생성
calendar_bp = Blueprint('calendar', __name__)

# 마일스톤 목록 조회 로직
@calendar_bp.route('/<int:project_id>', methods=['GET'])
@login_required
def calendar_view(project_id):
    project = UserProject.find_by_user_and_project(current_user.id, project_id)
    if not project:
        flash("프로젝트를 찾을 수 없습니다.")
        return redirect(url_for('project_main.project_main_view', project_id=project_id))
    if team:
        calendars = get_schedules_of_team_or_individual(project_id, team)
    else:
        calendars = get_all_schedules(project_id)
    return render_template('calendar_back.html', project_id=project_id, calendars=calendars)

# 일정 생성 로직
@calendar_bp.route('/<int:project_id>/create', methods=['GET', 'POST'])
@login_required
def create_schedule_view(project_id):
    project = UserProject.find_by_user_and_project(current_user.id, project_id)
    if request.method == 'POST':
        title = request.form.get('title')
        place = request.form.get('place')
        start_date = request.form.get('start_date')
        due_date = request.form.get('due_date')
        team = request.form.get('team')
        color = request.form.get('color')
        content = request.form.get('content')
        important = request.form.get('important')
        message = create_schedule(project_id, title, place, start_date, due_date, team, color, content, important)
        flash(message)
        return redirect(url_for('calendar.calendar_view', project_id=project_id))
    return render_template('create_schedule_back.html', project=project)

# 일정 수정 로직
@calendar_bp.route('/<int:project_id>/<int:calendar_id>/update', methods=['GET', 'POST'])
@login_required
def update_schedule_view(project_id, calendar_id):
    project = UserProject.find_by_user_and_project(current_user.id, project_id)
    schedule = Calendar.find_by_id(calendar_id)
    if request.method == 'POST':
        title = request.form.get('title')
        place = request.form.get('place')
        start_date = request.form.get('start_date')
        due_date = request.form.get('due_date')
        team = request.form.get('team')
        color = request.form.get('color')
        content = request.form.get('content')
        important = request.form.get('important')
        message = update_schedule(calendar_id, title, place, start_date, due_date, team, color, content, important)
        flash(message)
        return redirect(url_for('calendar.calender_view', project_id=project_id))
    return render_template('update_schedule_backㄴ.html', project=project, schedule=schedule)

# 일정 삭제 로직
@calendar_bp.route('/<int:project_id>/<int:milestone_id>/delete', methods=['POST'])
@login_required
def delete_milestone_view(project_id, calendar_id):
    message = delete_schedule(calendar_id)
    flash(message)
    return redirect(url_for('calendar.calendar_view', project_id=project_id))
