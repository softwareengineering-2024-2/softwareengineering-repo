from models.project_model import Project, UserProject
from models.user_model import Users
from uuid import uuid4
from flask import session
from flask_login import current_user

# 새로운 프로젝트를 생성하고 저장하는 로직
def create_project(project_name):
    # 새로운 프로젝트 Project 테이블에 저장
    unique_link = str(uuid4()) # 프로젝트 고유 링크 생성
    new_project = Project(project_name=project_name, project_link=unique_link)
    new_project.save_to_db()
    
    # 새로운 프로젝트 UserProject 테이블에 저장
    #access_token = session.get("token")
    new_user_project = UserProject(user_id=current_user.id, project_id=new_project.project_id, user_name="admin", user_role="admin")
    new_user_project.save_to_db()

    return f"Project '{new_project.project_name}' created successfully with ID {new_project.project_id}!"

# 프로젝트 링크를 통해 사용자를 프로젝트에 추가하는 로직
def join_project_by_link(project_link, user_id, user_name, user_role):
    project = Project.find_by_link(project_link)  # find_by_link() 아직 구현 안함
    if project:
        user_project = UserProject(user_id=user_id, project_id=project.project_id, user_name=user_name, user_role=user_role)
        user_project.save_to_db()
        return f"프로젝트 '{project.project_name}'에 성공적으로 참여했습니다."
    else:
        return "유효하지 않은 프로젝트 링크입니다."

# 사용자의 모든 프로젝트를 가져오는 로직
def get_user_projects():
    return UserProject.get_projects_by_user_id(current_user.id)

# 특정 ID의 프로젝트를 UserProject 테이블에서 삭제하는 로직
def delete_project(project_id):
    project = Project.find_by_id(project_id)
    if project:
        user_project = UserProject.find_by_project(project_id)
        if user_project:
            user_project.delete_from_db()
            return f"프로젝트 '{project.project_name}'에서 성공적으로 나갔습니다."
        else:
            return "프로젝트에 소속되지 않았습니다."
    return "프로젝트가 존재하지 않습니다."
