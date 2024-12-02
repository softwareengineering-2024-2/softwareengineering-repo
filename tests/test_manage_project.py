from unittest.mock import Mock, patch
from models.project_model import Project, UserProject
from flask_login import current_user
from controllers.project_controller import create_project, join_project, get_user_projects, delete_project, set_profile, check_pm

MockProject = Mock()
MockUserProject = Mock()

def test_manage_project_view_authenticated(authenticated_user, mocker, test_app):
    """사용자가 인증된 상태에서 프로젝트 관리 뷰를 요청하는 테스트"""

    # Mock 설정
    mock_user_projects = [
        Mock(index=1, user_id="testuser", project_id=1, user_name="user1", user_role="PM(기획자)"),
        Mock(index=2, user_id="testuser", project_id=2, user_name="user1", user_role="Member"),
        Mock(index=3, user_id="testuser", project_id=3, user_name="user1", user_role="Member")
    ]
    mocker.patch('controllers.project_controller.get_user_projects', return_value=mock_user_projects)
       
    with test_app.app_context():
        response = authenticated_user.get(f'/manage_project/')
    
        # 디버깅용 출력
        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.get_data(as_text=True)}")
        
        # 인증 실패 여부 확인
        assert response.status_code == 200
        assert "프로젝트 목록" in response.get_data(as_text=True)

def test_create_project(authenticated_user, mocker, test_app):
    """프로젝트 생성 기능을 테스트"""
    form_data = {
        'project_name': 'New Project'
    }

    # Mock 설정
    mocker.patch('controllers.project_controller.create_project', return_value=(MockProject))
    
    with test_app.app_context():
        response = authenticated_user.post('/manage_project/create', data=form_data)

        # 디버깅용 출력
        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.get_data(as_text=True)}")

        assert response.status_code == 302
        assert '/manage_project/project_created' in response.headers['Location']

def test_render_link_check_view(authenticated_user, test_app):
    """링크 체크 페이지 렌더링을 테스트"""

    with test_app.app_context():
        response = authenticated_user.get('/manage_project/link_check')

        # 디버깅용 출력
        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.get_data(as_text=True)}")

        assert response.status_code == 200
        assert "프로젝트 참여코드" in response.get_data(as_text=True)

def test_project_created_view(authenticated_user, mocker, test_app):
    """프로젝트 생성 완료 뷰를 테스트"""
    
    # Mock 설정
    mock_project = Mock(project_id=1, project_name='New Project')
    mocker.patch('models.project_model.Project.find_by_id', return_value=mock_project)    
    
    with test_app.app_context():
        response = authenticated_user.get('/manage_project/project_created')

        # 디버깅용 출력
        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.get_data(as_text=True)}")

        assert response.status_code == 200
        assert "New Project" in response.get_data(as_text=True)

def test_link_check_view(authenticated_user, mocker, test_app):
    """프로젝트 링크 유효성 검사 기능을 테스트"""
    form_data = {
        'project_link': 'valid_link'
    }

    # Mock 설정
    mock_project = Mock(project_id=1, project_name='Valid Project')
    mocker.patch('models.project_model.Project.find_by_link', return_value=mock_project)
    
    with test_app.app_context():
        response = authenticated_user.post('/manage_project/link_check', data=form_data)

        assert response.status_code == 200
        assert "Valid Project" in response.get_data(as_text=True)

def test_join_project_view(authenticated_user, test_app):
    """프로젝트 참여 기능을 테스트"""

    with test_app.app_context():
        with authenticated_user.session_transaction() as session:
            session['project_id'] = 1

        with patch('controllers.project_controller.join_project', return_value=None):
            response = authenticated_user.post('/manage_project/join')

            assert response.status_code == 302
            assert '/manage_project/1/profile' in response.headers['Location']

def test_delete_project_view(authenticated_user, mocker, test_app):
    """프로젝트 삭제 기능을 테스트"""

    # Mock 설정
    mocker.patch('controllers.project_controller.delete_project', return_value=None)
    
    with test_app.app_context():
        test_app.config['SERVER_NAME'] = 'localhost'  # SERVER_NAME 설정
        with test_app.test_request_context():
            response = authenticated_user.post('/manage_project/1/delete')

        assert response.status_code == 302
        assert '/manage_project/' in response.headers['Location']

def test_render_set_profile_view(authenticated_user, mocker, test_app):
    """프로젝트 프로필 설정 페이지 렌더링을 테스트"""

    # Mock 설정
    mock_user_project = Mock(user_id='testuser', project_id=1, user_name='Test User', user_role='Member')
    mocker.patch('models.project_model.UserProject.find_by_user_and_project', return_value=mock_user_project)
    
    with test_app.app_context():
        response = authenticated_user.get('/manage_project/1/profile')

        # 디버깅용 출력
        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.get_data(as_text=True)}")

        assert response.status_code == 200
        assert "프로필 설정" in response.get_data(as_text=True)

def test_set_profile_view(authenticated_user, mocker, test_app):
    """사용자 프로필 설정 기능을 테스트"""
    form_data = {
        'name': 'Test User',
        'role': 'PM(기획자)'
    }

    # Mock 설정
    mock_user_project = Mock(user_id='testuser', project_id=1, user_name='Test User', user_role='Member')
    mocker.patch('models.project_model.UserProject.find_by_user_and_project', return_value=mock_user_project)
    
    
    mocker.patch('controllers.project_controller.check_pm', return_value=False)
    mocker.patch('controllers.project_controller.set_profile', return_value=None)
    
    with test_app.app_context():
        response = authenticated_user.post('/manage_project/1/profile', data=form_data)

        assert response.status_code == 302
        assert '/project_main/1' in response.headers['Location']

def test_set_profile_view_existing_pm(authenticated_user, mocker, test_app):
    """프로젝트에 이미 PM이 존재할 때 사용자 프로필 설정 기능을 테스트"""
    form_data = {
        'name': 'Test User',
        'role': 'PM(기획자)'
    }

    # Mock 설정
    mock_user_project_member = Mock(user_id='testuser', project_id=1, user_name='Test User', user_role='Member')
    mock_user_project_pm = Mock(user_id='pmuser', project_id=1, user_name='PM User', user_role='PM(기획자)')
    mock_project = Mock(project_id=1, project_name='Test Project')
    mocker.patch('models.project_model.UserProject.find_by_user_and_project', return_value=mock_user_project_member)
    mocker.patch('models.project_model.Project.find_by_id', return_value=mock_project)   
    mocker.patch('controllers.project_controller.check_pm', return_value=True)
    mocker.patch('models.project_model.UserProject.find_by_project', return_value=[mock_user_project_member, mock_user_project_pm])
    mocker.patch('controllers.project_controller.set_profile', return_value=None)

    with test_app.app_context():
        with patch('flask.render_template') as mock_render_template:
            mock_render_template.return_value = "프로젝트에 이미 PM이 존재합니다."
            response = authenticated_user.post(f'/manage_project/1/profile', data=form_data)

            # 디버깅용 출력
            print(f"Response status code: {response.status_code}")
            print(f"Response data: {response.get_data(as_text=True)}")

            # 테스트 검증
            assert response.status_code == 200  # 200 OK (렌더링된 페이지)
            assert "프로젝트에 이미 PM이 존재합니다." in response.get_data(as_text=True)
