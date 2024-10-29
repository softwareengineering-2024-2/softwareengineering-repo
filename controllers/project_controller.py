from models.project_model import Project

# 새로운 프로젝트를 생성하고 저장하는 로직
def create_project(project_name):
    new_project = Project(project_name)
    new_project.save_to_db()
    return f"Project '{new_project.project_name}' created successfully with ID {new_project.project_id}!"

# 프로젝트 링크를 통해 사용자를 프로젝트에 추가하는 로직
def join_project_by_link(project_link):
    project = Project.find_by_link(project_link)  # find_by_link() 아직 구현 안함
    if project:
        # 여기에 현재 사용자를 프로젝트 팀원으로 추가하는 로직을 작성합니다.
        return f"프로젝트 '{project.project_name}'에 성공적으로 참여했습니다."
    else:
        return "유효하지 않은 프로젝트 링크입니다."

# 모든 프로젝트를 가져오는 로직
def get_all_projects():
    projects = Project.find_all()
    return projects

# 특정 ID의 프로젝트를 삭제하는 로직
def delete_project(project_id):
    project = Project.find_by_id(project_id)
    if project:
        project.delete_from_db()
        return f"Project '{project.project_name}' deleted successfully."
    else:
        return "Project not found or already deleted."
