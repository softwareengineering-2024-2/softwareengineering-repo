from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from models.burnup_model import BacklogChanges
from controllers.burnup_controller import get_burnup_data, increment_total_backlog, decrement_total_backlog, update_completed_backlog
from sqlalchemy.orm.exc import NoResultFound

def test_burnup_view_rendering(authenticated_user, test_app):
    """Burnup 차트 뷰 렌더링 테스트"""
    project_id = 1
    with test_app.app_context():
        with patch('models.project_model.Project.find_by_id', return_value=Mock(project_id=project_id, project_name="Test Project")):
            with patch('models.project_model.UserProject.find_by_user_and_project', return_value=Mock(project_id=1)):
                with patch('controllers.burnup_controller.get_burnup_data', return_value=([], [], [])):
                    response = authenticated_user.get(f'/burnup/{project_id}')
                    
                    # 디버깅용 출력
                    print(f"Response status code: {response.status_code}")
                    print(f"Response data: {response.get_data(as_text=True)}")

                    # 번업차트 페이지 확인
                    assert response.status_code == 200
                    assert "번업차트" in response.get_data(as_text=True)


def test_get_last_change(authenticated_user, test_app):
    """get_last_change 메서드 호출 테스트"""
    project_id = 1
    with test_app.app_context():
        with patch('models.burnup_model.BacklogChanges.query') as mock_query:
            mock_query.filter_by.return_value.order_by.return_value.first.return_value = Mock(total_backlog=30, completed_backlog=15)
            result = BacklogChanges.get_last_change(project_id)
            assert result.total_backlog == 30
            assert result.completed_backlog == 15


def test_burnup_data_retrieval(authenticated_user, test_app):
    """번업 차트 데이터를 가져오는 기능을 테스트"""
    project_id = 1
    mock_changes = [
        Mock(change_id=1, project_id=project_id, changed_date=datetime.today(), total_backlog=10, completed_backlog=5),
        Mock(change_id=2, project_id=project_id, changed_date=datetime.today() + timedelta(days=1), total_backlog=15, completed_backlog=10)
    ]

    with test_app.app_context():
        with patch('models.burnup_model.BacklogChanges.get_changes_by_project', return_value=mock_changes):
            dates, totals, completeds = get_burnup_data(project_id)
            
            # 디버깅용 출력
            print(f"Dates: {dates}, Totals: {totals}, Completeds: {completeds}")
            
            # 데이터 검증
            assert len(dates) == len(totals) == len(completeds) == 2
            assert totals == [10, 15]
            assert completeds == [5, 10]

def test_increment_total_backlog_functionality(authenticated_user, test_app):
    """총 백로그 수 증가 기능을 테스트"""
    project_id = 1

    with test_app.app_context():
        with patch('models.burnup_model.BacklogChanges.get_last_change', return_value=Mock(total_backlog=20, completed_backlog=10)), \
             patch('models.burnup_model.BacklogChanges.save_to_db') as mock_save:
            increment_total_backlog(project_id)
            mock_save.assert_called_once()

def test_decrement_total_backlog_functionality(authenticated_user, test_app):
    """총 백로그 수 감소 기능을 테스트"""
    project_id = 1

    with test_app.app_context():
        with patch('models.burnup_model.BacklogChanges.get_last_change', return_value=Mock(total_backlog=20, completed_backlog=10)), \
             patch('models.burnup_model.BacklogChanges.save_to_db') as mock_save:
            decrement_total_backlog(project_id)
            mock_save.assert_called_once()

def test_update_completed_backlog_functionality(authenticated_user, test_app):
    """완료된 백로그 수 업데이트 기능을 테스트"""
    project_id = 1
    done_backlog_count = 2

    with test_app.app_context():
        with patch('models.burnup_model.BacklogChanges.get_last_change', return_value=Mock(total_backlog=20, completed_backlog=10)), \
             patch('models.burnup_model.BacklogChanges.save_to_db') as mock_save:
            update_completed_backlog(project_id, done_backlog_count)
            mock_save.assert_called_once()

def test_increment_total_backlog_no_existing_record(authenticated_user, test_app):
    """Test incrementing the total backlog when no record exists for the current day."""
    project_id = 1
    today = datetime.today().date()

    with test_app.app_context():
        with patch('models.burnup_model.BacklogChanges.query') as mock_query:
            mock_query.filter_by().one.side_effect = NoResultFound
            mock_last_change = Mock(total_backlog=20, completed_backlog=10)
            with patch('models.burnup_model.BacklogChanges.get_last_change', return_value=mock_last_change):
                with patch('models.burnup_model.BacklogChanges.save_to_db') as mock_save:
                    new_change = BacklogChanges(project_id=project_id, changed_date=today, total_backlog=mock_last_change.total_backlog + 1, completed_backlog=mock_last_change.completed_backlog)
                    increment_total_backlog(project_id)
                    mock_save.assert_called_once()
                    assert new_change.total_backlog == 21  # Ensure it increments

def test_decrement_total_backlog_no_existing_record(authenticated_user, test_app):
    """Test decrementing the total backlog when no record exists for the current day."""
    project_id = 1
    today = datetime.today().date()

    with test_app.app_context():
        with patch('models.burnup_model.BacklogChanges.query') as mock_query:
            mock_query.filter_by().one.side_effect = NoResultFound
            mock_last_change = Mock(total_backlog=20, completed_backlog=10)
            with patch('models.burnup_model.BacklogChanges.get_last_change', return_value=mock_last_change):
                with patch('models.burnup_model.BacklogChanges.save_to_db') as mock_save:
                    new_change = BacklogChanges(project_id=project_id, changed_date=today, total_backlog=mock_last_change.total_backlog - 1, completed_backlog=mock_last_change.completed_backlog)
                    decrement_total_backlog(project_id)
                    mock_save.assert_called_once()
                    assert new_change.total_backlog == 19

def test_update_completed_backlog_no_existing_record(authenticated_user, test_app):
    """Test updating the completed backlog when no record exists for the current day."""
    project_id = 1
    done_backlog_count = 2
    today = datetime.today().date()

    with test_app.app_context():
        with patch('models.burnup_model.BacklogChanges.query') as mock_query:
            mock_query.filter_by().one.side_effect = NoResultFound
            mock_last_change = Mock(total_backlog=20, completed_backlog=10)
            with patch('models.burnup_model.BacklogChanges.get_last_change', return_value=mock_last_change):
                with patch('models.burnup_model.BacklogChanges.save_to_db') as mock_save:
                    new_change = BacklogChanges(project_id=project_id, changed_date=today, total_backlog=mock_last_change.total_backlog, completed_backlog=mock_last_change.completed_backlog + done_backlog_count)
                    update_completed_backlog(project_id, done_backlog_count)
                    mock_save.assert_called_once()
                    assert new_change.completed_backlog == 12