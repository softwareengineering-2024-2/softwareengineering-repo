# controllers/sprint_controller.py
from datetime import date, datetime
from models.sprint_model import Sprint, SprintBacklog
from models.productbacklog_model import ProductBacklog
from models.project_model import UserProject

from database import db 
from sqlalchemy.orm import joinedload
from controllers.burnup_controller import decrement_total_and_completed_backlog

# 프로젝트 id로 프로덕트 백로그를 모두 불러옴
def get_all_product_backlogs(project_id):
    return ProductBacklog.query.filter_by(project_id=project_id).all()

    
# 스프린트 백로그에 할당되지 않은 프로덕트 백로그만 가져오는 함수
def get_unassigned_product_backlogs(project_id):
    unassigned_backlogs = ProductBacklog.query.filter_by(project_id=project_id, sprint_id=None).all()
    return [backlog.to_dict() for backlog in unassigned_backlogs]

# 모든 스프린트를 가져오는 로직
def get_sprint(project_id):
    sprints = Sprint.query.filter_by(project_id=project_id).order_by(Sprint.due_date).all()
    return sprints

# 스프린트를 생성하는 로직
# 스프린트를 생성하는 로직
def create_sprint(project_id, sprint_name, start_date, end_date, status=None):
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

# 스프린트를 업데이트하는 메서드
def update_sprint(sprint_id, updates):
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

# 스프린트를 삭제하는 메서드
def delete_sprint(sprint_id):
    try:
        sprint = Sprint.query.get(sprint_id)
        deleted_sprint_backlogs = SprintBacklog.find_all_by_sprint_id(sprint_id) 
        if sprint:
            project_id = sprint.project_id
            db.session.delete(sprint)
            db.session.commit()
            
            # 관련된 SprintBacklog 수 계산
            total_count = 0 # 삭제할 총 백로그 수
            done_count = 0  # 삭제할 'Done' 상태의 백로그 수
            for sb in deleted_sprint_backlogs:
                total_count += 1
                if sb.status == 'Done':
                    done_count += 1
            
            # 삭제된 스프린트 백로그 수만큼 총 백로그 수와 완료된 백로그 수 감소
            decrement_total_and_completed_backlog(project_id, total_count, done_count)
            
            return sprint
        return None
    except SQLAlchemyError as e:
        db.session.rollback()
        return None

# 특정 스프린트의 백로그를 불러오는 함수
def get_sprints_with_backlogs(project_id, sprint_id=None):
    try:
        query = Sprint.query.options(
            joinedload(Sprint.product_backlog)
        ).filter_by(project_id=project_id)
        
        if sprint_id:
            query = query.filter(Sprint.sprint_id == sprint_id)

        sprints = query.all()
        sprint_details = []

        for sprint in sprints:
            is_past_due = date.today() > sprint.sprint_end_date
            backlog_details = []
            for backlog in sprint.product_backlog:
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
            'status': sprint.status,
            'product_backlogs': backlog_details,
            'is_past_due': is_past_due,
        })

    return sprint_details

    
# 프로덕트 백로그에 스프린트 ID를 할당하는 메서드
def assign_backlogs_to_sprint(sprint_id, new_backlog_ids):
    try:
        # 새로운 백로그 ID를 세트로 변환
        new_backlog_ids = set(map(int, new_backlog_ids))
        
        # 현재 스프린트에 할당된 백로그 ID를 가져옴
        current_backlogs = ProductBacklog.query.filter_by(sprint_id=sprint_id).all()
        current_backlog_ids = set(backlog.product_backlog_id for backlog in current_backlogs)
        
        # 제거해야 할 백로그 (현재 할당되었지만 선택되지 않은 백로그)
        backlogs_to_unassign = current_backlog_ids - new_backlog_ids
        
        # 새로 할당해야 할 백로그 (이전에 할당되지 않았지만 새로 선택된 백로그)
        backlogs_to_assign = new_backlog_ids - current_backlog_ids
        
        # 백로그 할당 해제 및 관련 SprintBacklog 삭제
        for backlog_id in backlogs_to_unassign:
            backlog = ProductBacklog.query.get(backlog_id)
            if backlog:
                backlog.sprint_id = None
                # 관련된 SprintBacklog 삭제
                sprint_backlogs = SprintBacklog.query.filter_by(product_backlog_id=backlog_id).all()
                total_count = 0 # 삭제할 총 백로그 수
                done_count = 0  # 삭제할 'Done' 상태의 백로그 수
                for sb in sprint_backlogs:
                    total_count += 1
                    if sb.status == 'Done':
                        done_count += 1
                    db.session.delete(sb)
                
                # 삭제된 백로그 수만큼 총 백로그 수와 완료된 백로그 수 감소
                decrement_total_and_completed_backlog(Sprint.find_by_id(sprint_id).project_id, total_count, done_count)
        
        # 백로그에 스프린트 ID 할당
        for backlog_id in backlogs_to_assign:
            backlog = ProductBacklog.query.get(backlog_id)
            if backlog:
                backlog.sprint_id = sprint_id
                # 필요한 경우 새로운 SprintBacklog 생성 로직 추가
                
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        return False, str(e)
    

# 모든 스프린트 백로그를 가져오는 로직
def get_sprint_backlogs(sprint_id):
    return SprintBacklog.find_all_by_sprint_id(sprint_id)

# 스프린트 백로그 생성
def create_sprint_backlog(sprint_id, product_backlog_id, content, user_id):
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
    backlog = SprintBacklog.query.get(backlog_id)
    if backlog:
        backlog.status = status
        db.session.commit()

        # 해당 스프린트의 모든 백로그가 Done인지 확인
        sprint_id = backlog.sprint_id
        all_backlogs = SprintBacklog.query.filter_by(sprint_id=sprint_id).all()
        if all(b.status == 'Done' for b in all_backlogs):
            # 스프린트의 status를 Done으로 업데이트
            sprint = Sprint.query.get(sprint_id)
            if sprint:
                sprint.status = 'Done'
                db.session.commit()
        else:
            # 하나라도 Done이 아니면 스프린트의 status를 In Progress로 설정
            sprint = Sprint.query.get(sprint_id)
            if sprint and sprint.status != 'In Progress':
                sprint.status = 'In Progress'
                db.session.commit()

        return True, "Status updated successfully", backlog.sprint.project_id
    else:
        return False, "Backlog not found", None


def get_users_by_project_id(project_id):
    user_projects = UserProject.query.filter_by(project_id=project_id).all()
    users = [{'user_id': user_project.user_id, 'user_name': user_project.user_name} for user_project in user_projects]
    return users


# def get_current_sprint_backlogs(user_id, project_id):
#     try:
#         # 현재 사용자가 참여 중인 프로젝트의 ID 확인
#         user_projects = UserProject.query.filter_by(user_id=user_id, project_id=project_id).all()
#         project_ids = [up.project_id for up in user_projects]

#         # 오늘 날짜 기준으로 현재 스프린트 찾기
#         today = datetime.today().date()
#         current_sprint = Sprint.query.filter(
#             Sprint.project_id.in_(project_ids),
#             Sprint.sprint_start_date <= today,
#             Sprint.sprint_end_date >= today,
#         ).first()

#         # 현재 스프린트가 있는지 확인
#         if current_sprint:
#             # 스프린트 ID로 전체 백로그 가져오기 (퍼센트 계산용)
#             all_sprint_backlogs = SprintBacklog.query.filter_by(sprint_id=current_sprint.sprint_id).all()
            
#             # 전체 백로그 개수
#             total_backlogs = len(all_sprint_backlogs)
#             # 'Done' 상태인 백로그 개수
#             done_backlogs = sum(1 for backlog in all_sprint_backlogs if backlog.status == 'Done')

#             # 퍼센트 계산 (총 백로그가 0이 아닌 경우)
#             progress_percentage = (done_backlogs / total_backlogs * 100) if total_backlogs > 0 else 0

#             # 현재 사용자 ID로 필터링된 스프린트 백로그 가져오기 (사용자별 콘텐츠 표시용)
#             user_sprint_backlogs = SprintBacklog.query.filter_by(sprint_id=current_sprint.sprint_id, user_id=user_id).all()

#             # 스프린트 백로그 정보를 반환할 데이터 구조
#             backlog_details = [
#                 {
#                     'sprint_backlog_content': backlog.sprint_backlog_content,
#                     'status': backlog.status
#                 }
#                 for backlog in user_sprint_backlogs
#             ]

#             return {
#                 'sprint_id': current_sprint.sprint_id,
#                 'sprint_name': current_sprint.sprint_name,
#                 'backlogs': backlog_details,
#                 'progress_percentage': round(progress_percentage, 2)  # 소수점 두 자리까지 반올림
#             }
#         else:
#             return {'message': 'No current sprint found'}

#     except SQLAlchemyError as e:
#         return {'error': str(e)}
def get_current_sprint_backlogs(user_id, project_id):
    try:
        # 사용자가 참여 중인 프로젝트의 ID 확인
        user_projects = UserProject.query.filter_by(user_id=user_id, project_id=project_id).all()
        project_ids = [up.project_id for up in user_projects]

        # 프로젝트 ID로 모든 스프린트 가져오기
        all_sprints = Sprint.query.filter(Sprint.project_id.in_(project_ids)).all()
        if not all_sprints:
            return {'message': 'No sprints found for the project'}

        sprint_backlog_details = []
        total_backlogs = 0
        total_done_backlogs = 0

        for sprint in all_sprints:
            print(f"Processing Sprint ID: {sprint.sprint_id}")  # 스프린트 ID 출력

            # 각 스프린트의 백로그 가져오기
            sprint_backlogs = SprintBacklog.query.filter_by(sprint_id=sprint.sprint_id).all()

            # 디버깅: 각 백로그 ID와 상태 출력
            for backlog in sprint_backlogs:
                print(f"Sprint ID: {sprint.sprint_id}, Backlog ID: {backlog.sprint_backlog_id}, Status: {backlog.status}")

            # 스프린트 백로그 개수와 완료된 백로그 개수 계산
            sprint_total = len(sprint_backlogs)
            sprint_done = sum(1 for backlog in sprint_backlogs if backlog.status.lower() == 'done')  # 대소문자 처리 추가

            # 디버깅: 스프린트별 개수 출력
            print(f"Sprint ID: {sprint.sprint_id}, Total Backlogs: {sprint_total}, Done Backlogs: {sprint_done}")

            # 전체 백로그에 합산
            total_backlogs += sprint_total
            total_done_backlogs += sprint_done

            # 스프린트 별 백로그 정보 저장
            sprint_backlog_details.append({
                'sprint_id': sprint.sprint_id,
                'sprint_name': sprint.sprint_name,
                'start_date': sprint.sprint_start_date.strftime('%Y-%m-%d'),
                'end_date': sprint.sprint_end_date.strftime('%Y-%m-%d'),
                'backlogs': [
                    {
                        'sprint_backlog_content': backlog.sprint_backlog_content,
                        'status': backlog.status
                    }
                    for backlog in sprint_backlogs
                ],
                'progress_percentage': (sprint_done / sprint_total * 100) if sprint_total > 0 else 0
            })

        # 전체 진행률 계산
        overall_progress_percentage = (total_done_backlogs / total_backlogs * 100) if total_backlogs > 0 else 0

        # 디버깅: 전체 진행률 출력
        print(f"Total Backlogs: {total_backlogs}, Total Done: {total_done_backlogs}, Overall Progress: {overall_progress_percentage:.2f}%")

        return {
            'project_id': project_id,
            'overall_progress_percentage': round(overall_progress_percentage, 2),  # 전체 진행률
            'sprints': sprint_backlog_details
        }

    except SQLAlchemyError as e:
        print(f"Error: {str(e)}")  # 예외 메시지 출력
        return {'error': str(e)}

def move_incomplete_backlogs_to_next_sprint(sprint_id, project_id):
    # 현재 스프린트 가져오기
    current_sprint = Sprint.query.get(sprint_id)
    if not current_sprint:
        return False, "Current Sprint not found"

    # 다음 스프린트 찾기
    next_sprint = Sprint.query.filter(
        Sprint.project_id == project_id,
        Sprint.sprint_start_date > current_sprint.sprint_end_date
    ).order_by(Sprint.sprint_start_date).first()

    if not next_sprint:
        return False, "No next Sprint found"

    # 완료되지 않은 스프린트 백로그 가져오기
    incomplete_backlogs = SprintBacklog.query.filter(
        SprintBacklog.sprint_id == sprint_id,
        SprintBacklog.status != 'Done'
    ).all()

    # 해당하는 ProductBacklog의 sprint_id를 다음 스프린트로 업데이트
    for sprint_backlog in incomplete_backlogs:
        product_backlog = ProductBacklog.query.get(sprint_backlog.product_backlog_id)
        if product_backlog:
            product_backlog.sprint_id = next_sprint.sprint_id
            db.session.add(product_backlog) 

    # SprintBacklog의 sprint_id도 다음 스프린트로 업데이트
    for sprint_backlog in incomplete_backlogs:
        sprint_backlog.sprint_id = next_sprint.sprint_id
        db.session.add(sprint_backlog)

    # 스프린트 백로그가 없는 현재 스프린트의 프로덕트 백로그 가져오기
    unassigned_product_backlogs = ProductBacklog.query.filter(
        ProductBacklog.sprint_id == sprint_id,
        ~ProductBacklog.product_backlog_id.in_(
            db.session.query(SprintBacklog.product_backlog_id).filter(
                SprintBacklog.sprint_id == sprint_id
            )
        )
    ).all()

    # 이 프로덕트 백로그들의 sprint_id를 다음 스프린트로 업데이트
    for product_backlog in unassigned_product_backlogs:
        product_backlog.sprint_id = next_sprint.sprint_id
        db.session.add(product_backlog)

    db.session.commit()
    return True, "Backlogs moved successfully"
