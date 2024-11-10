from models.project_model import Project, UserProject
from flask_login import current_user
from flask import Blueprint, render_template, request, redirect, url_for, flash, session,jsonify
from controllers.userstory_controller import show_stories, create_story, update_story, delete_story
from controllers.notlist_controller import create_keywords, delete_keyword, show_notlist 

userstory_bp = Blueprint('userstory', __name__)

# 유저스토리 목록 보기
@userstory_bp.route('/<int:project_id>', methods=['GET'])
def view_stories_route(project_id):
    stories = show_stories(project_id)
    not_list = show_notlist(project_id)
    if isinstance(stories, tuple):
        return stories
    
    if isinstance(not_list, tuple):
        return not_list
   
    keyword_list = [keyword.keyword for keyword in not_list]

    return render_template('userstory.html', project=Project.find_by_id(project_id), userproject=UserProject.find_by_user_and_project(current_user.id, project_id), stories=stories, not_list=not_list,keyword_list=keyword_list)

# 유저스토리 작성
@userstory_bp.route('/userstory/<int:project_id>', methods=['POST'])
def create_story_route(project_id):
    content = request.form.get('content')
    create_story(content, project_id)
    
    return redirect(url_for('userstory.view_stories_route', project_id=project_id))

# 유저스토리 수정
@userstory_bp.route('/userstory/<int:project_id>/<int:story_id>', methods=['POST'])
def update_story_route(project_id, story_id):
    content = request.form.get('content')
    update_story(story_id, content)

    return redirect(url_for('userstory.view_stories_route', project_id=project_id))

# 유저스토리 삭제
@userstory_bp.route('/userstory/<int:project_id>/<int:story_id>/delete', methods=['POST'])
def delete_story_route(project_id, story_id):
    error_message = delete_story(story_id)
    if error_message:
        flash(error_message, "error")
    else:
        flash("유저스토리가 성공적으로 삭제되었습니다.", "success")
    return redirect(url_for('userstory.view_stories_route', project_id=project_id))


# 키워드 추가 라우트
@userstory_bp.route('/notlist/<int:project_id>', methods=['POST'])
def create_keywords_route(project_id):
    keyword = request.form.get('keyword')  # form 데이터로부터 키워드 받기
    
    if not keyword:
        return jsonify({"error": "Keyword missing"}), 400
    
    # 키워드 저장 함수 호출 (데이터베이스에 저장)
    result = create_keywords(keyword, project_id)

    if isinstance(result, tuple):
        return jsonify({"error": result[0]}), result[1]

    # 저장된 키워드를 반환 (클라이언트에 보여줄 데이터)
    return redirect(url_for('userstory.view_stories_route', project_id=project_id))

# 키워드 삭제 라우트
@userstory_bp.route('/notlist/<int:project_id>/<int:not_list_id>/delete', methods=['POST'])
def delete_keyword_route(project_id, not_list_id):
    delete_keyword(not_list_id)      
    return redirect(url_for('userstory.view_stories_route', project_id=project_id))
