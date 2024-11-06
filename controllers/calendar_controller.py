from models.calendar_model import Calendar
from flask_login import current_user

# 모든 일정(팀+개인)을 가져오는 로직
def get_all_schedules(project_id):
    return Calendar.find_by_project(project_id)

# 모든 팀 또는 개인 일정을 가져오는 로직
def get_schedules_of_team_or_personal(project_id, team):
    return Calendar.find_by_project_and_team(project_id, team)

# 새로운 일정을 생성하고 저장하는 로직
def create_schedule(project_id, title, place, start_date, due_date, team, color, content, important):
    if not title or not start_date or not due_date:
        return "일정 제목과 기간을 입력해야 합니다."
    new_schedule = Calendar(user_id=current_user.id, project_id=project_id, title=title, place=place, start_date=start_date, due_date=due_date, team=team, color=color, content=content, important=important)
    new_schedule.save_to_db()
    return "일정이 추가되었습니다."

# 일정을 수정하는 로직
def update_schedule(calendar_id, title, place, start_date, due_date, team, color, content, important):
    if not title or not start_date or not due_date:
        return "일정 제목과 기간을 입력해야 합니다."
    
    schedule = Calendar.find_by_id(calendar_id)
    if schedule:
        schedule.update_calendar(calendar_id, title, place, start_date, due_date, team, color, content, important)
        return "일정이 수정되었습니다."
    return "일정을 찾을 수 없습니다."

# 일정을 삭제하는 로직
def delete_schedule(calendar_id):
    schedule = Calendar.find_by_id(calendar_id)
    if schedule:
        schedule.delete_from_db()
        return "일정이 삭제되었습니다."
    return "일정을 찾을 수 없습니다."
