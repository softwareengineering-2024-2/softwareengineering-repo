import json
from unittest.mock import patch, Mock
from controllers.productbacklog_controller import (
    get_user_stories, 
    update_product_backlog, 
    save_all_backlog_groups, 
    delete_product_backlog, 
    save_backlog_order
)

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

# 특정 프로젝트의 유저스토리 목록 가져오기 테스트
def test_get_user_stories(authenticated_user, mocker, test_app):
    """
    특정 프로젝트의 유저스토리 목록을 올바르게 가져오는지 확인.
    """
    project_id = 1
    mock_user_stories = [
        Mock(story_id=1, project_id=1, story_content="User Story 1"),
        Mock(story_id=2, project_id=1, story_content="User Story 2")
    ]
    mock_query = Mock()
    mock_query.filter_by.return_value.order_by.return_value.all.return_value = mock_user_stories
    mocker.patch('models.userstory_model.UserStory.query', mock_query)

    with test_app.app_context():
        result = get_user_stories(project_id)
        assert len(result) == 2
        assert result[0].story_id == 1
        assert result[1].story_id == 2

# 유저스토리를 지정된 백로그로 이동 테스트
def test_update_product_backlog(authenticated_user, mocker, test_app):
    """
    유저스토리를 특정 백로그에 추가하는 기능 테스트.
    """
    story_id = 1
    backlog_id = 2
    
    # Mock UserStory 객체 생성
    mock_user_story = Mock(story_id=story_id, product_backlog_id=None)
    
    # Mock UserStory.query.get() 반환값 설정
    mock_query = Mock()
    mock_query.get.return_value = mock_user_story
    mocker.patch('models.userstory_model.UserStory.query', mock_query)
    
    # Mock db.session.commit()
    mock_commit = mocker.patch('database.db.session.commit', return_value=None)
    
    with test_app.app_context():
        result = update_product_backlog(story_id, backlog_id)
        
        # 검증
        assert result is True
        assert mock_user_story.product_backlog_id == backlog_id  # 업데이트 확인
        mock_commit.assert_called_once()  # 커밋 호출 확인

# 빈 백로그 삭제 테스트
def test_delete_empty_backlogs(authenticated_user, mocker, test_app):
    """
    유저스토리가 없는 빈 백로그를 삭제하는 테스트.
    """
    # Mock ProductBacklog 데이터
    mock_backlogs = [
        Mock(product_backlog_id=1, project_id=1),
        Mock(product_backlog_id=2, project_id=1)
    ]

    # Mock UserStory 데이터: 모든 백로그가 빈 상태로 설정
    mock_user_stories = []

    # Mock 설정
    mock_product_backlog_query = Mock()
    mock_product_backlog_query.filter.return_value.all.return_value = mock_backlogs
    mocker.patch('models.productbacklog_model.ProductBacklog.query', mock_product_backlog_query)

    mock_user_story_query = Mock()
    mock_user_story_query.filter_by.return_value.all.return_value = mock_user_stories
    mocker.patch('models.userstory_model.UserStory.query', mock_user_story_query)

    mock_db_session = mocker.patch('database.db.session')

    with test_app.app_context():
        success = save_all_backlog_groups([], [])  # 빈 백로그를 처리하기 위해 빈 데이터 전달
        assert success is True  # 함수가 성공적으로 실행되었는지 확인

        # Mock 호출 확인
        assert mock_db_session.delete.call_count == len(mock_backlogs)  # 모든 빈 백로그가 삭제되었는지 확인
        for backlog in mock_backlogs:
            mock_db_session.delete.assert_any_call(backlog)  # 각 백로그가 삭제되었는지 확인

# 백로그 삭제 실패 테스트
def test_delete_product_backlog_fail(authenticated_user, mocker, test_app):
    """
    존재하지 않는 백로그를 삭제하려고 할 때 False 반환 테스트.
    """
    backlog_id = 999  # 존재하지 않는 백로그 ID

    # Mock 설정
    mock_product_backlog_query = Mock()
    mock_product_backlog_query.get.return_value = None  # 존재하지 않는 백로그를 반환
    mocker.patch('models.productbacklog_model.ProductBacklog.query', mock_product_backlog_query)

    with test_app.app_context():
        result = delete_product_backlog(backlog_id)

        # 검증
        assert result is None  # 함수가 None을 반환해야 함

# 백로그 순서 저장 실패 테스트
def test_save_backlog_order_fail(authenticated_user, mocker, test_app):
    """
    유효하지 않은 백로그 ID로 순서 저장 시도.
    """
    # Mock 설정
    mock_product_backlog_query = Mock()
    mock_product_backlog_query.get.return_value = None  # 존재하지 않는 백로그 반환
    mocker.patch('models.productbacklog_model.ProductBacklog.query', mock_product_backlog_query)

    # Mock db.session
    mock_db_session = mocker.patch('database.db.session')

    with test_app.app_context():
        # 존재하지 않는 백로그 ID로 순서 저장 시도
        result = save_backlog_order([999, 1000])
        
        # 검증
        assert result is True  # 논리적 문제 없음, True 반환
        mock_db_session.add.assert_not_called()  # 데이터베이스에 추가되지 않았음을 확인
