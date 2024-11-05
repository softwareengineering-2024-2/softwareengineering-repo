from flask import Blueprint, render_template, request, jsonify, redirect, url_for,flash
from controllers.userstory_controller import show_stories, create_story, update_story, delete_story
from controllers.notlist_controller import show_notlist
userstory_bp = Blueprint('userstory_view', __name__)

# 유저스토리 목록 보기
@userstory_bp.route('/<int:project_id>', methods=['GET'])
def view_stories_route(project_id):
    result = show_stories(project_id)
    not_list = show_notlist(project_id)
    if isinstance(result, tuple):
        return result
    return render_template('userstory_back.html', stories=result, project_id=project_id, not_list=not_list)

# 유저스토리 작성
@userstory_bp.route('/userstory/<int:project_id>', methods=['POST'])
def create_story_route(project_id):
    content = request.form.get('content')
    result = create_story(content, project_id)
    if isinstance(result, tuple):
        return jsonify({"error": result[0]}), result[1]
    return redirect(url_for('userstory_view.view_stories_route', project_id=project_id))

# 유저스토리 수정
@userstory_bp.route('/userstory/<int:project_id>/<int:story_id>', methods=['POST'])
def update_story_route(project_id, story_id):
    content = request.form.get('content')
    result = update_story(story_id, content, project_id)
    if isinstance(result, tuple):
        return jsonify({"error": result[0]}), result[1]
    return redirect(url_for('userstory_view.view_stories_route', project_id=project_id))

# 유저스토리 삭제
@userstory_bp.route('/userstory/<int:project_id>/<int:story_id>', methods=['POST'])
def delete_story_route(project_id, story_id):
    
    result=delete_story(story_id)
    flash(result)
    return redirect(url_for('userstory_view.view_stories_route', project_id=project_id))