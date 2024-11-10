from models.milestone_model import Milestone
from flask_login import current_user

# 모든 마일스톤을 가져오는 로직
def get_milestones(project_id):
    Milestone.update_check_status(project_id)
    return Milestone.find_by_project_ordered_by_due_date(project_id)

# 새로운 마일스톤을 생성하고 저장하는 로직
def create_milestone(project_id, milestone_content, due_date):
    new_milestone = Milestone(project_id=project_id, milestone_content=milestone_content, due_date=due_date, check=False)
    new_milestone.save_to_db()
    return "마일스톤이 추가되었습니다."

# 마일스톤을 수정하는 로직
def update_milestone(milestone_id, milestone_content, due_date):
    if not milestone_content or not due_date:
        return "마일스톤 내용과 마감 기한을 입력해야 합니다."
    
    milestone = Milestone.find_by_id(milestone_id)
    if milestone:
        milestone.update_milestone(milestone_id, milestone_content, due_date)
        return "마일스톤이 수정되었습니다."
    return "마일스톤을 찾을 수 없습니다."

# 마일스톤을 삭제하는 로직
def delete_milestone(milestone_id):
    milestone = Milestone.find_by_id(milestone_id)
    if milestone:
        milestone.delete_from_db()
        return "마일스톤이 삭제되었습니다."
    return "마일스톤을 찾을 수 없습니다."

# 마일스톤 수를 계산하는 로직
def get_milestone_counts(project_id):
    milestones = Milestone.find_by_project_ordered_by_due_date(project_id)
    total_count = len(milestones)
    completed_count = sum(1 for milestone in milestones if milestone.check)
    return total_count, completed_count