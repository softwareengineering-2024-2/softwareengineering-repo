from models.burnup_model import BacklogChanges
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime

# burnup chart를 그리기 위한 데이터를 가져오는 함수
def get_burnup_data(project_id):
    changes = BacklogChanges.get_changes_by_project(project_id)
    dates = [change.changed_date.strftime('%Y-%m-%d') for change in changes]
    totals = [change.total_backlog for change in changes]
    completeds = [change.completed_backlog for change in changes]
    return dates, totals, completeds

# 스프린트 백로그 생성 시 총 백로그 수를 증가시키는 함수
def increment_total_backlog(project_id):
    today = datetime.today().date()
    try:
        change = BacklogChanges.query.filter_by(project_id=project_id, changed_date=today).one()
        change.total_backlog += 1  # 총 백로그 수 증가
    except NoResultFound:
        last_change = BacklogChanges.get_last_change(project_id) # 최근 변경사항
        change = BacklogChanges(project_id=project_id, changed_date=today, total_backlog=last_change.total_backlog+1, completed_backlog=last_change.completed_backlog)
    change.save_to_db()
    return None

# 스프린트 백로그 삭제 시 총 백로그 수를 감소시키는 함수
def decrement_total_backlog(project_id):
    today = datetime.today().date()
    try:
        change = BacklogChanges.query.filter_by(project_id=project_id, changed_date=today).one()
        change.total_backlog -= 1  # 총 백로그 수 감소
    except NoResultFound:
        last_change = BacklogChanges.get_last_change(project_id) # 최근 변경사항
        change = BacklogChanges(project_id=project_id, changed_date=today, total_backlog=last_change.total_backlog-1, completed_backlog=last_change.completed_backlog)
    change.save_to_db()
    return None

# 스크럼보드에서 스프린트 백로그의 상태를 'done'으로 변경하거나 'done'에서 다른 상태로 변경 시 완료된 백로그 수를 업데이트하는 함수
def update_completed_backlog(project_id, done_backlog_count):
    today = datetime.today().date()
    try:
        change = BacklogChanges.query.filter_by(project_id=project_id, changed_date=today).one()
        change.completed_backlog += done_backlog_count  # 완료된 백로그 수 증가
    except NoResultFound:
        last_change = BacklogChanges.get_last_change(project_id) # 최근 변경사항
        change = BacklogChanges(project_id=project_id, changed_date=today, total_backlog=last_change.total_backlog, completed_backlog=last_change.completed_backlog+done_backlog_count)
    change.save_to_db()
    return None

# 스프린트 수정/삭제로 인한 백로그 삭제 시 변경된 백로그 수를 업데이트하는 함수
def decrement_total_and_completed_backlog(project_id, total_backlog_count, done_backlog_count):
    today = datetime.today().date()
    try:
        change = BacklogChanges.query.filter_by(project_id=project_id, changed_date=today).one()
        change.total_backlog -= total_backlog_count  # 총 백로그 수 증가
        change.completed_backlog -= done_backlog_count  # 완료된 백로그 수 증가
    except NoResultFound:
        last_change = BacklogChanges.get_last_change(project_id) # 최근 변경사항
        change = BacklogChanges(project_id=project_id, changed_date=today, total_backlog=last_change.total_backlog-total_backlog_count, completed_backlog=last_change.completed_backlog-done_backlog_count)
    change.save_to_db()
    return None
