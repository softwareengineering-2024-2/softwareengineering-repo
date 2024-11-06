from flask import flash, redirect, render_template, request, session, url_for
from models.not_list_model import NotList
from models.project_model import UserProject

# not list 보여주기
def show_notlist(project_id):
    if not project_id:
        return "Project ID is missing", 400
    not_list_keywords = NotList.query.filter_by(project_id=project_id).all()
    return not_list_keywords

# not list 키워드 추가
def create_keywords(keyword, project_id):
    if not project_id:
        return "Project ID is missing", 400
    
    # not list 키워드 추가하기
    new_keyword = NotList(project_id=project_id, keyword=keyword)
    new_keyword.save_to_db()

    return new_keyword

# not list 삭제
def delete_keyword(not_list_id,project_id, user_id):
    user_role = UserProject.query.filter_by(project_id=project_id, user_id=user_id).first_or_404().user_role
    if user_role == 'PM':
        not_list_item = NotList.query.filter_by(not_list_id=not_list_id).first()
        not_list_item.delete_from_db()
    else:
        return "Not list 키워드는 PM만 삭제할 수 있습니다."
    
    return not_list_item

#사용자 역할 가져오기
def get_user_role(project_id, user_id):
    user_project = UserProject.query.filter_by(project_id=project_id, user_id=user_id).first()
    if user_project:
        return user_project.user_role
    return None