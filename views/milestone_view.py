from flask import Blueprint, render_template, request, redirect, url_for, flash
from controllers.milestone_controller import get_milestones, create_milestone, update_milestone, delete_milestone, get_milestone_counts
from controllers.calendar_controller import create_schedules
from models.project_model import UserProject, Project
from flask_login import login_required, current_user

# Blueprint 객체 생성
milestone_bp = Blueprint('milestone', __name__)

# 마일스톤 목록 조회 로직
@milestone_bp.route('/<int:project_id>', methods=['GET'])
@login_required
def milestone_view(project_id):
    userproject = UserProject.find_by_user_and_project(current_user.id, project_id)
    milestones = get_milestones(userproject.project_id)
    total_count, completed_count = get_milestone_counts(project_id)
    return render_template('milestone.html',
                           project=Project.find_by_id(project_id),
                           userproject=userproject, milestones=milestones,
                           total_count=total_count, completed_count=completed_count)

# 마일스톤 생성 로직
@milestone_bp.route('/<int:project_id>/create', methods=['POST'])
@login_required
def create_milestone_view(project_id):
    milestone_content = request.form.get('milestone_content')
    due_date = request.form.get('due_date')
    create_milestone(project_id, milestone_content, due_date)
    create_schedules(current_user.id,project_id, milestone_content, None, due_date, due_date, True, 0, None, True)

    return redirect(url_for('milestone.milestone_view', project_id=project_id))

# # 마일스톤 수정 로직
# @milestone_bp.route('/<int:project_id>/<int:milestone_id>/update', methods=['GET', 'POST'])
# @login_required
# def update_milestone_view(project_id, milestone_id):
#     project = UserProject.find_by_user_and_project(current_user.id, project_id)
#     if not project:
#         flash("프로젝트를 찾을 수 없습니다.")
#         return redirect(url_for('project_main.project_main_view', project_id=project_id))
#     if request.method == 'POST':
#         milestone_content = request.form.get('milestone_content')
#         due_date = request.form.get('due_date')
#         message = update_milestone(milestone_id, milestone_content, due_date)
#         flash(message)
#         return redirect(url_for('milestone.milestone_view', project_id=project_id))
#     return render_template('update_milestone_back.html', project=project, milestone=Milestone.find_by_id(milestone_id))

# 마일스톤 삭제 로직
@milestone_bp.route('/<int:project_id>/<int:milestone_id>/delete', methods=['POST'])
@login_required
def delete_milestone_view(project_id, milestone_id):
    userproject = UserProject.find_by_user_and_project(current_user.id, project_id)
    if not userproject:
        flash("프로젝트를 찾을 수 없습니다.")
        return redirect(url_for('project_main.project_main_view', project_id=project_id))
    message = delete_milestone(milestone_id)
    flash(message)
    return redirect(url_for('milestone.milestone_view', project_id=project_id))
