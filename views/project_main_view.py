from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.project_model import Project

# 블루프린트 생성
project_main_bp = Blueprint('project_main', __name__)

@project_main_bp.route('/<int:project_id>')
@login_required
def project_main_view(project_id):
    userproject=Project.find_by_id(project_id)
    return render_template('project_main.html', userproject=userproject)
        