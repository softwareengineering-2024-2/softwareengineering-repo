from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.project_model import UserProject, Project

# 블루프린트 생성
project_main_bp = Blueprint('project_main', __name__)

@project_main_bp.route('/<int:project_id>')
@login_required
def project_main_view(project_id):
    userproject=UserProject.find_by_user_and_project(current_user.id, project_id)
    project_name = Project.find_by_id(project_id).project_name
    return render_template('project_main_back.html', userproject=userproject, project_name=project_name)