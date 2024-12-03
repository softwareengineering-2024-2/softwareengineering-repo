import pytest
from app import create_app
from database import db
from models.user_model import Users

@pytest.fixture(scope="module")
def test_app():
    """테스트용 Flask 애플리케이션 설정"""
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test_secret_key",
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope='function')
def client(test_app):
    """Flask 테스트 클라이언트 생성"""
    return test_app.test_client()

@pytest.fixture(scope='function')
def runner(test_app):
    """Flask 테스트 CLI 러너 생성"""
    return test_app.test_cli_runner()

@pytest.fixture(scope='function')
def user_fixture(test_app):
    """테스트용 사용자 생성 및 데이터 반환"""
    with test_app.app_context():
        user = Users.create_user('testuser', 'token1234')
        db.session.add(user)
        db.session.commit()
        user_data = {
            'user_id': user.user_id,
            'name': 'Test User',  
            'email': 'testuser@example.com',  
            'profile_pic': 'default.jpg', 
        }
        return user_data

@pytest.fixture(scope='function')
def authenticated_user(client, user_fixture):
    """인증된 사용자를 위한 픽스처로, 테스트 세션을 제공합니다."""
    with client.session_transaction() as session:
        session['_user_id'] = str(user_fixture['user_id'])  
        session['_fresh'] = True
        session['user_info'] = {
            "id": str(user_fixture['user_id']),
            "name": user_fixture['name'],
            "email": user_fixture['email'],
            "profile_pic": user_fixture['profile_pic'],
        }
    return client