from flask import flash, jsonify
from models.alert_model import Alert
from models.project_model import Project, UserProject
from flask_login import current_user

# 프로젝트 이름 조회하기
def get_project_name(project_id):
    project = Project.query.filter_by(project_id=project_id).first()
    project_name = project.project_name
    return project_name

# 알림 저장하기
def save_alert(user_id,project_id, alert_content, status):
    alert = Alert(user_id=user_id,project_id=project_id, alert_content=alert_content, status=status)
    alert.save_to_db()

# 알림 조회하기
def get_alerts(project_id):
    user_id = current_user.id
    user_role = UserProject.query.filter_by(user_id=user_id, project_id=project_id).first().user_role

    if user_role  == 'PM(기획자)':
        alerts = Alert.query.filter_by(project_id=project_id).order_by(Alert.alert_id.desc()).all()
        return [{
        'content': alert.alert_content
    } for alert in alerts]
    
