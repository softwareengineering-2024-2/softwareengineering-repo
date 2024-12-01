from unittest.mock import Mock

def mock_url_for(endpoint, **values):
    """특정 엔드포인트를 처리하기 위한 mock된 url_for 함수"""
    if endpoint == 'calendar.calendar_view':
        return f"/calendar/{values.get('project_id')}"
    return f"/{endpoint}/" + "/".join(str(v) for v in values.values())

def test_scrum_view_no_sprints(authenticated_user, test_app, mocker):
    """프로젝트에 스프린트가 없는 경우 테스트"""
    project_id = 1
    mock_project = Mock()
    mock_project.project_id = project_id
    mock_project.project_name = 'Test Project'
    mock_project.__bool__ = Mock(return_value=True)  # 프로젝트 객체가 True로 평가되도록 설정

    with test_app.app_context():
        mock_project_query = Mock()
        mock_project_query.get.return_value = mock_project
        mocker.patch('views.scrum_view.Project.query', mock_project_query)

        mocker.patch('views.scrum_view.get_user_projects', return_value=[]) 
        mocker.patch('views.scrum_view.get_sprints_with_backlogs', return_value=[])
        mocker.patch('flask.url_for', side_effect=mock_url_for)

        response = authenticated_user.get(f'/scrum/{project_id}')

        # 인증 실패 여부 확인
        assert response.status_code != 302, "Authentication failed. Check authenticated_user fixture."

        assert response.status_code == 200
        assert '현재 프로젝트에 스프린트가 없습니다.' in response.get_data(as_text=True)

def test_scrum_view_selected_sprint_not_found(authenticated_user, test_app, mocker):
    """선택된 스프린트가 존재하지 않는 경우 테스트"""
    project_id = 1
    sprint_id = 999  # 존재하지 않는 스프린트 ID

    mock_project = Mock()
    mock_project.project_id = project_id
    mock_project.project_name = 'Test Project'
    mock_project.__bool__ = Mock(return_value=True)       
    mock_sprints = [
        {
            "sprint_id": 1,
            "sprint_name": "Sprint 1",
            "is_past_due": False
        }
    ]

    with test_app.app_context():
        mock_project_query = Mock()
        mock_project_query.get.return_value = mock_project
        mocker.patch('views.scrum_view.Project.query', mock_project_query)

        mocker.patch('views.scrum_view.get_user_projects', return_value=[])
        mocker.patch('views.scrum_view.get_sprints_with_backlogs', return_value=mock_sprints)

        mock_sprint_query = Mock()
        mock_sprint_query.get.return_value = None  # 스프린트가 not found일 때
        mocker.patch('views.scrum_view.Sprint.query', mock_sprint_query)

        # 'url_for' 패치
        mocker.patch('flask.url_for', side_effect=mock_url_for)

        response = authenticated_user.get(f'/scrum/{project_id}?sprint_id={sprint_id}')

        assert response.status_code == 200
        assert '선택된 스프린트를 찾을 수 없습니다.' in response.get_data(as_text=True)

def test_scrum_view_sprint_backlogs(authenticated_user, test_app, mocker):
    """스프린트 백로그 로딩 및 상태별 분류 테스트"""
    project_id = 1
    sprint_id = 1

    mock_project = Mock()
    mock_project.project_id = project_id
    mock_project.project_name = 'Test Project'
    mock_project.__bool__ = Mock(return_value=True)

    mock_sprints = [
        {
            "sprint_id": sprint_id,
            "sprint_name": "Sprint 1",
            "is_past_due": False
        }
    ]

    mock_sprint = Mock()
    mock_sprint.sprint_id = sprint_id
    mock_sprint.__bool__ = Mock(return_value=True)

    mock_backlog_data = [
        (
            Mock(
                backlog_id=1,
                sprint_id=sprint_id,
                status='To Do',
                user_id=1
            ),
            Mock(user_name='User 1')
        ),
        (
            Mock(
                backlog_id=2,
                sprint_id=sprint_id,
                status='In Progress',
                user_id=2
            ),
            Mock(user_name='User 2')
        )
    ]

    with test_app.app_context():
        mock_project_query = Mock()
        mock_project_query.get.return_value = mock_project
        mocker.patch('views.scrum_view.Project.query', mock_project_query)

        mocker.patch('views.scrum_view.get_user_projects', return_value=[])
        mocker.patch('views.scrum_view.get_sprints_with_backlogs', return_value=mock_sprints)
        mock_sprint_query = Mock()
        mock_sprint_query.get.return_value = mock_sprint
        mocker.patch('views.scrum_view.Sprint.query', mock_sprint_query)

        # 'url_for' 패치
        mocker.patch('flask.url_for', side_effect=mock_url_for)

        mock_db_query = Mock()
        mock_db_query.join.return_value.filter.return_value.all.return_value = mock_backlog_data
        mocker.patch('views.scrum_view.db.session.query', return_value=mock_db_query)

        response = authenticated_user.get(f'/scrum/{project_id}?sprint_id={sprint_id}')

        assert response.status_code == 200

        response_data = response.get_data(as_text=True)
        assert 'To Do' in response_data
        assert 'In Progress' in response_data

def test_update_sprint_backlog_statuses(authenticated_user, test_app, mocker):
    """스프린트 백로그 상태 업데이트 API 테스트"""
    updated_backlogs = [
        {
            'backlog_id': 1,
            'new_status': 'Done'
        }
    ]

    with test_app.app_context():

        mock_backlog = Mock()
        mock_backlog.status = 'In Progress'
        mock_backlog.sprint_id = 1

        mock_sprintbacklog_query = Mock()
        mock_sprintbacklog_query.get.return_value = mock_backlog
        mocker.patch('views.scrum_view.SprintBacklog.query', mock_sprintbacklog_query)

        mock_sprint = Mock()
        mock_sprint.project_id = 1

        mock_sprint_query = Mock()
        mock_sprint_query.get.return_value = mock_sprint
        mocker.patch('views.scrum_view.Sprint.query', mock_sprint_query)

        mocker.patch('views.scrum_view.update_completed_backlog', return_value=True)
        mocker.patch('views.scrum_view.db.session.commit', return_value=None)
        mocker.patch('flask.url_for', side_effect=mock_url_for)

        response = authenticated_user.post('/scrum/update_sprint_backlog_statuses',
                                           json={'updated_backlogs': updated_backlogs},
                                           content_type='application/json')

        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response Data: {response.get_data(as_text=True)}"
        assert response.json['success'] is True