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
    
    # not list 키워드 가져오기
    not_list_keywords = show_notlist(project_id)
    
    # not list 키워드가 포함되어 있는지 확인
    for keyword in not_list_keywords:
        if keyword.keyword in user_story_content:
            return "키워드 감지"

    new_userstory = UserStory(project_id=project_id, user_story_content=user_story_content)
    new_userstory.save_to_db()
    
    session.pop('keyword_checked', None)  # 플래그 초기화
    return new_userstory

#유저스토리 키워드 검사
def check_keyword(check_or_not, user_story_content, project_id=None, story_id=None):
    if not story_id:
        if check_or_not == 'check':
            new_userstory = UserStory(project_id=project_id, user_story_content=user_story_content)
            new_userstory.save_to_db()
            return new_userstory
        else:
            new_userstory = None
            return user_story_content
        
    else:
        if check_or_not == 'check':
            story = UserStory.query.get_or_404(story_id)
            story.update_in_db(user_story_content=user_story_content)
            return story
        else:
            story = None
            return user_story_content  
        
   

# 유저스토리 수정
def update_story(story_id, user_story_content, project_id):
    story = UserStory.query.get_or_404(story_id)
    
     # not list 키워드 가져오기
    not_list_keywords = show_notlist(project_id)
    
    # not list 키워드가 포함되어 있는지 확인
    for keyword in not_list_keywords:
        if keyword.keyword in user_story_content:
            return "키워드 감지"
    
    story.update_in_db(user_story_content=user_story_content)
    session.pop('keyword_checked', None)  # 플래그 초기화
    return story

# 유저스토리 삭제
def delete_story(story_id):
    story = UserStory.query.filter_by(story_id=story_id).first_or_404()
    if story:
        story.delete_from_db()
    return None