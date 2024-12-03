from unittest.mock import patch, Mock, MagicMock


def mock_url_for(endpoint, **values):
    """특정 엔드포인트를 처리하기 위한 mock된 url_for 함수"""
    if endpoint == 'retrospect.retrospect_view':
        return f"/retrospect/{values.get('project_id')}"
    return f"/{endpoint}/" + "/".join(str(v) for v in values.values())

# 회고 생성 테스트
def test_create_retrospect(authenticated_user, mocker, test_app):
    """
    회고 생성 테스트: 올바른 데이터를 받아 회고가 성공적으로 생성되는지 확인.
    """

    project_id = 1
    form_data = {
        "user_id": 1,
        "project_id": 1,
        "sprint_id": 1,
        "retrospect_title": "Sprint 1 회고",
        "retrospect_content": "이번 Sprint에서 배운 점과 개선할 점",
        "label": "retrospect",
        "file_link": None
    }
    file_mock = Mock()
    mocker.patch('controllers.retrospect_controller.handle_file_upload', return_value=file_mock)
    mocker.patch('controllers.retrospect_controller.create_retrospect', return_value=True)

    with test_app.app_context():
        response = authenticated_user.post(
            f'/retrospect/{project_id}/create',
            data=form_data,
            content_type='multipart/form-data'
        )
        assert response.status_code == 302  # 리다이렉트 확인
        assert f'/retrospect/{project_id}' in response.location
    # mocker.resetall()

def test_view_retrospect_view(authenticated_user, mocker, test_app):
    """
    회고 조회 View에 대한 테스트: 데이터 조회 및 템플릿 렌더링 확인.
    """
    project_id = 1
    retrospect_id = 1

    # Mock 데이터 설정
    mock_project = Mock(project_id=project_id, project_name="Test Project")
    mock_retrospect = Mock(
        retrospect_id=retrospect_id,
        retrospect_title="Sprint 1 회고",
        retrospect_content="이번 Sprint에서 배운 점과 개선할 점",
        sprint_id=1,
        label="retrospect",
    )
    mock_user_project = Mock(user_id=1, user_role="PM(기획자)")

    # Mock 설정
    mock_query = Mock()
    mock_query.get_or_404.return_value = mock_project
    mocker.patch('models.project_model.Project.query', mock_query)
    mocker.patch('controllers.retrospect_controller.get_retrospect_by_id', return_value=mock_retrospect)
    mocker.patch('controllers.retrospect_controller.get_sprints', return_value=[Mock(sprint_id=1, sprint_name="Sprint 1")])
    mocker.patch('controllers.retrospect_controller.get_user_name_by_project_and_user', return_value="Test User")
    mocker.patch('drive.drive_init.extract_file_id', return_value="12345")
    mocker.patch('drive.drive_init.get_file_name', return_value="Test File")
    mocker.patch('models.project_model.UserProject.find_by_user_and_project', return_value=mock_user_project)

    # 인증된 사용자 세션 설정
    with authenticated_user.session_transaction() as session:
        session['_user_id'] = 1
        session['_fresh'] = True

    # GET 요청 수행
    response = authenticated_user.get(f'/retrospect/{project_id}/view/{retrospect_id}')

    # 상태 코드 검증
    assert response.status_code == 200

    # 반환된 HTML 검증
    response_data = response.get_data(as_text=True)
    print(response_data)
    # 템플릿 내 Mock 데이터 확인
    assert "Sprint 1 회고" in response_data  # 제목 확인
    assert "Sprint 1" in response_data  # 스프린트 확인
    assert "회고" in response_data  # 카테고리 확인
    assert "이번 Sprint에서 배운 점과 개선할 점" in response_data  # 내용 확인
    assert "목록으로 돌아가기" in response_data  # 버튼 텍스트 확인




def test_retrospect_view_authenticated(authenticated_user, mocker, test_app):
    """
    회고 관리 페이지 렌더링 테스트: 인증된 사용자가 회고 페이지에 접근할 수 있는지 확인.
    """
    project_id = 1

    # Mock Project 객체 생성
    mock_project = Mock()
    mock_project.project_id = project_id
    mock_project.project_name = "Test Project"

    # Mock UserProject 객체 생성
    mock_user_project = Mock()
    mock_user_project.user_id = 1
    mock_user_project.project_id = project_id
    mock_user_project.user_name = "Test User"

    mock_query = Mock()
    mock_query.get_or_404.return_value = mock_project  # get_or_404 반환값 설정
    mock_query.filter_by.return_value.first.return_value = mock_project  # filter_by().first() 반환값 설정

    # Project.query를 mock_query로 모킹
    mocker.patch('models.project_model.Project.query', mock_query)
    mocker.patch('controllers.retrospect_controller.get_sprints', return_value=[])
    mocker.patch('controllers.retrospect_controller.get_filtered_retrospects', return_value=Mock(items=[]))
    mocker.patch('models.project_model.UserProject.query.filter_by', return_value=Mock(all=lambda: [mock_user_project]))

    # 테스트 실행
    with test_app.app_context():
        response = authenticated_user.get(f'/retrospect/{project_id}')
        print(response.get_data(as_text=True))

        # 응답 상태 코드 확인
        assert response.status_code == 200

        assert 'Test Project' in response.get_data(as_text=True)

        # 응답 데이터에 "회고 등록" 텍스트 포함 확인
        assert '회고 등록' in response.get_data(as_text=True)

# 회고 수정 테스트
def test_edit_retrospect(authenticated_user, mocker, test_app):
    """
    회고 수정 테스트: 올바른 데이터를 받아 회고가 성공적으로 수정되는지 확인.
    """
    project_id = 1
    retrospect_id = 1
    form_data = {
        "sprint_id": 1,
        "retrospect_title": "수정된 회고 제목",
        "retrospect_content": "수정된 내용",
        "label": "risk",
    }

    # Mock current_user
    mocker.patch('flask_login.current_user', Mock(id=1, is_authenticated=True))

    retrospect_mock = Mock(user_id=1, file_link="mock_file_link")
    mocker.patch('models.retrospect_model.Retrospect.query.get_or_404', return_value=retrospect_mock)
    mocker.patch('controllers.retrospect_controller.update_retrospect', return_value=True)
    mocker.patch('controllers.retrospect_controller.handle_file_upload', return_value="mock_file_link_updated")

    with test_app.app_context():
        response = authenticated_user.post(
            f'/retrospect/{project_id}/edit/{retrospect_id}',
            data=form_data,
            content_type='multipart/form-data'
        )
        assert response.status_code == 302  # 리다이렉트 확인
        assert f'/retrospect/{project_id}' in response.location

def test_delete_retrospect(authenticated_user, mocker, test_app):
    """
    회고 삭제 테스트: 특정 회고가 성공적으로 삭제되는지 확인.
    """
    project_id = 1
    retrospect_id = 1

    # Mock current_user
    mocker.patch('flask_login.current_user', Mock(id=1, is_authenticated=True))

    # Mock 설정
    retrospect_mock = Mock(user_id=1)
    mocker.patch('models.retrospect_model.Retrospect.query.get_or_404', return_value=retrospect_mock)
    mocker.patch('controllers.retrospect_controller.delete_retrospect', return_value=True)

    with test_app.app_context():
        test_app.debug = True  # Debug 활성화
        response = authenticated_user.post(f'/retrospect/{project_id}/delete/{retrospect_id}')
        assert response.status_code == 302
        assert f'/retrospect/{project_id}' in response.location

def test_retrospect_view_no_retrospects(authenticated_user, mocker, test_app):
    """
    회고가 없는 프로젝트 페이지가 빈 상태로 로드되는지 확인.
    """
    project_id = 1

    mock_project = Mock(project_id=project_id, project_name="Test Project")
    mock_user_project = Mock(user_id=1, user_name="Test User")

    mock_query = Mock()
    mock_query.get_or_404.return_value = mock_project
    mocker.patch('models.project_model.Project.query', mock_query)
    mocker.patch('controllers.retrospect_controller.get_filtered_retrospects', return_value=Mock(items=[]))
    mocker.patch('models.project_model.UserProject.query.filter_by', return_value=Mock(all=lambda: [mock_user_project]))

    with test_app.app_context():
        response = authenticated_user.get(f'/retrospect/{project_id}')
        assert response.status_code == 200
        assert '아직 생성된 회고가 없습니다.' in response.get_data(as_text=True)

def test_get_edit_retrospect_view_invalid_retrospect(authenticated_user, mocker, test_app):
    """
    잘못된 회고 ID로 수정 페이지에 접근할 때 404 반환 확인.
    """
    project_id = 1
    retrospect_id = 999  # 존재하지 않는 회고 ID

    mock_query = Mock()
    mock_query.get_or_404.side_effect = Exception("404 Not Found")
    mocker.patch('models.retrospect_model.Retrospect.query', mock_query)

    with test_app.app_context():
        response = authenticated_user.get(f'/retrospect/{project_id}/edit/{retrospect_id}')
        assert response.status_code == 404


def test_edit_retrospect_view_unauthorized_user(authenticated_user, mocker, test_app):
    """
    권한 없는 사용자가 회고를 수정하려 할 때 리다이렉트 확인.
    """
    project_id = 1
    retrospect_id = 1

    mock_retrospect = Mock(user_id=2)  # 다른 사용자가 작성한 회고
    mock_query = Mock()
    mock_query.get_or_404.return_value = mock_retrospect
    mocker.patch('models.retrospect_model.Retrospect.query', mock_query)

    with test_app.app_context():
        response = authenticated_user.post(
            f'/retrospect/{project_id}/edit/{retrospect_id}',
            data={},
            content_type='multipart/form-data'
        )
        assert response.status_code == 302
        assert f'/retrospect/{project_id}' in response.location

def test_get_create_retrospect_view_invalid_project(authenticated_user, mocker, test_app):
    """
    잘못된 프로젝트 ID로 회고 생성 페이지에 접근할 때 404 반환 확인.
    """
    project_id = 999  # 존재하지 않는 프로젝트 ID

    mocker.patch('models.project_model.Project.query.get_or_404', side_effect=Exception("404 Not Found"))

    with test_app.app_context():
        response = authenticated_user.get(f'/retrospect/{project_id}/create')
        assert response.status_code == 404

def test_get_edit_retrospect_view_invalid_retrospect(authenticated_user, mocker, test_app):
    """
    잘못된 회고 ID로 수정 페이지에 접근할 때 404 반환 확인.
    """
    project_id = 1
    retrospect_id = 999  # 존재하지 않는 회고 ID
    mocker.patch('models.retrospect_model.Retrospect.query.get_or_404', side_effect=Exception("404 Not Found"))

    with test_app.app_context():
        response = authenticated_user.get(f'/retrospect/{project_id}/edit/{retrospect_id}')
        assert response.status_code == 404

def test_view_retrospect_invalid_id(authenticated_user, mocker, test_app):
    """
    잘못된 회고 ID로 조회하려 할 때 404 반환 확인.
    """
    project_id = 1
    retrospect_id = 999  # 존재하지 않는 회고 ID
    mocker.patch('controllers.retrospect_controller.get_retrospect_by_id', side_effect=Exception("404 Not Found"))

    with test_app.app_context():
        response = authenticated_user.get(f'/retrospect/{project_id}/view/{retrospect_id}')
        assert response.status_code == 404

def test_delete_retrospect_view_unauthorized_user(authenticated_user, mocker, test_app):
    """
    권한 없는 사용자가 회고를 삭제하려 할 때 리다이렉트 확인.
    """
    project_id = 1
    retrospect_id = 1

    mock_retrospect = Mock(user_id=2)  # 다른 사용자가 작성한 회고
    mock_query = Mock()
    mock_query.get_or_404.return_value = mock_retrospect
    mocker.patch('models.retrospect_model.Retrospect.query', mock_query)

    with test_app.app_context():
        response = authenticated_user.post(f'/retrospect/{project_id}/delete/{retrospect_id}')
        assert response.status_code == 302
        assert f'/retrospect/{project_id}' in response.location
