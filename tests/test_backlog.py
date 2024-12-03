import json
from unittest.mock import patch, Mock

# Product Backlog 페이지 렌더링 테스트
def test_product_backlog_view_authenticated(authenticated_user, mocker, test_app):
    """
    Product Backlog 페이지 렌더링 테스트: 인증된 사용자가 페이지에 접근할 수 있는지 확인.
    """
    project_id = 1

    # Mock 설정
    mock_project = Mock()
    mock_project.project_id = project_id
    mock_user_project = Mock()
    mock_user_stories = [Mock(story_id=1, project_id=1), Mock(story_id=2, project_id=1)]
    mock_backlog_groups = [Mock(product_backlog_id=1), Mock(product_backlog_id=2)]

    mocker.patch('models.project_model.Project.find_by_id', return_value=mock_project)
    mocker.patch('models.project_model.UserProject.find_by_user_and_project', return_value=mock_user_project)
    mocker.patch('controllers.productbacklog_controller.get_user_stories', return_value=mock_user_stories)
    mocker.patch('models.productbacklog_model.ProductBacklog.query.filter_by', return_value=mock_backlog_groups)

    with test_app.app_context():
        response = authenticated_user.get(f'/productbacklog/{project_id}')

        # 검증
        assert response.status_code == 200
        assert 'backlog' in response.get_data(as_text=True)

# 새로운 백로그 그룹 생성 또는 업데이트 테스트
def test_create_or_update_backlog_group(authenticated_user, mocker, test_app):
    """
    새로운 백로그 그룹 생성 또는 업데이트 API 테스트: 성공적으로 백로그 그룹이 생성되거나 업데이트되는지 확인.
    """
    # 테스트용 데이터 설정
    form_data = {
        "group_name": "New Group",
        "story_ids": ["1", "2", "3"],
        "backlog_id": "5"  # 기존 백로그 ID (없으면 None)
    }

    # Mock create_or_update_product_backlog_group 함수
    mock_create_or_update = mocker.patch(
        'views.productbacklog_view.create_or_update_product_backlog_group',
        return_value=10  # 새로운 product_backlog_id 반환
    )

    # Flask 애플리케이션 컨텍스트 내에서 테스트 실행
    with test_app.app_context():
        response = authenticated_user.post(
            '/productbacklog/create_or_update_group',
            data=form_data,
            content_type='application/x-www-form-urlencoded'  # Form 데이터 전송
        )

        # 응답 데이터 확인
        response_data = json.loads(response.get_data(as_text=True))

        # 검증
        assert response.status_code == 200
        assert response_data['success'] is True
        assert response_data['product_backlog_id'] == 10

        # Mock 함수 호출 확인
        mock_create_or_update.assert_called_once_with(
            form_data["group_name"],
            form_data["story_ids"],
            int(form_data["backlog_id"])  # backlog_id는 int로 변환
        )

# 유저스토리 이동 테스트
def test_move_user_story(authenticated_user, mocker, test_app):
    form_data = {"story_id": "1", "backlog_id": "2"}
    mock_update = mocker.patch('views.productbacklog_view.update_product_backlog', return_value=True)

    with test_app.app_context():
        response = authenticated_user.post(
            '/productbacklog/move',
            data=form_data,
            content_type='application/x-www-form-urlencoded'
        )
        response_data = json.loads(response.get_data(as_text=True))

        # 검증
        assert response.status_code == 200
        assert response_data['success'] is True
        mock_update.assert_called_with("1", "2")

# 백로그 그룹 저장 테스트
def test_save_backlog_groups(authenticated_user, mocker, test_app):
    """
    백로그 그룹 저장 API 테스트: 올바른 데이터를 받아 백로그 그룹이 성공적으로 저장되는지 확인.
    """
    form_data = {
        "backlogGroups": [
            {"backlogName": "Group 1", "storyIds": [1, 2]},
            {"backlogName": "Group 2", "storyIds": [3]}
        ],
        "unassignedStoryIds": [4, 5]  # 테스트 데이터
    }

    # Mock save_all_backlog_groups
    mock_save_all_backlog_groups = mocker.patch(
        'views.productbacklog_view.save_all_backlog_groups',
        return_value=True  # 저장 성공 시 True 반환
    )

    with test_app.app_context():
        response = authenticated_user.post(
            '/productbacklog/save_groups',
            data=json.dumps(form_data),  # JSON 데이터로 전달
            content_type='application/json'
        )

        # 응답 데이터 확인
        response_data = json.loads(response.get_data(as_text=True))

        # 검증
        assert response.status_code == 200
        assert response_data['success'] is True

        # Mock 호출 검증
        mock_save_all_backlog_groups.assert_called_once_with(
            form_data['backlogGroups'],
            form_data['unassignedStoryIds']
        )

def test_delete_backlog_view(authenticated_user, mocker, test_app):
    """
    백로그 삭제 API 테스트: 특정 ID의 백로그가 성공적으로 삭제되는지 확인.
    """
    # 테스트용 백로그 ID
    backlog_id = 1

    # Mock delete_product_backlog 함수
    mock_delete_product_backlog = mocker.patch(
        'views.productbacklog_view.delete_product_backlog',
        return_value=True  # 삭제 성공 시 True 반환
    )

    with test_app.app_context():
        # DELETE 요청
        response = authenticated_user.delete(f'/productbacklog/delete/{backlog_id}')

        # 응답 데이터 확인
        response_data = json.loads(response.get_data(as_text=True))

        # 검증
        assert response.status_code == 200
        assert response_data['success'] is True

        # Mock 호출 확인
        mock_delete_product_backlog.assert_called_once_with(backlog_id)

# 백로그 박스 순서 저장 테스트
def test_save_backlog_order_view(authenticated_user, mocker, test_app):
    """
    백로그 박스 순서 저장 API 테스트.
    """
    form_data = {
        "backlogOrderList": [1, 2, 3]
    }
    mocker.patch('controllers.productbacklog_controller.save_backlog_order', return_value=True)

    with test_app.app_context():
        response = authenticated_user.post(
            '/productbacklog/save_order',
            data=json.dumps(form_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data(as_text=True))

        # 검증
        assert response.status_code == 200
        assert response_data['success'] is True
