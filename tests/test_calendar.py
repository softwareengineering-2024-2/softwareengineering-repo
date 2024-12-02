from unittest.mock import patch, Mock
from flask import json
from datetime import datetime

MockCalendar = Mock()

# 캘린더 페이지 렌더링 테스트
def test_calendar_view_authenticated(authenticated_user, mocker, test_app):
    """
    캘린더 페이지 렌더링 테스트: 인증된 사용자가 캘린더 페이지를 접근할 수 있는지 확인.
    """
    project_id = 1

    # Mock 설정
    mocker.patch('models.project_model.UserProject.find_by_user_and_project', return_value=Mock())
    mocker.patch('models.project_model.Project.find_by_id', return_value=Mock(project_id=project_id, project_name="Test Project"))
    mocker.patch('controllers.calendar_controller.show_schedules', return_value=[])

    with test_app.app_context():
        response = authenticated_user.get(f'/calendar/{project_id}')
        assert response.status_code == 200
        assert 'calendar' in response.get_data(as_text=True)

# 일정 조회 테스트
def test_get_schedule(authenticated_user, mocker, test_app):
    """
    일정 조회 API 테스트: 특정 프로젝트의 일정을 반환하는지 확인.
    """
    project_id = 1

    # Mock 데이터 생성
    mock_schedule = Mock()
    mock_schedule.calendar_id = 1
    mock_schedule.user_id = 'testuser'
    mock_schedule.title = '마일스톤 2'
    mock_schedule.place = None
    mock_schedule.start_date = datetime(2024, 12, 19)  # datetime 객체로 설정
    mock_schedule.due_date = datetime(2024, 12, 19)    # datetime 객체로 설정
    mock_schedule.color = 0
    mock_schedule.content = None
    mock_schedule.important = True
    mock_schedule.team = True

    mock_schedules = [mock_schedule]

    # Mock 설정
    mocker.patch('controllers.calendar_controller.show_schedules', return_value=mock_schedules)
    mocker.patch('controllers.calendar_controller.get_all_schedules', return_value=mock_schedules)
    mocker.patch('controllers.calendar_controller.get_schedules_of_team', return_value=mock_schedules)
    mocker.patch('controllers.calendar_controller.get_schedules_of_personal', return_value=mock_schedules)

    with test_app.app_context():
        response = authenticated_user.get(f'/calendar/schedules/{project_id}/?team=true&personal=true')
        response_data = json.loads(response.get_data(as_text=True))
        assert response.status_code == 200
        expected_data = [{
            "calendar_id": 1,
            "user_id": "testuser",
            "title": "마일스톤 2",
            "place": None,
            "start_date": "2024-12-19T00:00:00",  # datetime 객체의 isoformat() 결과
            "due_date": "2024-12-19T00:00:00",   # datetime 객체의 isoformat() 결과
            "color": 0,
            "content": None,
            "important": True,
            "team": True
        }]
        assert response_data == expected_data

# 일정 추가 테스트
def test_create_schedule(authenticated_user, mocker, test_app):
    """
    일정 추가 API 테스트: 올바른 데이터를 받아 일정이 성공적으로 생성되는지 확인.
    """
    project_id = 1
    form_data = {
        "title": "마일스톤 2",
        "place": None,
        "start_date": "2024-12-19T00:00:00",  # datetime 객체의 isoformat() 결과
        "due_date": "2024-12-19T00:00:00",   # datetime 객체의 isoformat() 결과
        "color": 0,
        "content": None,
        "important": True,
        "team": True
    }

    MockCalendar.start_date = datetime.strptime('2024-12-01', '%Y-%m-%d').date()
    MockCalendar.due_date = datetime.strptime('2024-12-05', '%Y-%m-%d').date()

    # Mock 설정
    mocker.patch('controllers.calendar_controller.create_schedules', return_value=(MockCalendar, None))
    mocker.patch('models.calendar_model.Calendar.save_to_db', return_value=None)

    with test_app.app_context():
        response = authenticated_user.post(
            f'/calendar/{project_id}/',
            data=json.dumps(form_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data(as_text=True))

        assert response.status_code == 200
        assert response_data['message'] == "create success"

# 일정 수정 테스트
def test_update_schedule(authenticated_user, mocker, test_app):
    """
    일정 수정 API 테스트: 올바른 데이터를 받아 일정이 성공적으로 수정되는지 확인.
    """
    calendar_id = 1

        # Mock 데이터 생성
    mock_schedule = Mock()
    mock_schedule.calendar_id = 1
    mock_schedule.user_id = 'testuser'
    mock_schedule.title = '마일스톤 2'
    mock_schedule.place = None
    mock_schedule.start_date = datetime(2024, 12, 19)  # datetime 객체로 설정
    mock_schedule.due_date = datetime(2024, 12, 19)    # datetime 객체로 설정
    mock_schedule.color = 0
    mock_schedule.content = None
    mock_schedule.important = True
    mock_schedule.team = True
    form_data = {
        "title": "마일스톤 2",
        "place": None,
        "start_date": "2024-12-19T00:00:00",  # datetime 객체의 isoformat() 결과
        "due_date": "2024-12-19T00:00:00",   # datetime 객체의 isoformat() 결과
        "color": 0,
        "content": None,
        "important": True,
        "team": True
    }

    # Mock 설정
    mocker.patch('controllers.calendar_controller.update_schedules', return_value=True)
    mocker.patch('models.calendar_model.Calendar.find_by_id', return_value=MockCalendar)
    mocker.patch('models.calendar_model.Calendar.update_calendar', return_value=None)

    with test_app.app_context():
        response = authenticated_user.post(
            f'/calendar/update/{calendar_id}',
            data=json.dumps(form_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data(as_text=True))

        assert response.status_code == 200
        assert response_data['message'] == "modify success"

# 일정 삭제 테스트
def test_delete_schedule(authenticated_user, mocker, test_app):
    """
    일정 삭제 API 테스트: 특정 ID의 일정이 성공적으로 삭제되는지 확인.
    """
    calendar_id = 1
    mock_schedule = Mock()
    mock_schedule.calendar_id = 1
    mock_schedule.user_id = 'testuser'
    mock_schedule.title = '마일스톤 2'
    mock_schedule.place = None
    mock_schedule.start_date = datetime(2024, 12, 19)  # datetime 객체로 설정
    mock_schedule.due_date = datetime(2024, 12, 19)    # datetime 객체로 설정
    mock_schedule.color = 0
    mock_schedule.content = None
    mock_schedule.important = True
    mock_schedule.team = True

    # Mock 설정
    mocker.patch('controllers.calendar_controller.delete_schedules', return_value=True)
    mocker.patch('models.calendar_model.Calendar.find_by_id', return_value=mock_schedule)
    mocker.patch('models.calendar_model.Calendar.delete_from_db', return_value=None)
    
    with test_app.app_context():
        response = authenticated_user.delete(f'/calendar/{calendar_id}')
        response_data = json.loads(response.get_data(as_text=True))

        assert response.status_code == 200
        assert response_data['message'] == "delete success"
