from flask import Blueprint, render_template
from models.project_model import UserProject, Project
from flask_login import login_required, current_user

# Blueprint 객체 생성
guide_bp = Blueprint('guide', __name__)

# 가이드 메인 페이지 렌더링
@guide_bp.route('/<int:project_id>', methods=['GET'])
@login_required
def guide_view(project_id):
    # 목차와 콘텐츠를 렌더링
    return render_template('guide.html',project=Project.find_by_id(project_id),
                           userproject=UserProject.find_by_user_and_project(current_user.id, project_id))
