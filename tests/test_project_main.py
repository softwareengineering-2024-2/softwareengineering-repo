from unittest.mock import patch, Mock
from flask import json
from datetime import datetime

from flask_login import current_user

# 프로젝트 메인 페이지 렌더링 테스트
def test_project_main_view_authenticated(authenticated_user, mocker, test_app):
    """
    프로젝트 메인 페이지 렌더링 테스트: 인증된 사용자가 프로젝트 메인 페이지를 접근할 수 있는지 확인.
    """
    project_id = 1
    user_id = 1

    # Mock 설정
    mocker.patch('models.project_model.UserProject.find_by_user_and_project', return_value=Mock())
    mocker.patch('models.project_model.Project.find_by_id', return_value=Mock(project_id=project_id, project_name="Test Project"))
    mocker.patch('controllers.sprint_controller.get_current_sprint_backlogs', return_value={"overall_progress_percentage": 50, "sprints": []})
    mocker.patch('controllers.todolist_controller.show_todos', return_value=[])

    with test_app.app_context():
        response = authenticated_user.get(f'/project_main/{project_id}')
        assert response.status_code == 200
        assert 'dashboard' in response.get_data(as_text=True)



def test_create_todo_authenticated(authenticated_user, mocker, test_app):
    """투두리스트 저장 API 테스트"""
    project_id = 1
    form_data = {"todo_content": "새로운 할 일"}

    # Mock 설정
    mocker.patch('controllers.todolist_controller.write_todo', return_value=None)

    with test_app.app_context():
        response = authenticated_user.post(
            f'/project_main/todo/{project_id}',
            data=json.dumps(form_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data(as_text=True))

        # 테스트 검증
        assert response.status_code == 200
        assert response_data['message'] == "success"


def test_get_todos_authenticated(authenticated_user, mocker, test_app):
    """투두리스트 조회 API 테스트"""
    project_id = 1

    # Mock 데이터 생성
    mock_todos = [
        {"todo_id": 1, "todo": "새로운 할 일", "status": False}
    ]

    # Mock 설정
    mocker.patch('controllers.todolist_controller.show_todos', return_value=mock_todos)

    with test_app.app_context():
        response = authenticated_user.get(f'/project_main/get_todo/{project_id}')
        response_data = json.loads(response.get_data(as_text=True))

        # 반환값 확인
        assert response.status_code == 200
        assert len(response_data) == 1
        assert response_data[0]['todo'] == "새로운 할 일"
        assert response_data[0]['status'] is False


def test_update_todo_authenticated(authenticated_user, mocker, test_app):
    """투두리스트 수정 API 테스트"""
    todo_id = 1
    form_data = {"todo_content": "수정된 할 일"}

    # Mock 데이터
    mock_updated_todo = {"todo_id": todo_id, "todo": form_data["todo_content"]}

    # Mock 설정
    mocker.patch('controllers.todolist_controller.update_todos', return_value=mock_updated_todo)

    with test_app.app_context():
        response = authenticated_user.post(
            f'/project_main/update_todo/{todo_id}',
            data=json.dumps(form_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data(as_text=True))

        # 테스트 검증
        assert response.status_code == 200
        assert response_data[0]['todo_id'] == todo_id
        assert response_data[0]['todo'] == form_data["todo_content"]




def test_change_status_authenticated(authenticated_user, mocker, test_app):
    """투두리스트 상태 변경 API 테스트"""
    todo_id = 1

    # Mock 데이터
    mock_status_update = {"todo_id": todo_id, "status": "completed"}

    # Mock 설정
    mocker.patch('controllers.todolist_controller.change_todo_status', return_value=mock_status_update)

    with test_app.app_context():
        response = authenticated_user.post(f'/project_main/change_status/{todo_id}')

        response_data = json.loads(response.get_data(as_text=True))
        print(response_data[0])
        

        # 테스트 검증
        assert response.status_code == 200
        assert response_data[0]['todo'] == '수정된 할 일'
        assert response_data[0]['status'] == True

def test_delete_todo_authenticated(authenticated_user, mocker, test_app):
    """투두리스트 삭제 API 테스트"""
    todo_id = 1

    # Mock 설정
    mocker.patch('controllers.todolist_controller.delete_todos', return_value=None)

    with test_app.app_context():
        response = authenticated_user.delete(f'/project_main/delete_todo/{todo_id}')
        response_data = json.loads(response.get_data(as_text=True))

        # 테스트 검증
        assert response.status_code == 200
        assert response_data['message'] == "success"


# 2주 캘린더
# tests/test_project_main.py

def test_get_schedule_authenticated(authenticated_user, mocker, test_app):
    """
    일정 조회 API 테스트: 특정 프로젝트의 일정을 반환하는지 확인.
    """
    project_id = 1

    # Mock 설정
    mocker.patch('controllers.calendar_controller.create_schedules', return_value=mock_schedules)
    mocker.patch('controllers.calendar_controller.show_schedules', return_value=mock_schedules)
    mocker.patch('controllers.calendar_controller.get_all_schedules', return_value=mock_schedules)

    with test_app.app_context():
        response = authenticated_user.get(f'/project_main/calendar/{project_id}')
        response_data = json.loads(response.get_data(as_text=True))
        print("결과", response_data)

        # 테스트 검증
        assert response.status_code == 200
        assert len(response_data) > 0  # 응답 데이터가 비어 있지 않아야 함
        assert response_data[0]['title'] == '마일스톤 2'

class MockSchedule:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

mock_schedules = [
    MockSchedule(
        calendar_id=1,
        user_id="testuser",
        title="마일스톤 2",
        place=None,
        start_date=datetime(2024, 12, 19),
        due_date=datetime(2024, 12, 19),
        color=0,
        content=None,
        important=True,
        team=True
    )
]