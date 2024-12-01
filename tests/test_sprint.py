from flask import url_for
import pytest
from unittest.mock import Mock, patch
from datetime import datetime

# MockSprint 객체를 생성하고 필요한 속성 설정
MockSprint = Mock()

def test_get_product_backlogs_view_authenticated(authenticated_user, test_app):
    """사용자가 인증된 상태에서 스프린트 백로그 뷰를 요청하는 테스트"""
    project_id = 1  # 테스트용 프로젝트 ID

    with test_app.app_context():
        # Mock 데이터베이스와 프로젝트 데이터
        with patch('models.project_model.Project.find_by_id', return_value=Mock(project_id=project_id, project_name="Test Project")):
            with patch('models.project_model.UserProject.find_by_user_and_project', return_value=Mock(id=1)):
                with patch('controllers.sprint_controller.get_sprints_with_backlogs', return_value=[]):
                    with patch('controllers.sprint_controller.get_all_product_backlogs', return_value=[]):
                        with patch('controllers.sprint_controller.get_unassigned_product_backlogs', return_value=[]):
                            response = authenticated_user.get(f'/sprint/{project_id}')
                            
                            # 디버깅용 출력
                            print(f"Response data: {response.get_data(as_text=True)}")
                            print(f"Response status code: {response.status_code}")
                            
                            # 인증 실패 여부 확인
                            assert response.status_code != 302, "Authentication failed. Check authenticated_user fixture."
                            
                            assert response.status_code == 200
                            assert '스프린트' in response.get_data(as_text=True)

def test_add_sprint(authenticated_user, mocker, test_app):
    """스프린트 추가 기능을 테스트"""
    form_data = {
        'project_id': '1',
        'sprint_name': 'New Sprint',
        'start_date': '2024-12-01',
        'end_date': '2024-12-15',
        'backlogs': ['1','2']
    }
    MockSprint.start_date = datetime.strptime('2024-12-01', '%Y-%m-%d').date()
    MockSprint.end_date = datetime.strptime('2024-12-15', '%Y-%m-%d').date()
    
    # Mock 설정
    mocker.patch('controllers.sprint_controller.create_sprint', return_value=(MockSprint, None))
    mocker.patch('views.sprint_view.create_schedules', return_value=True)
    mocker.patch('controllers.sprint_controller.assign_backlogs_to_sprint', return_value=True)

    with test_app.app_context():
        # 실제 URL에 맞게 수정
        response = authenticated_user.post('/sprint/add-sprint', data=form_data)

        # 디버깅용 출력
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.get_data(as_text=True)}")

        assert response.status_code == 302
        assert '/sprint/1' in response.headers['Location']


def test_edit_sprint(authenticated_user, mocker,test_app):
    """스프린트 수정 기능을 테스트"""
    form_data = {
        'sprint_name': 'Updated Sprint',
        'start_date': '2023-02-01',
        'end_date': '2023-02-15',
        'backlogs': ['3','4']
    }
    mocker.patch('controllers.sprint_controller.update_sprint', return_value=True)
    mocker.patch('controllers.calendar_controller.update_sprint_schedules', return_value=True)
    mocker.patch('controllers.sprint_controller.assign_backlogs_to_sprint', return_value=True)

    with test_app.app_context():
        response = authenticated_user.post('/sprint/edit-sprint/1/2', data=form_data)
        assert response.status_code == 302
        assert '/sprint/2' in response.headers['Location']

