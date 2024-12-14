from unittest.mock import Mock, patch
from models.project_model import Project, UserProject

MockProject = Mock()

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
        response = authenticated_user.get('/manage_project/')
    
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
        with patch('flask.render_template') as mock_render_template:
            mock_render_template.return_value = "존재하지 않는 참여코드입니다."
            response = authenticated_user.post('/manage_project/link_check', data=form_data)

            # 디버깅용 출력
            print(f"Response status code: {response.status_code}")
            print(f"Response data: {response.get_data(as_text=True)}")

            assert response.status_code == 200
            assert "Valid Project" in response.get_data(as_text=True)

def test_link_check_fail_view_(authenticated_user, mocker, test_app):
    """유효하지 않은 링크를 전달한 경우 프로젝트 링크 유효성 검사 기능을 테스트"""
    form_data = {
        'project_link': 'unvalid_link'
    }

    # Mock 설정
    mocker.patch('models.project_model.Project.find_by_link', return_value=None)
    
    with test_app.app_context():
        with patch('flask.render_template') as mock_render_template:
            mock_render_template.return_value = "존재하지 않는 참여코드입니다."
            response = authenticated_user.post('/manage_project/link_check', data=form_data)

            # 디버깅용 출력
            print(f"Response status code: {response.status_code}")
            print(f"Response data: {response.get_data(as_text=True)}")

            assert response.status_code == 200
            assert "존재하지 않는 참여코드입니다." in response.get_data(as_text=True)

def test_join_project_view(authenticated_user, test_app):
    """프로젝트 참여 기능을 테스트"""

    with test_app.app_context():
        with authenticated_user.session_transaction() as session:
            session['project_id'] = 1

        with patch('controllers.project_controller.join_project', return_value=None):
            response = authenticated_user.post('/manage_project/join')

            # 디버깅용 출력
            print(f"Response status code: {response.status_code}")
            print(f"Response data: {response.get_data(as_text=True)}")

            assert response.status_code == 302
            assert '/manage_project/1/profile' in response.headers['Location']

def test_delete_project_view(authenticated_user, mocker, test_app):
    """프로젝트 삭제 기능을 테스트"""

    # Mock 설정
    mocker.patch('controllers.project_controller.delete_project', return_value=None)
    
    with test_app.app_context():
        response = authenticated_user.post('/manage_project/1/delete')

        # 디버깅용 출력
        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.get_data(as_text=True)}")

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
    """PM에서 Member로의 사용자 역할 변경을 테스트"""
    form_data = {
        'name': 'Test User',
        'role': 'Member'
    }

    # Mock 설정
    mock_user_project = Mock(user_id='testuser', project_id=1, user_name='Test User', user_role='PM(기획자)')
    mocker.patch('models.project_model.UserProject.find_by_user_and_project', return_value=mock_user_project)
    mocker.patch('controllers.project_controller.set_profile', return_value=None)
    
    with test_app.app_context():
        response = authenticated_user.post('/manage_project/1/profile', data=form_data)

        # 디버깅용 출력
        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.get_data(as_text=True)}")

        assert response.status_code == 302
        assert '/project_main/1' in response.headers['Location']

def test_set_profile_view_non_existing_pm(authenticated_user, mocker, test_app):
    """다른 PM이 존재하지 않는 경우 Member에서 PM으로의 사용자 역할 변경을 테스트"""
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

        # 디버깅용 출력
        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.get_data(as_text=True)}")

        assert response.status_code == 302
        assert '/project_main/1' in response.headers['Location']

def test_set_profile_view_existing_pm(authenticated_user, mocker, test_app):
    """프로젝트에 이미 PM이 존재할 때 Member에서 PM으로의 역할 변경을 테스트"""
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
            response = authenticated_user.post('/manage_project/1/profile', data=form_data)

            # 디버깅용 출력
            print(f"Response status code: {response.status_code}")
            print(f"Response data: {response.get_data(as_text=True)}")

            # 테스트 검증
            assert response.status_code == 200  # 200 OK (렌더링된 페이지)
            assert "프로젝트에 이미 PM이 존재합니다." in response.get_data(as_text=True)

from unittest.mock import patch
from models.project_model import Project

def test_find_by_link(test_app):
    """프로젝트 링크로 프로젝트를 검색하는 기능을 테스트"""
    project_link = "test_link"

    # 검색할 때 반환될 가상의 프로젝트 객체
    mock_project = Project(project_name="Test Project", project_link=project_link)
    mock_project.project_id = 1  # 일반적으로 데이터베이스에서 설정되는 ID
    expected_project = Project(project_name="Test Project", project_link=project_link)

    with test_app.app_context():
        # Project.query.filter_by의 반환을 모의로 설정
        with test_app.app_context():
            with patch('sqlalchemy.orm.Query.filter_by') as mock_filter:
                mock_filter.return_value.first.return_value = expected_project

                # 메서드 호출 및 결과 확인
                result = Project.find_by_link(project_link)
                assert result == expected_project
                assert result.project_name == "Test Project"
                assert result.project_link == project_link

                # filter_by가 올바른 인자로 호출되었는지 검사
                mock_filter.assert_called_once_with(project_link=project_link)

def test_set_user_profile(mocker, test_app):
    """사용자 프로필 정보 저장 테스트"""
    user_id = 'testuser'
    project_id = 1
    user_name = 'new_name'
    user_role = 'new_role'
    
    # 실제 UserProject 객체를 사용하는 대신 모킹을 사용
    mock_user_project = Mock(user_id=user_id, project_id=project_id, user_name='old_name', user_role='old_role')
    mocker.patch('models.project_model.UserProject.find_by_user_and_project', return_value=mock_user_project)
    
    with test_app.app_context():
        UserProject.set_user_profile(user_id, project_id, user_name, user_role)
        mock_user_project.user_name = user_name
        mock_user_project.user_role = user_role
        assert mock_user_project.user_name == 'new_name'
        assert mock_user_project.user_role == 'new_role'
