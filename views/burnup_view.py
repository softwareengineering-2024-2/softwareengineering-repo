from flask import Blueprint, render_template
from flask_login import login_required
from controllers.burnup_controller import get_burnup_data
from models.project_model import UserProject, Project
from flask_login import login_required, current_user

# Blueprint 객체 생성
burnup_bp = Blueprint('burnup', __name__)

# 번업 차트 페이지 렌더링 로직
@burnup_bp.route('/<int:project_id>', methods=['GET'])
@login_required
def burnup_view(project_id):
    dates, totals, completeds = get_burnup_data(project_id)
    return render_template('burnup.html',
                           project=Project.find_by_id(project_id),
                           userproject=UserProject.find_by_user_and_project(current_user.id, project_id),
                           dates=dates, totals=totals, completeds=completeds)
