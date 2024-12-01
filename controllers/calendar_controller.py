from flask import request
from models.calendar_model import Calendar
from models.milestone_model import Milestone
from models.sprint_model import Sprint
from flask_login import current_user

# 모든 일정(팀+개인)을 가져오는 로직
def get_all_schedules(project_id):
    # 프로젝트에 속한 모든 일정을 반환하지만, 개인 일정은 현재 사용자가 생성한 것만 포함
    schedules = Calendar.query.filter_by(project_id=project_id).all()
    filtered_schedules = []
    for schedule in schedules:
        if not schedule.team:  # 개인 일정인 경우
            if schedule.user_id == current_user.id:  # 현재 사용자가 생성한 일정만 포함
                filtered_schedules.append(schedule)
        else:
            filtered_schedules.append(schedule)
    return filtered_schedules


# 팀 일정 조회
def get_schedules_of_team(project_id):
    return Calendar.query.filter_by(project_id=project_id,team=1).all()

# 개인 일정 조회
def get_schedules_of_personal(project_id, user_id):
    return Calendar.query.filter_by(project_id=project_id,team=0,user_id=user_id).all()

# 일정 조회
def show_schedules(project_id, user_id):
    team = request.args.get('team', 'true').lower()
    personal = request.args.get('personal', 'true').lower()

    
    
    if team:
        schedules = get_schedules_of_team(project_id)
    if personal:
        schedules = get_schedules_of_personal(project_id, user_id)

    if team and personal:
        schedules = get_all_schedules(project_id)
        
    return [{"calendar_id": schedules.calendar_id,
             "user_id": schedules.user_id,
            "title": schedules.title,
            "place": schedules.place,
            "start_date": schedules.start_date.isoformat(),
            "due_date": schedules.due_date.isoformat(),
            "color": schedules.color,
            "content": schedules.content,
            "important": schedules.important,
            "team": schedules.team
            } for schedules in schedules] 

# 일정 추가
def create_schedules(user_id,project_id, title, place, start_date, due_date, team, color, content, important):
    schedule = Calendar(user_id=user_id, project_id=project_id, title=title, place=place, start_date=start_date, due_date=due_date, team=team, color=color, content=content, important=important)
    schedule.save_to_db()

# 일정 수정
def update_schedules(calendar_id,title, place, start_date, due_date, team, color, content, important):
    schedule = Calendar.find_by_id(calendar_id)
    schedule.update_calendar( title, place, start_date, due_date, team, color, content, important)
    return [{'title': schedule.title,
            'place': schedule.place,
            'start_date': schedule.start_date,
            'due_date': schedule.due_date,
            'team': schedule.team,
            'color': schedule.color,
            'content': schedule.content,
            'important': schedule.important
                }]

# 일정 삭제
def delete_schedules(calendar_id):
    schedule = Calendar.find_by_id(calendar_id)
    schedule.delete_from_db()
    return None

# 마일스톤 일정 삭제
def delete_milestone_schedules(project_id, milestone_id):
    milestone_content = Milestone.find_by_id(milestone_id).milestone_content
    schedule = Calendar.find_by_title(project_id, milestone_content)
    schedule.delete_from_db()
    return None

# 스프린트 일정 수정
def update_sprint_schedules(project_id, sprint_name, start_date, end_date):
    schedule = Calendar.find_by_title(project_id, sprint_name)
    if schedule:
        schedule.update_calendar(sprint_name, None, start_date, end_date, True, 0, None, True)
    return None

# 스프린트 일정 삭제
def delete_sprint_schedules(project_id, sprint_name):
    schedule = Calendar.find_by_title(project_id, sprint_name)
    schedule.delete_from_db()
    return None