from models.project_model import Project, UserProject
from models.burnup_model import BacklogChanges
from uuid import uuid4
from flask_login import current_user
from datetime import datetime

# 새로운 프로젝트를 생성하고 저장하는 로직
def create_project(project_name):
    unique_link = str(uuid4()) # 프로젝트 고유 링크 생성
    new_project = Project(project_name=project_name, project_link=unique_link)
    new_project.save_to_db()
    
    # 새로운 프로젝트 UserProject 테이블에 저장
    new_user_project = UserProject(user_id=current_user.id, project_id=new_project.project_id, user_name=current_user.name, user_role="Member")
    new_user_project.save_to_db()

    # 새로운 프로젝트의 초기 번업 차트 데이터 저장
    new_change = BacklogChanges(project_id=new_project.project_id, changed_date=datetime.now().date(), total_backlog=0, completed_backlog=0)
    new_change.save_to_db()

    return new_project

# 사용자를 프로젝트에 추가하는 로직
def join_project(project_id):
    project = Project.find_by_id(project_id)
    if project:
        user_project = UserProject(user_id=current_user.id, project_id=project_id, user_name=current_user.name, user_role="Member")
        user_project.save_to_db()
        return f"프로젝트 {project.project_name}에 성공적으로 참여했습니다."
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
            return f"프로젝트 {project.project_name}에서 성공적으로 나갔습니다."
        else:
            return "프로젝트에 소속되지 않았습니다."
    return "프로젝트가 존재하지 않습니다."

# 사용자의 프로필 정보를 설정하는 로직
def set_profile(project_id, user_name, user_role):
    userproject = UserProject.find_by_user_and_project(current_user.id, project_id)
    if userproject:
        userproject.set_user_profile(current_user.id, project_id, user_name=user_name, user_role=user_role)
        return f"프로필이 설정되었습니다."