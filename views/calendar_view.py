from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from controllers.calendar_controller import (
    get_all_schedules,
    get_schedules_of_team_or_personal,
    create_schedule,
    update_schedule,
    delete_schedule
)
from models.project_model import Project, UserProject
from models.calendar_model import Calendar
from flask_login import login_required, current_user

# Blueprint 객체 생성
calendar_bp = Blueprint('calendar', __name__)

# HTML 페이지 렌더링
@calendar_bp.route('/<int:project_id>', methods=['GET'])
@login_required
def calendar_view(project_id):
    try:
        userproject = UserProject.find_by_user_and_project(current_user.id, project_id)
        if not userproject:
            flash("프로젝트를 찾을 수 없습니다.")
            return redirect(url_for('project_main.project_main_view', project_id=project_id))

        # HTML 페이지를 렌더링
        return render_template('calendar_back.html', project=Project.find_by_id(project_id), userproject=userproject)
    except Exception as e:
        print(f"Error: {e}")  # 오류 로그 출력
        return "Internal Server Error", 500

# 일정 JSON 반환
@calendar_bp.route('/<int:project_id>/schedules', methods=['GET'])
@login_required
def get_schedules(project_id):
    try:
        userproject = UserProject.find_by_user_and_project(current_user.id, project_id)
        if not userproject:
            return jsonify({"error": "프로젝트를 찾을 수 없습니다."}), 404

        team = request.args.get('team', 'true').lower() == 'true'
        personal = request.args.get('personal', 'true').lower() == 'true'

        if team and personal:
            schedules = get_all_schedules(project_id)
        elif team:
            schedules = get_schedules_of_team_or_personal(project_id, team=True)
        elif personal:
            schedules = get_schedules_of_team_or_personal(project_id, team=False)
        else:
            schedules = []

        # JSON 응답 준비
        schedules_list = []
        for schedule in schedules:
            schedules_list.append({
                "title": schedule.title,
                "start_date": schedule.start_date.isoformat(),
                "due_date": schedule.due_date.isoformat(),
                "color": schedule.color,
            })

        return jsonify(schedules_list)
    except Exception as e:
        print(f"Error: {e}")  # 오류 로그 출력
        return jsonify({"error": "Internal Server Error"}), 500

# 일정 생성 로직
@calendar_bp.route('/<int:project_id>/create', methods=['GET', 'POST'])
@login_required
def create_schedule_view(project_id):
    userproject = UserProject.find_by_user_and_project(current_user.id, project_id)
    if request.method == 'POST':
        title = request.form.get('title')
        place = request.form.get('place')
        start_date = request.form.get('start_date')
        due_date = request.form.get('due_date')
        team = request.form.get('category') == 'team'
        color = request.form.get('color')
        content = request.form.get('content')
        important = request.form.get('important') == 'on'
        message = create_schedule(project_id, title, place, start_date, due_date, team, color, content, important)
        flash(message)
        return redirect(url_for('calendar.calendar_view', project_id=project_id))
    return render_template('create_schedule_back.html', project=Project.find_by_id(project_id), userproject=userproject)

# 일정 수정 로직
@calendar_bp.route('/<int:project_id>/<int:calendar_id>/update', methods=['GET', 'POST'])
@login_required
def update_schedule_view(project_id, calendar_id):
    userproject = UserProject.find_by_user_and_project(current_user.id, project_id)
    schedule = Calendar.find_by_id(calendar_id)
    if request.method == 'POST':
        title = request.form.get('title')
        place = request.form.get('place')
        start_date = request.form.get('start_date')
        due_date = request.form.get('due_date')
        team = request.form.get('team') == 'team'
        color = request.form.get('color')
        content = request.form.get('content')
        important = request.form.get('important') == 'on'
        message = update_schedule(calendar_id, title, place, start_date, due_date, team, color, content, important)
        flash(message)
        return redirect(url_for('calendar.calendar_view', project_id=project_id))
    return render_template('calendar_back.html', project=Project.find_by_id(project_id), userproject=userproject, schedule=schedule)

# 일정 삭제 로직
@calendar_bp.route('/<int:project_id>/<int:calendar_id>/delete', methods=['POST'])
@login_required
def delete_schedule_view(project_id, calendar_id):
    message = delete_schedule(calendar_id)
    flash(message)
    return redirect(url_for('calendar.calendar_view', project_id=project_id))
