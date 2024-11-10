from flask import Blueprint, render_template
from flask_login import login_required, current_user
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

    return render_template(
        'main.html',
        userproject=userproject,
        project=project,
        progress_percentage=progress_percentage,
        current_sprint_backlogs=current_sprint_backlogs 
    )