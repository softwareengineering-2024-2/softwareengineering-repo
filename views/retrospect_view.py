# retrospect_view.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.project_model import Project, UserProject
from models.sprint_model import Sprint
from models.user_model import Users
from models.retrospect_model import Retrospect
from controllers.retrospect_controller import get_sprints, create_retrospect, update_retrospect, delete_retrospect, get_retrospect_by_id, get_user_name_by_project_and_user, get_filtered_retrospects
from flask_login import current_user, login_required
from database import db

# Blueprint 객체 생성
retrospect_bp = Blueprint('retrospect', __name__)

# retrospect 관리 페이지
@retrospect_bp.route('/<int:project_id>', methods=['GET'])
@login_required
def retrospect_view(project_id):
    project = Project.query.get_or_404(project_id)
    sprints = get_sprints(project_id)

    label = request.args.get('category', 'all')
    sprint_id = request.args.get('sprint', 'all')
    page = request.args.get('page', 1, type=int)

    retrospects = get_filtered_retrospects( # 필터링
        project_id=project_id,
        category=label,
        sprint_id=sprint_id,
        page=page,
        per_page=12
    )

    user_projects = UserProject.query.filter_by(project_id=project_id).all()
    user_map = {user_project.user_id: user_project.user_name for user_project in user_projects}    

    return render_template('retrospect_back.html', project=project, project_id=project_id, sprints=sprints, retrospects=retrospects, user_map=user_map)

# 회고 생성 페이지
@retrospect_bp.route('/<int:project_id>/create', methods=['GET'])
@login_required
def get_create_retrospect_view(project_id):
    project = Project.query.get_or_404(project_id)
    sprints = get_sprints(project_id)
    return render_template('create_retrospect_back.html', project=project, sprints=sprints)

# 회고 생성
@retrospect_bp.route('/<int:project_id>/create', methods=['POST'])
@login_required
def create_retrospect_view(project_id):
    data = {
        "user_id": current_user.id,
        "project_id": project_id,
        "sprint_id": request.form.get("sprint_id"),
        "retrospect_title": request.form.get("retrospect_title"),
        "retrospect_content": request.form.get("retrospect_content"),
        "label": request.form.get("label")
    }
    if create_retrospect(data):
        flash("회고가 성공적으로 생성되었습니다.", "success")
    else:
        flash("회고 생성에 실패했습니다.", "error")
    return redirect(url_for('retrospect.retrospect_view', project_id=project_id))

# 회고 수정 페이지
@retrospect_bp.route('/<int:project_id>/edit/<int:retrospect_id>', methods=['GET'])
@login_required
def get_edit_retrospect_view(project_id, retrospect_id):
    project = Project.query.get_or_404(project_id)
    retrospect = Retrospect.query.get_or_404(retrospect_id)
    sprints = get_sprints(project_id)
    return render_template('create_retrospect_back.html', project=project, retrospect=retrospect, sprints=sprints)

# 회고 수정
@retrospect_bp.route('/<int:project_id>/edit/<int:retrospect_id>', methods=["POST"])
@login_required
def edit_retrospect_view(project_id, retrospect_id):
    data = {
        "retrospect_title": request.form.get("retrospect_title"),
        "retrospect_content": request.form.get("retrospect_content"),
        "label": request.form.get("label"),
        "sprint_id": request.form.get("sprint_id")
    }
    if update_retrospect(retrospect_id, data):
        flash("회고가 성공적으로 수정되었습니다.", "success")
    else:
        flash("회고 수정에 실패했습니다.", "error")
    return redirect(url_for('retrospect.retrospect_view', project_id=project_id))

# 회고 조회 페이지
@retrospect_bp.route('/<int:project_id>/view/<int:retrospect_id>', methods=["GET"])
@login_required
def view_retrospect_view(project_id, retrospect_id):
    retrospect = get_retrospect_by_id(retrospect_id)
    if not retrospect:
        return render_template("404.html"), 404
    
    sprints = get_sprints(project_id)

    user_name = get_user_name_by_project_and_user(project_id, retrospect.user_id)

    return render_template('view_retrospect_back.html', retrospect=retrospect, sprints=sprints, user_name=user_name)

# 회고 삭제
@retrospect_bp.route('/<int:project_id>/delete/<int:retrospect_id>', methods=["POST"])
@login_required
def delete_retrospect_view(project_id, retrospect_id):
    if delete_retrospect(retrospect_id):
        flash("회고가 성공적으로 삭제되었습니다.", "success")
    else:
        flash("회고 삭제에 실패했습니다.", "error")
    return redirect(url_for('retrospect.retrospect_view', project_id=project_id))

