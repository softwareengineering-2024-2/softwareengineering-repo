from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required, current_user
from controllers.calendar_controller import show_schedules
from controllers.todolist_controller import change_todo_status, delete_todos, show_todos, update_todos, write_todo
from models.project_model import UserProject, Project
from controllers.sprint_controller import get_current_sprint_backlogs


# 블루프린트 생성
project_main_bp = Blueprint('project_main', __name__)

@project_main_bp.route('/<int:project_id>')
@login_required
def project_main_view(project_id):
    userproject=UserProject.find_by_user_and_project(current_user.id, project_id)
    project = Project.find_by_id(project_id)
    # 현재 스프린트 백로그 데이터 가져오기
    current_sprint_backlogs = get_current_sprint_backlogs(current_user.id, project_id)

    # `progress_percentage`가 존재하는지 확인하고 전달
    progress_percentage = current_sprint_backlogs.get('progress_percentage', 0) if current_sprint_backlogs else 0

    # todo 리스트 전달하기
    todo_list = show_todos(project_id, current_user.id)

    return render_template(
        'main.html',
        userproject=userproject,
        project=project,
        progress_percentage=progress_percentage,
        current_sprint_backlogs=current_sprint_backlogs,
        todo_list = todo_list
    )

# 투두리스트 저장
@project_main_bp.route('/todo/<int:project_id>', methods=['POST'])
def create_todo(project_id):
    user_id = current_user.id
    todo_content = request.json.get('todo_content')
    write_todo(user_id, project_id, todo_content, False)
    return jsonify({"message": "success"})

# 투두리스트 조회
@project_main_bp.route('/get_todo/<int:project_id>', methods=['GET'])
def get_todos(project_id):
    todos = show_todos(project_id, current_user.id)
    return todos

# 투두리스트 수정
@project_main_bp.route('/update_todo/<int:todo_id>', methods=['POST'])
def update_todo(todo_id):
    todo_content = request.json.get('todo_content')
    todo = update_todos(todo_id, todo_content)
    return todo

# 투두리스트 삭제
@project_main_bp.route('/delete_todo/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    delete_todos(todo_id)
    return jsonify({"message": "success"})

# 투두리스트 상태 변경
@project_main_bp.route('/change_status/<int:todo_id>', methods=['POST'])
def change_status(todo_id):
    todo = change_todo_status(todo_id)
    return jsonify(todo)

# 2주 캘린더
@project_main_bp.route('/calendar/<int:project_id>',methods=['GET'])
def get_schedule(project_id):
    user_id = current_user.id
    schedule = show_schedules(project_id, user_id)
    return schedule