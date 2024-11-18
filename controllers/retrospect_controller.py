# retrospect_controller.py

from models.retrospect_model import Retrospect
from models.user_model import Users
from models.project_model import Project, UserProject
from models.sprint_model import Sprint
from database import db

# 특정 프로젝트의 스프린트 목록을 가져오는 함수
def get_sprints(project_id):
    try:
        sprints = Sprint.query.filter_by(project_id=project_id).order_by(Sprint.sprint_id).all()
        return sprints if sprints else []
    except Exception:
        return None

# 회고를 생성하고 저장하는 함수
def create_retrospect(data):
    retrospect = Retrospect(
        user_id=data.get('user_id'),
        project_id=data.get('project_id'),
        sprint_id=data.get('sprint_id'),
        retrospect_title=data.get('retrospect_title'),
        retrospect_content=data.get('retrospect_content'),
        label=data.get('label')
    )
    db.session.add(retrospect)
    db.session.commit()
    return True

# 회고를 수정하는 함수
def update_retrospect(retrospect_id, data):
    retrospect = Retrospect.query.get(retrospect_id)
    if not retrospect:
        return False
    retrospect.retrospect_title = data.get("retrospect_title", retrospect.retrospect_title)
    retrospect.retrospect_content = data.get("retrospect_content", retrospect.retrospect_content)
    retrospect.label = data.get("label", retrospect.label)
    db.session.commit()
    return True

# 회고를 조회하는 함수
def get_retrospect_by_id(retrospect_id):
    retrospect = Retrospect.query.get(retrospect_id)
    if not retrospect:
        return None
    return retrospect

# 특정 프로젝트의 사용자 이름을 가져오는 함수
def get_user_name_by_project_and_user(project_id, user_id):
    user_project = UserProject.query.filter_by(project_id=project_id, user_id=user_id).first()
    if not user_project:
        return "Unknown User"
    return user_project.user_name

# 회고를 삭제하는 함수
def delete_retrospect(retrospect_id):
    retrospect = Retrospect.query.get(retrospect_id)
    if not retrospect:
        return False
    db.session.delete(retrospect)
    db.session.commit()
    return True