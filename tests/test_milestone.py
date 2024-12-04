from unittest.mock import Mock, patch
from datetime import date, timedelta
from models.milestone_model import Milestone

MockMilestone = Mock()
MockCalendar = Mock()

def test_milestone_view(authenticated_user, test_app):
    """사용자가 인증된 상태에서 마일스톤 페이지를 요청하는 테스트"""
    project_id = 1
    total_count = 3
    completed_count = 2

    # Mock 설정
    mock_milestones = [
        Mock(milestone_id=1, project_id=project_id, milestone_content="마일스톤 1", due_date=date(2024, 12, 1), check=True),
        Mock(milestone_id=2, project_id=project_id, milestone_content="마일스톤 2", due_date=date(2024, 12, 19), check=False)
    ]

    with test_app.app_context():
        with patch('models.project_model.Project.find_by_id', return_value=Mock(project_id=project_id, project_name="Test Project")):
            with patch('models.project_model.UserProject.find_by_user_and_project', return_value=Mock(project_id=1)):
                with patch('controllers.milestone_controller.get_milestones', return_value=mock_milestones):
                    with patch('controllers.milestone_controller.get_milestone_counts', return_value=(total_count, completed_count)):
                        response = authenticated_user.get(f'/milestone/{project_id}')
            
                        # 디버깅용 출력
                        print(f"Response status code: {response.status_code}")
                        print(f"Response data: {response.get_data(as_text=True)}")

                        # 마일스톤 목록 페이지 확인
                        assert response.status_code == 200
                        assert "마일스톤 목록" in response.get_data(as_text=True)

def test_create_milestone(authenticated_user, mocker, test_app):
    """마일스톤 생성 기능을 테스트"""
    project_id = 1
    
    form_data = {
        'milestone_content': 'New Milestone',
        'due_date': date(2024, 12, 1)
    }

    # Mock 설정
    mocker.patch('controllers.milestone_controller.create_milestone', return_value=MockMilestone)
    mocker.patch('models.milestone_model.Milestone.save_to_db', return_value=None)
    mocker.patch('controllers.calendar_controller.create_schedules', return_value=MockCalendar)
    mocker.patch('models.calendar_model.Calendar.save_to_db', return_value=None)
    
    with test_app.app_context():
        response = authenticated_user.post(f'/milestone/{project_id}/create', data=form_data)

        # 디버깅용 출력
        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.get_data(as_text=True)}")

        assert response.status_code == 302
        assert '/milestone/1' in response.headers['Location']
        
def test_delete_milestone(authenticated_user, mocker, test_app):
    """마일스톤 삭제 기능을 테스트"""
    # Mock 설정
    mocker.patch('models.milestone_model.Milestone.find_by_id', return_value=Mock(milestone_id=2, project_id=1, milestone_content="마일스톤 2"))
    mocker.patch('models.calendar_model.Calendar.find_by_title', return_value=Mock(calendar_id=1, project_id=1, title="마일스톤 2"))
    mocker.patch('controllers.milestone_controller.delete_milestone', return_value=None)
    mocker.patch('controllers.calendar_controller.delete_milestone_schedules', return_value=None)

    with test_app.app_context():
        response = authenticated_user.post('/milestone/1/2/delete')

        # 디버깅용 출력
        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.get_data(as_text=True)}")

        # 삭제 후 리디렉션 확인
        assert response.status_code == 302
        assert '/milestone/1' in response.headers['Location']

def test_save_to_db_and_delete_from_db(test_app):
    """마일스톤을 저장하고 삭제하는 기능을 테스트"""
    project_id = 1
    milestone_content = "Test Save and Delete"
    due_date = date(2024, 12, 15)

    # 새 마일스톤 객체 생성 및 저장 테스트
    new_milestone = Milestone(project_id=project_id, milestone_content=milestone_content, due_date=due_date, check=False)
    with test_app.app_context():
        new_milestone.save_to_db()
        saved_milestone = Milestone.find_by_id(new_milestone.milestone_id)
        assert saved_milestone is not None
        assert saved_milestone.milestone_content == milestone_content

        # 마일스톤 삭제 테스트
        saved_milestone.delete_from_db()
        deleted_milestone = Milestone.find_by_id(new_milestone.milestone_id)
        assert deleted_milestone is None

def test_update_milestone(test_app):
    """마일스톤 업데이트 기능을 테스트"""
    project_id = 1
    milestone_content = "Initial Content"
    updated_content = "Updated Content"
    initial_date = date(2024, 12, 1)
    updated_date = date(2024, 12, 2)

    # 초기 마일스톤 객체 생성 및 저장
    initial_milestone = Milestone(project_id=project_id, milestone_content=milestone_content, due_date=initial_date, check=False)
    with test_app.app_context():
        initial_milestone.save_to_db()
        
        # 마일스톤 업데이트 테스트
        Milestone.update_milestone(initial_milestone.milestone_id, updated_content, updated_date)
        updated_milestone = Milestone.find_by_id(initial_milestone.milestone_id)
        assert updated_milestone.milestone_content == updated_content
        assert updated_milestone.due_date == updated_date

        # 정리
        updated_milestone.delete_from_db()

def test_update_check_status(test_app):
    """마일스톤 check 상태 업데이트 기능을 테스트"""
    project_id = 1
    milestone_content = "Check Status Test"
    past_date = date.today() - timedelta(days=1)  # 과거 날짜
    future_date = date.today() + timedelta(days=1)  # 미래 날짜

    past_milestone = Milestone(project_id=project_id, milestone_content=milestone_content, due_date=past_date, check=False)
    future_milestone = Milestone(project_id=project_id, milestone_content=milestone_content, due_date=future_date, check=False)

    with test_app.app_context():
        past_milestone.save_to_db()
        future_milestone.save_to_db()

        Milestone.update_check_status(project_id)
        
        # 과거 날짜 마일스톤의 check는 True 여야 함
        updated_past_milestone = Milestone.find_by_id(past_milestone.milestone_id)
        assert updated_past_milestone.check == True

        # 미래 날짜 마일스톤의 check는 False 여야 함
        updated_future_milestone = Milestone.find_by_id(future_milestone.milestone_id)
        assert updated_future_milestone.check == False

        # 정리
        updated_past_milestone.delete_from_db()
        updated_future_milestone.delete_from_db()
