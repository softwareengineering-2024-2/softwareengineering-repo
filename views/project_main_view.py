from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.project_model import UserProject, Project

# 블루프린트 생성
project_main_bp = Blueprint('project_main', __name__)

@project_main_bp.route('/<int:project_id>')
@login_required
def project_main_view(project_id):
    userproject=UserProject.find_by_user_and_project(current_user.id, project_id)
    project = Project.find_by_id(project_id)
    return render_template('main.html', userproject=userproject, project=project, progress_percentage=35)