from unittest.mock import patch, Mock
from flask import json

def assert_redirect_to_userstory(response, project_id):
    """리다이렉션 검증 헬퍼 함수"""
    assert response.status_code == 302
    assert f'/userstory/{project_id}' in response.headers['Location']



def test_create_story_authenticated(authenticated_user, mocker, test_app):
    """유저스토리 작성 테스트"""
    project_id = 1
    form_data = {"content": "New User Story"}

    # Mock 설정
    mocker.patch('controllers.userstory_controller.create_story', return_value=None)

    with test_app.app_context():
        response = authenticated_user.post(
            f'/userstory/{project_id}', data=form_data
        )
        assert_redirect_to_userstory(response, project_id)

def test_update_story_authenticated(authenticated_user, mocker, test_app):
    """유저스토리 수정 테스트"""
    project_id, story_id = 1, 1
    form_data = {"content": "Updated Story"}

    # Mock 설정
    mocker.patch('controllers.userstory_controller.update_story', return_value=None)

    with test_app.app_context():
        response = authenticated_user.post(
            f'/userstory/{project_id}/{story_id}', data=form_data
        )
        assert_redirect_to_userstory(response, project_id)

def test_create_keyword_authenticated(authenticated_user, mocker, test_app):
    """키워드 추가 테스트"""
    project_id = 1
    form_data = {"keyword": "New Keyword"}

    # Mock 설정
    mocker.patch('controllers.notlist_controller.create_keywords', return_value=None)

    with test_app.app_context():
        response = authenticated_user.post(
            f'/userstory/notlist/{project_id}', data=form_data
        )
        assert_redirect_to_userstory(response, project_id)


def test_view_stories_authenticated(authenticated_user, mocker, test_app):
    """유저스토리 목록 보기 테스트"""
    project_id = 1

    # Mock 데이터 설정
    mock_stories = [{"id": 1, "content": "Story 1"}]
    mock_notlist = [{"id": 1, "keyword": "Keyword 1"}]

    # Mock 객체 생성 및 속성 설정
    mock_project = Mock()
    mock_project.project_id = project_id

    mock_user_project = Mock()

    # Mock 함수 패치
    mocker.patch('controllers.userstory_controller.show_stories', return_value=mock_stories)
    mocker.patch('controllers.notlist_controller.show_notlist', return_value=mock_notlist)
    mocker.patch('models.project_model.Project.find_by_id', return_value=mock_project)
    mocker.patch('models.project_model.UserProject.find_by_user_and_project', return_value=mock_user_project)

    # 테스트 실행
    with test_app.app_context():
        response = authenticated_user.get(f'/userstory/{project_id}')
        response_data =response.get_data(as_text=True)
        print("response_data: ", response_data)

        assert response.status_code == 200
        assert "Updated Story" in response.get_data(as_text=True)
        assert "New Keyword" in response.get_data(as_text=True)

def test_delete_story_authenticated(authenticated_user, mocker, test_app):
    """유저스토리 삭제 테스트"""
    project_id, story_id = 1, 1

    # Mock 설정
    mocker.patch('controllers.userstory_controller.delete_story', return_value=None)

    with test_app.app_context():
        response = authenticated_user.post(f'/userstory/{project_id}/{story_id}/delete')
        assert_redirect_to_userstory(response, project_id)


def test_delete_keyword_authenticated(authenticated_user, mocker, test_app):
    """키워드 삭제 테스트"""
    project_id, keyword_id = 1, 1

    # Mock 설정
    mocker.patch('controllers.notlist_controller.delete_keyword', return_value=None)

    with test_app.app_context():
        response = authenticated_user.post(f'/userstory/notlist/{project_id}/{keyword_id}/delete')
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