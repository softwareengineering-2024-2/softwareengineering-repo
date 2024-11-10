from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session
from controllers.userstory_controller import show_stories, create_story, update_story, delete_story, check_keyword
from controllers.notlist_controller import show_notlist

userstory_bp = Blueprint('userstory', __name__)

# 유저스토리 목록 보기
@userstory_bp.route('/<int:project_id>', methods=['GET'])
def view_stories_route(project_id):
    result = show_stories(project_id)
    not_list = show_notlist(project_id)
    if isinstance(result, tuple):
        return result
   
    return render_template('userstory.html', project_id=project_id, stories=result, not_list=not_list)

# 유저스토리 작성
@userstory_bp.route('/userstory/<int:project_id>', methods=['POST'])
def create_story_route(project_id):
    content = request.form.get('content')
    result = create_story(content, project_id)
    
    if result == "키워드 감지":
        session['pending_user_story'] = {
            'content': content,
            'project_id': project_id,
            'story_id': None  # 새 유저스토리이므로 story_id는 None
        }
        return render_template('keyword_check_back.html', project_id=project_id, user_story_content=content)
    
    return redirect(url_for('userstory.view_stories_route', project_id=project_id))

# 유저스토리 수정
@userstory_bp.route('/userstory/<int:project_id>/<int:story_id>', methods=['POST'])
def update_story_route(project_id, story_id):
    content = request.form.get('content')
    result = update_story(story_id, content, project_id)
   
    if result == "키워드 감지":
        session['pending_user_story'] = {
            'content': content,
            'project_id': project_id,
            'story_id': story_id
        }
        return render_template('keyword_check_back.html', project_id=project_id, story_id=story_id, user_story_content=content)
   
    return redirect(url_for('userstory.view_stories_route', project_id=project_id))

# 유저스토리 삭제
@userstory_bp.route('/userstory/<int:project_id>/<int:story_id>/delete', methods=['POST'])
def delete_story_route(project_id, story_id):
    delete_story(story_id)
    return redirect(url_for('userstory.view_stories_route', project_id=project_id))

# 유저스토리 키워드 검사
@userstory_bp.route('/userstory/check/<int:project_id>', methods=['POST'])
def check_keyword_route(project_id):
    check_or_not = request.form.get('check_or_not')
    pending_user_story = session.get('pending_user_story')
    if not pending_user_story:
        flash("세션에 유저스토리 데이터가 없습니다.", "error")
        return redirect(url_for('userstory.view_stories_route', project_id=project_id))
    
    user_story_content = pending_user_story['content']
    story_id = pending_user_story['story_id']
    result = check_keyword(check_or_not, user_story_content, project_id, story_id)
    
    if result == "check":
        flash("유저스토리가 성공적으로 저장되었습니다.", "success")
    elif result == "not":
        flash("유저스토리 저장이 취소되었습니다.", "info")
    
    session.pop('pending_user_story', None)  # 세션에서 데이터 제거
    return redirect(url_for('userstory.view_stories_route', project_id=project_id))

