# controllers/sprint_controller.py
from datetime import datetime
from models.sprint_model import Sprint, SprintBacklog
from models.productbacklog_model import ProductBacklog
from models.project_model import UserProject

from database import db 
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

# 프로젝트 id로 프로덕트 백로그를 모두 불러옴
def get_all_product_backlogs(project_id):
    try:
        return ProductBacklog.query.filter_by(project_id=project_id).all()
    except SQLAlchemyError as e:
        return str(e)
    
# 스프린트 백로그에 할당되지 않은 프로덕트 백로그만 가져오는 함수
def get_unassigned_product_backlogs(project_id):
    try:
        # 스프린트에 할당되지 않은 프로덕트 백로그를 필터링
        unassigned_backlogs = ProductBacklog.query.filter_by(project_id=project_id, sprint_id=None).all()
        return unassigned_backlogs
    except SQLAlchemyError as e:
        return str(e)

# 모든 스프린트를 가져오는 로직
def get_sprint(project_id):
    try:
        sprints = Sprint.query.filter_by(project_id=project_id).order_by(Sprint.due_date).all()
        return sprints
    except SQLAlchemyError as e:
        return str(e)

# 스프린트를 생성하는 로직
# 스프린트를 생성하는 로직
def create_sprint(project_id, sprint_name, start_date, end_date, status=None):
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        if end_date <= start_date:
            return None, "Invalid dates: End date must be after start date."

        # 해당 프로젝트의 다른 스프린트와 날짜가 겹치지 않는지 확인
        overlapping_sprints = Sprint.query.filter(
            Sprint.project_id == project_id,
            Sprint.sprint_end_date >= start_date,
            Sprint.sprint_start_date <= end_date
        ).all()
        
        if overlapping_sprints:
            return None, "Date conflict: Another sprint overlaps with the given dates."

        new_sprint = Sprint(project_id=project_id, sprint_name=sprint_name, sprint_start_date=start_date, sprint_end_date=end_date, status=status)
        db.session.add(new_sprint)
        db.session.commit()
        return new_sprint, None
    except SQLAlchemyError as e:
        db.session.rollback()
        return None, str(e)

# 스프린트를 업데이트하는 메서드
def update_sprint(sprint_id, updates):
    try:
        sprint = Sprint.query.get(sprint_id)
        if sprint:
            sprint.sprint_name = updates.get('name', sprint.sprint_name)
            
            # 문자열을 datetime.date로 변환
            if 'start_date' in updates:
                sprint.sprint_start_date = datetime.strptime(updates['start_date'], "%Y-%m-%d").date()
            if 'end_date' in updates:
                sprint.sprint_end_date = datetime.strptime(updates['end_date'], "%Y-%m-%d").date()
            
            # 날짜 검증
            if not sprint.is_valid_dates():
                return None, "Invalid sprint dates: Start date must be today or later, and end date must be after start date."

            db.session.commit()
            return sprint
        return None
    except SQLAlchemyError as e:
        db.session.rollback()
        return str(e)

# 스프린트를 삭제하는 메서드
def delete_sprint(sprint_id):
    try:
        sprint = Sprint.query.get(sprint_id)
        if sprint:
            project_id = sprint.project_id
            db.session.delete(sprint)
            db.session.commit()
            return sprint
        return None
    except SQLAlchemyError as e:
        db.session.rollback()
        return None

# 스프린트를 불러오는 로직
def get_sprints_with_backlogs(project_id):
    try:
        sprints = Sprint.query.options(
            joinedload(Sprint.product_backlog)
        ).filter_by(project_id=project_id).all()

        sprint_details = []
        for sprint in sprints:
            backlog_details = []
            for backlog in sprint.product_backlog:
                # SprintBacklog와 UserProject를 조인하여 project_id와 user_id를 모두 검사
                sprint_backlogs = (
                    db.session.query(SprintBacklog, UserProject.user_name)
                    .join(UserProject, (SprintBacklog.user_id == UserProject.user_id) & (UserProject.project_id == project_id))
                    .filter(SprintBacklog.product_backlog_id == backlog.product_backlog_id)
                    .all()
                )
                
                sprint_backlog_contents = [
                    {
                        'sprint_backlog_id': sb.SprintBacklog.sprint_backlog_id,
                        'content': sb.SprintBacklog.sprint_backlog_content,
                        'user_id': sb.SprintBacklog.user_id,
                        'status': sb.SprintBacklog.status,
                        'user_name': sb.user_name  
                    }
                    for sb in sprint_backlogs
                ]
                
                backlog_details.append({
                    'product_backlog_id': backlog.product_backlog_id,
                    'content': backlog.product_backlog_content,
                    'sprint_backlogs': sprint_backlog_contents
                })

            sprint_details.append({
                'sprint_id': sprint.sprint_id,
                'sprint_name': sprint.sprint_name,
                'start_date': sprint.sprint_start_date.strftime('%Y-%m-%d'),
                'end_date': sprint.sprint_end_date.strftime('%Y-%m-%d'),
                'product_backlogs': backlog_details
            })

        return sprint_details
    except SQLAlchemyError as e:
        return str(e)

    
# 프로덕트 백로그에 스프린트 ID를 할당하는 메서드
def assign_backlogs_to_sprint(sprint_id, backlog_ids):
    try:
        for backlog_id in backlog_ids:
            backlog = ProductBacklog.query.get(backlog_id)
            if backlog:
                backlog.sprint_id = sprint_id
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        return str(e)
    
# 수정할 때 sprintBacklog의 sprint_id 재할당
def assign_backlogs_to_sprint(sprint_id, backlog_ids):
    try:
        # 기존에 해당 스프린트에 할당된 모든 백로그의 sprint_id를 제거
        ProductBacklog.query.filter_by(sprint_id=sprint_id).update({"sprint_id": None})
        db.session.commit()
        
        # 새로 선택된 백로그에 sprint_id 할당
        for backlog_id in backlog_ids:
            backlog = ProductBacklog.query.get(backlog_id)
            if backlog:
                backlog.sprint_id = sprint_id
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        return str(e)
    
    
# 모든 스프린트 백로그를 가져오는 로직
def get_sprint_backlogs(sprint_id):
    try:
        return SprintBacklog.find_all_by_sprint_id(sprint_id)
    except SQLAlchemyError as error:
        return {'error': str(error)}

# 스프린트 백로그 생성
def create_sprint_backlog(sprint_id, product_backlog_id, content, user_id):
    try:
        new_backlog = SprintBacklog(
            sprint_id=sprint_id,
            product_backlog_id=product_backlog_id,
            sprint_backlog_content=content,
            user_id=user_id,
            status='To Do'  # 기본 상태 설정
        )
        db.session.add(new_backlog)
        db.session.commit()
        return new_backlog, None  # 성공 시 에러 메시지는 None
    except SQLAlchemyError as e:
        db.session.rollback()
        return None, str(e)  # 실패 시 None과 에러 메시지 반환


# 스프린트 백로그 삭제
def delete_backlog(backlog_id):
    backlog = SprintBacklog.query.get(backlog_id)
    if backlog:
        project_id = backlog.sprint.project_id
        db.session.delete(backlog)
        db.session.commit()
        return True, "Deleted Successfully", project_id
    return False, "Backlog Not Found"

# 스프린트 백로그 업데이트
def update_backlog_details(backlog_id, content, user_id):
    backlog = SprintBacklog.query.get(backlog_id)
    if backlog:
        backlog.sprint_backlog_content = content
        backlog.user_id = user_id
        db.session.commit()
        return True, "Updated Successfully", backlog.sprint.project_id
    return False, "Backlog Not Found"

def update_backlog_status(backlog_id, status):
    try:
        backlog = SprintBacklog.query.get(backlog_id)
        if backlog:
            backlog.status = status
            db.session.commit()
            # 성공시 반환
            return True, "Status updated successfully", backlog.sprint.project_id
        else:
            # 백로그를 찾을 수 없을 때
            return False, "Backlog not found", None
    except Exception as e:
        db.session.rollback()
        # 데이터베이스 오류 발생시
        return False, str(e), None



def get_users_by_project_id(project_id):
    user_projects = UserProject.query.filter_by(project_id=project_id).all()
    users = [{'user_id': user_project.user_id, 'user_name': user_project.user_name} for user_project in user_projects]
    return users


def get_current_sprint_backlogs(user_id, project_id):
    try:
        # 현재 사용자가 참여 중인 프로젝트의 ID 확인
        user_projects = UserProject.query.filter_by(user_id=user_id, project_id=project_id).all()
        project_ids = [up.project_id for up in user_projects]

        # 오늘 날짜 기준으로 현재 스프린트 찾기
        today = datetime.today().date()
        current_sprint = Sprint.query.filter(
            Sprint.project_id.in_(project_ids),
            Sprint.sprint_start_date <= today,
            Sprint.sprint_end_date >= today,
        ).first()

        # 현재 스프린트가 있는지 확인
        if current_sprint:
            # 스프린트 ID로 전체 백로그 가져오기 (퍼센트 계산용)
            all_sprint_backlogs = SprintBacklog.query.filter_by(sprint_id=current_sprint.sprint_id).all()
            
            # 전체 백로그 개수
            total_backlogs = len(all_sprint_backlogs)
            # 'Done' 상태인 백로그 개수
            done_backlogs = sum(1 for backlog in all_sprint_backlogs if backlog.status == 'Done')

            # 퍼센트 계산 (총 백로그가 0이 아닌 경우)
            progress_percentage = (done_backlogs / total_backlogs * 100) if total_backlogs > 0 else 0

            # 현재 사용자 ID로 필터링된 스프린트 백로그 가져오기 (사용자별 콘텐츠 표시용)
            user_sprint_backlogs = SprintBacklog.query.filter_by(sprint_id=current_sprint.sprint_id, user_id=user_id).all()

            # 스프린트 백로그 정보를 반환할 데이터 구조
            backlog_details = [
                {
                    'sprint_backlog_content': backlog.sprint_backlog_content,
                    'status': backlog.status
                }
                for backlog in user_sprint_backlogs
            ]

            return {
                'sprint_id': current_sprint.sprint_id,
                'sprint_name': current_sprint.sprint_name,
                'backlogs': backlog_details,
                'progress_percentage': round(progress_percentage, 2)  # 소수점 두 자리까지 반올림
            }
        else:
            return {'message': 'No current sprint found'}

    except SQLAlchemyError as e:
        return {'error': str(e)}
