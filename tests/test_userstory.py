from unittest.mock import Mock
import pytest

def assert_redirect_to_userstory(response, project_id):
    """리다이렉션 검증 헬퍼 함수"""
    assert response.status_code == 302
    assert f'/userstory/{project_id}' in response.headers['Location']


def test_create_story_route(authenticated_user, mocker, test_app):
    """유저스토리 작성 기능 테스트"""
    mocker.patch('controllers.userstory_controller.create_story', return_value=None)

    form_data = {'content': 'New User Story'}
    project_id = 1

    with test_app.app_context():
        response = authenticated_user.post(f'/userstory/{project_id}', data=form_data)
        assert_redirect_to_userstory(response, project_id)


def test_update_story_route(authenticated_user, mocker, test_app):
    """유저스토리 수정 기능 테스트"""

    mock_userstory = Mock()
    mock_userstory.story_id = 1
    mock_userstory.user_story_content = 'Updated User Story'
    mock_userstory.product_backlog_id = None

    mocker.patch('controllers.userstory_controller.update_story', return_value=mock_userstory)

    form_data = {'content': 'Updated User Story'}
    project_id= 1
    story_id = 1

    with test_app.app_context():
        response = authenticated_user.post(f'/userstory/{project_id}/{story_id}', data=form_data)
        assert_redirect_to_userstory(response, project_id)


def test_delete_story_route(authenticated_user, mocker, test_app):
    """유저스토리 삭제 기능 테스트"""
    mocker.patch('controllers.userstory_controller.delete_story', return_value=None)

    project_id, story_id = 1, 1

    with test_app.app_context():
        response = authenticated_user.post(f'/userstory/{project_id}/{story_id}/delete')
        assert_redirect_to_userstory(response, project_id)


def test_create_keywords_route(authenticated_user, mocker, test_app):
    """키워드 추가 기능 테스트"""
    mocker.patch('controllers.notlist_controller.create_keywords', return_value=None)

    form_data = {'keyword': 'test_keyword'}
    project_id = 1

    with test_app.app_context():
        response = authenticated_user.post(f'/userstory/notlist/{project_id}', data=form_data)
        assert_redirect_to_userstory(response, project_id)


def test_delete_keyword_route(authenticated_user, mocker, test_app):
    """키워드 삭제 기능 테스트"""
    mocker.patch('controllers.notlist_controller.delete_keyword', return_value=None)

    project_id, not_list_id = 1, 1

    with test_app.app_context():
        response = authenticated_user.post(f'/userstory/notlist/{project_id}/{not_list_id}/delete')
        assert_redirect_to_userstory(response, project_id)

def test_save_alert_to_db(authenticated_user, mocker, test_app):
    """알림 저장 기능 테스트"""
    
    # mock 객체 설정: Project 객체처럼 행동하게끔 mock
    mock_project = Mock()
    mock_project.project_name = "Test Project"
    
    # filter_by().first() 호출 시 mock_project를 반환하도록 설정
    mock_project_query = Mock()
    mock_project_query.filter_by.return_value.first.return_value = mock_project

    # filter_by 메소드가 mock_project_query를 반환하도록 모킹
    mocker.patch('models.project_model.Project.query', mock_project_query)
    
    # 알림 저장 함수 모킹
    mocker.patch('controllers.alert_controller.save_alert', return_value=None)
    
    # get_project_name 함수 모킹
    mocker.patch('controllers.alert_controller.get_project_name', return_value="Test Project")

    # 알림 데이터 설정
    alert_data = {"project_id": 1, "message": "Test Alert"}
    
    # 예상되는 결과 값 설정
    expected_result = {
        'status': 'success',
        'message': 'Message sent to PM'
    }

    # 실제 요청 시나리오 실행
    with test_app.app_context():
        response = authenticated_user.post('/userstory/alert/save_alert_to_db', json=alert_data)
        
        # 성공적인 응답 검증
        assert response.status_code == 200
        assert response.json == expected_result


# get_alerts 테스트
def test_get_messages(authenticated_user, mocker, test_app):
    """알림 조회 기능 테스트"""

    # mock 객체 설정: Project 객체처럼 행동하게끔 mock
    mock_project = Mock()
    mock_project.project_name = "Test Project"
    # filter_by().first() 호출 시 mock_project를 반환하도록 설정
    mock_project_query = Mock()
    mock_project_query.filter_by.return_value.first.return_value = mock_project

    # mock 객체 설정: 알림 데이터
    mock_alerts = Mock()
    mock_alerts.user_id = "testuser"
    mock_alerts.project_id = 1
    mock_alerts.user_role = 'PM(기획자)'  # PM 역할 설정
    mock_alerts.content = 'Test Alert'
    
    # mock_alert을 리스트로 설정
    expected_result = [{'content': f' 프로젝트[{mock_project.project_name}] : 해당 프로젝트에 {mock_alerts.content}'}]

    # mock_user_project 설정: UserProject 객체
    mock_user_project = Mock()
    mock_user_project.user_role = 'PM(기획자)'  # UserProject의 역할 설정

    # UserProject 쿼리 모킹: filter_by().first()가 mock_user_project를 반환하도록 설정
    mock_user_project_query = Mock()
    mock_user_project_query.filter_by.return_value.first.return_value = mock_user_project
    mocker.patch('models.project_model.UserProject.query', mock_user_project_query)

    # 알림 조회 함수 모킹: get_alerts가 mock_alert를 반환하도록 설정
    mocker.patch('controllers.alert_controller.get_alerts', return_value=expected_result)

    # 실제 요청 시나리오 실행
    with test_app.app_context():
        response = authenticated_user.get('/userstory/get_alerts/1')
        # 성공적인 응답 검증
        assert response.status_code == 200
        assert response.json == expected_result  # mock_alert를 그대로 응답으로 비교