from flask import flash, redirect, render_template, request, session, url_for
from models.userstory_model import UserStory
from controllers.notlist_controller import show_notlist
from database import db

# 유저스토리 보여주기
def show_stories(project_id):
    if not project_id:
        return "Project ID is missing", 400
    
    stories = UserStory.query.filter_by(project_id=project_id).all()
    return stories

# 유저스토리 작성
def create_story(user_story_content, project_id):
    if not project_id:
        return "Project ID is missing", 400
    
    # 세션에서 키워드 체크 플래그 가져오기
    keyword_checked = session.get('keyword_checked', False)
    
    # not list 키워드 가져오기
    not_list_keywords = show_notlist(project_id)
    
    # not list 키워드가 포함되어 있는지 확인
    if not keyword_checked:
        for keyword in not_list_keywords:
            if keyword.keyword in user_story_content:
                flash("유저 스토리에 'not list' 키워드가 포함되어 있습니다. 다시 입력해 주세요.", "warning")
                session['keyword_checked'] = True
                return user_story_content

    new_userstory = UserStory(project_id=project_id, user_story_content=user_story_content)
    new_userstory.save_to_db()
    
    session.pop('keyword_checked', None)  # 플래그 초기화
    return new_userstory


# 유저스토리 수정
def update_story(story_id, user_story_content, project_id):
    story = UserStory.query.get_or_404(story_id)
    
    # 세션에서 키워드 체크 플래그 가져오기
    keyword_checked = session.get('keyword_checked', False)
    
    # not list 키워드 가져오기
    not_list_keywords = show_notlist(project_id)
    
    # not list 키워드가 포함되어 있는지 확인
    if user_story_content is not None and not keyword_checked:
        for keyword in not_list_keywords:
            if keyword.keyword in user_story_content:
                flash("유저 스토리에 'not list' 키워드가 포함되어 있습니다. 다시 입력해 주세요.")
                session['keyword_checked'] = True
                return None
    
    story.update_in_db(user_story_content=user_story_content)
    session.pop('keyword_checked', None)  # 플래그 초기화
    return story

# 유저스토리 삭제
def delete_story(story_id):
    story = UserStory.query.filter_by(story_id=story_id).first_or_404()
    if story:
        story.delete_from_db()
        return "유저스토리가 삭제 되었습니다"
    return "유저스토리가 존재하지 않습니다", 400