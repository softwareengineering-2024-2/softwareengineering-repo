from unittest.mock import Mock
from flask import json


def test_guide_view_authenticated(authenticated_user, mocker, test_app):
    """
    가이드 메인 페이지 렌더링 테스트: 인증된 사용자가 가이드 페이지에 접근할 수 있는지 확인.
    """
    project_id = 1

    # Mock 데이터 설정
    mock_project = Mock()
    mock_project.project_id = project_id
    mock_project.project_name = "Test Project"

    mock_user_project = Mock()
    mock_user_project.user_id = 1
    mock_user_project.project_id = project_id

    # Mock 메서드 설정
    mocker.patch('models.project_model.Project.find_by_id', return_value=mock_project)
    mocker.patch(
        'models.project_model.UserProject.find_by_user_and_project',
        return_value=mock_user_project
    )

    # 테스트 실행
    with test_app.app_context():
        response = authenticated_user.get(f'/guide/{project_id}')

        # 응답 상태 코드 검증
        assert response.status_code == 200

        # 응답 데이터에 가이드 텍스트 포함 여부 검증
        response_data = response.get_data(as_text=True)
        print("response_data:", response_data)
        assert "Test Project" in response_data
