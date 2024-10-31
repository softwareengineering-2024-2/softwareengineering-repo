from flask_login import UserMixin
from models import db

# User 모델
class Users(UserMixin, db.Model):
    # User 테이블 생성
    __tablename__ = 'User'
    user_id = db.Column(db.String(255), primary_key=True, nullable=False)
    token = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, user_id, token=None):
        self.user_id = user_id
        self.token = token

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # # 토큰을 기준으로 사용자를 검색하는 메서드
    # @classmethod
    # def get_user_by_token(cls, token):
    #     return cls.query.filter_by(token=token).first()
    
    # @classmethod
    # # 토큰을 기준으로 사용자를 검색하고 사용자 id를 반환하는 메서드
    # def get_user_id_by_token(cls, token):
    #     user = cls.query.filter_by(token=token).first()
    #     if user:
    #         return user.user_id
    #     return None

    # 새로운 사용자 추가
    @classmethod
    def create_user(cls, user_id, token):
        user = cls.query.get(user_id)
        if user is None:
            user = cls(user_id=user_id, token=token)
            user.save_to_db()
        return user
    
    
    