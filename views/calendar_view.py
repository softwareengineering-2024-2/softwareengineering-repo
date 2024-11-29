from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from controllers.calendar_controller import (
    show_schedules,
    create_schedules,
    update_schedules,
    delete_schedules
)
from models.project_model import Project, UserProject
from models.calendar_model import Calendar
from flask_login import login_required, current_user
import traceback
from flask import current_app

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

        # 일정 조회
        schedules = show_schedules(project_id, current_user.id)

        # HTML 페이지를 렌더링
        return render_template('calendar_back.html', project=Project.find_by_id(project_id), userproject=userproject,schedules=schedules)
    except Exception as e:
    # 로그 출력
        current_app.logger.error(f"An error occurred: {e}")
        current_app.logger.error(traceback.format_exc())  # 상세 에러 스택 트레이스 출력
        return "Internal Server Error", 500

# 일정 조회
@calendar_bp.route('/schedules/<int:project_id>/', methods=['GET'])
def get_schedule(project_id):
    user_id = current_user.id
    schedule = show_schedules(project_id, user_id)
    return schedule

# 일정 추가
@calendar_bp.route('/<int:project_id>/', methods=['POST'])
def create_schedule(project_id):
    user_id = current_user.id
    title = request.json.get('title')
    place = request.json.get('place')
    start_date = request.json.get('start_date')
    due_date = request.json.get('due_date')
    team = request.json.get('team')
    color = request.json.get('color')
    content = request.json.get('content')
    important = request.json.get('important')
    create_schedules(user_id, project_id, title, place, start_date, due_date, team, color, content, important)
    return jsonify({"message": "success"})

#일정 수정
@calendar_bp.route('/update/<int:calendar_id>', methods=['POST'])
def update_schedule(calendar_id):
    title = request.json.get('title')
    place = request.json.get('place')
    start_date = request.json.get('start_date')
    due_date = request.json.get('due_date')
    team = request.json.get('team')
    color = request.json.get('color')
    content = request.json.get('content')
    important = request.json.get('important')
    update_schedules(calendar_id, title, place, start_date, due_date, team, color, content, important)
    return jsonify({"message": "success"})

# 일정 삭제
@calendar_bp.route('/<int:calendar_id>', methods=['DELETE'])
def delete_schedule(calendar_id):
    delete_schedules(calendar_id)
    return jsonify({"message": "success"})
    

