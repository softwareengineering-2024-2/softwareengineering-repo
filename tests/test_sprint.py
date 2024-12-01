from unittest.mock import Mock, patch
from datetime import datetime
from controllers.sprint_controller import (
    assign_backlogs_to_sprint,
    get_unassigned_product_backlogs,
    get_sprints_with_backlogs,
    update_sprint
)

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

def test_delete_sprint(authenticated_user, mocker, test_app):
    """스프린트 삭제 기능을 테스트"""
    sprint_id = 1
    project_id = 1

    # Mock 설정
    mock_sprint = Mock()
    mock_sprint.project_id = project_id
    mock_sprint.sprint_name = 'Test Sprint'  # 필요한 속성 추가
    mocker.patch('controllers.sprint_controller.delete_sprint', return_value=mock_sprint)
    # 모킹 경로 수정: views.sprint_view에서 import한 함수 모킹
    mocker.patch('views.sprint_view.delete_sprint_schedules', return_value=True)
    
    # BacklogChanges.get_last_change를 모킹하여 NoneType 에러 방지
    mock_last_change = Mock()
    mock_last_change.total_backlog = 10
    mock_last_change.completed_backlog = 5
    mocker.patch('controllers.burnup_controller.BacklogChanges.get_last_change', return_value=mock_last_change)

    with test_app.app_context():
        response = authenticated_user.post(f'/sprint/delete-sprint/{sprint_id}')

        # 디버깅용 출력
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.get_data(as_text=True)}")

        assert response.status_code == 302
        assert f'/sprint/{project_id}' in response.headers['Location']

def test_update_backlog_status(authenticated_user, mocker, test_app):
    """스프린트 백로그 상태 업데이트를 테스트"""
    backlog_id = 1
    form_data = {
        'status': 'Done'
    }

    # Mock 설정
    mocker.patch('views.sprint_view.update_backlog_status', return_value=(True, "Status updated successfully", 1))

    with test_app.app_context():
        response = authenticated_user.post(f'/sprint/edit-backlog-status/{backlog_id}', data=form_data)

        # 디버깅용 출력
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.get_data(as_text=True)}")

        assert response.status_code == 302
        assert '/sprint/1' in response.headers['Location']

def test_create_sprint_invalid_dates(authenticated_user, mocker, test_app):
    """스프린트 생성 시 잘못된 날짜 입력을 테스트"""
    form_data = {
        'project_id': '1',
        'sprint_name': 'Invalid Date Sprint',
        'start_date': '2024-12-15',
        'end_date': '2024-12-01',  # 종료일이 시작일보다 이전
        'backlogs': []
    }

    # Mock 설정
    mocker.patch('controllers.sprint_controller.create_sprint', return_value=(None, "Invalid dates: End date must be after start date."))

    with test_app.app_context():
        response = authenticated_user.post('/sprint/add-sprint', data=form_data)

        # 디버깅용 출력
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.get_data(as_text=True)}")

        assert response.status_code == 302
        assert '/sprint/1' in response.headers['Location']

def test_move_incomplete_backlogs_to_next_sprint(authenticated_user, mocker, test_app):
    """미완료 백로그를 다음 스프린트로 이동하는 기능을 테스트"""
    sprint_id = 1
    project_id = 1

    # Mock 설정
    mocker.patch('views.sprint_view.move_incomplete_backlogs_to_next_sprint', return_value=(True, "Backlogs moved successfully"))

    with test_app.app_context():
        response = authenticated_user.post(f'/sprint/move-backlogs/{sprint_id}/{project_id}')

        # 디버깅용 출력
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.get_data(as_text=True)}")

        assert response.status_code == 200
        # JSON 응답을 파싱하여 메시지 확인
        response_json = response.get_json()
        assert response_json['message'] == '백로그가 다음 스프린트로 이전되었습니다.'

def test_assign_backlogs_to_sprint(authenticated_user, mocker, test_app):
    """백로그를 스프린트에 할당하는 기능을 테스트"""
    sprint_id = 1
    new_backlog_ids = [1, 2, 3]

    # Mock 설정
    mocker.patch('controllers.sprint_controller.assign_backlogs_to_sprint', return_value=True)

    result = assign_backlogs_to_sprint(sprint_id, new_backlog_ids)
    assert result == True

def test_get_unassigned_product_backlogs(mocker):
    """할당되지 않은 프로덕트 백로그를 가져오는 기능을 테스트"""
    project_id = 1

    # Mock 데이터 생성
    mock_backlogs = [Mock(product_backlog_id=i, to_dict=lambda i=i: {'product_backlog_id': i}) for i in range(1, 4)]

    # filter_by를 호출할 때 어떤 인자든 받아들이도록 설정
    mock_query = Mock()
    mock_query.filter_by = Mock(return_value=Mock(all=Mock(return_value=mock_backlogs)))
    mocker.patch('models.productbacklog_model.ProductBacklog.query', new=mock_query)

    result = get_unassigned_product_backlogs(project_id)
    assert len(result) == 3
    # 결과를 정렬하여 순서 보장
    result_sorted = sorted(result, key=lambda x: x['product_backlog_id'])
    assert result_sorted[0]['product_backlog_id'] == 1

def test_get_sprints_with_backlogs(mocker):
    """백로그와 함께 스프린트를 가져오는 기능을 테스트"""
    project_id = 1

    # Mock 데이터 생성
    mock_sprint = Mock(
        sprint_id=1,
        sprint_name='Sprint 1',
        sprint_start_date=datetime.strptime('2024-12-01', '%Y-%m-%d').date(),
        sprint_end_date=datetime.strptime('2024-12-15', '%Y-%m-%d').date(),
        status='In Progress',
        product_backlog=[]
    )

    # 메서드 체이닝을 올바르게 모킹
    mock_query = Mock()
    mock_query.options.return_value = mock_query  # options() 호출 시 자신을 반환
    mock_query.filter_by.return_value = mock_query  # filter_by() 호출 시 자신을 반환
    mock_query.all.return_value = [mock_sprint]
    mocker.patch('models.sprint_model.Sprint.query', new=mock_query)

    result = get_sprints_with_backlogs(project_id)
    assert len(result) == 1
    assert result[0]['sprint_name'] == 'Sprint 1'

# 성공
def test_update_sprint_invalid_dates(mocker):
    """스프린트 업데이트 시 잘못된 날짜를 처리하는지 테스트"""
    sprint_id = 1
    updates = {
        'start_date': '2024-12-15',
        'end_date': '2024-12-01'  # 종료일이 시작일보다 이전
    }

    # Mock 스프린트 객체 생성
    mock_sprint = Mock(
        sprint_id=sprint_id,
        sprint_start_date=datetime.strptime('2024-12-15', '%Y-%m-%d').date(),
        sprint_end_date=datetime.strptime('2024-12-01', '%Y-%m-%d').date(),
        is_valid_dates=Mock(return_value=False)
    )
    mocker.patch('models.sprint_model.Sprint.query.get', return_value=mock_sprint)

    updated_sprint = update_sprint(sprint_id, updates)
    assert updated_sprint is None

# 성공
def test_create_sprint_date_overlap(authenticated_user, mocker, test_app):
    """스프린트 생성 시 날짜가 다른 스프린트와 겹치는지 테스트"""
    form_data = {
        'project_id': '1',
        'sprint_name': 'Overlapping Sprint',
        'start_date': '2024-12-05',
        'end_date': '2024-12-10',
        'backlogs': []
    }

    # Mock 설정
    overlapping_sprint = Mock(
        sprint_id=2,
        project_id=1,
        sprint_start_date=datetime.strptime('2024-12-03', '%Y-%m-%d').date(),
        sprint_end_date=datetime.strptime('2024-12-08', '%Y-%m-%d').date()
    )

    # 모킹 경로 수정
    mocker.patch('views.sprint_view.create_sprint', return_value=(None, "Date conflict: Another sprint overlaps with the given dates."))
    mocker.patch('models.sprint_model.Sprint.query.filter', return_value=Mock(all=Mock(return_value=[overlapping_sprint])))

    with test_app.app_context():
        response = authenticated_user.post('/sprint/add-sprint', data=form_data)

        # 디버깅용 출력
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.get_data(as_text=True)}")

        assert response.status_code == 302
        assert '/sprint/1' in response.headers['Location']