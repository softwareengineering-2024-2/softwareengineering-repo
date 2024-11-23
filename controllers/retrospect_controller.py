# retrospect_controller.py

from models.retrospect_model import Retrospect
from models.project_model import UserProject
from models.sprint_model import Sprint
from database import db
from drive.drive_init import upload_to_drive

# 특정 프로젝트의 스프린트 목록을 가져오는 함수
def get_sprints(project_id):
    sprints = Sprint.query.filter_by(project_id=project_id).order_by(Sprint.sprint_id).all()
    return sprints if sprints else []

# 회고를 생성하고 저장하는 함수
def create_retrospect(data):
    retrospect = Retrospect(
        user_id=data.get('user_id'),
        project_id=data.get('project_id'),
        sprint_id=data.get('sprint_id'),
        retrospect_title=data.get('retrospect_title'),
        retrospect_content=data.get('retrospect_content'),
        label=data.get('label'),
        file_link=data.get('file_link'),
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
    retrospect.file_link = data.get("file_link", retrospect.file_link)
    retrospect.sprint_id = data.get("sprint_id", retrospect.sprint_id)
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

# 회고를 필터링하는 함수
def get_filtered_retrospects(project_id, category=None, sprint_id=None, page=1, per_page=12):
    query = Retrospect.query.filter_by(project_id=project_id)
    if category and category != 'all':
        query = query.filter_by(label=category)
    if sprint_id and sprint_id != 'all':
        query = query.filter_by(sprint_id=sprint_id)
    return query.order_by(Retrospect.retrospect_id.desc()).paginate(page=page, per_page=per_page, error_out=False)

# 파일 업로드하고 링크 반환하는 함수
def handle_file_upload(file):
    if file and file.filename != '':
        folder_id = "1FcmKeVM8SaYPcJ8CUfOt6iBkB6tseANk"
        upload_result = upload_to_drive(file, file.filename, folder_id)
        return upload_result.get('webViewLink')
    return None