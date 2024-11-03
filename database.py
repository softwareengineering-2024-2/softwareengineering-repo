from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy 객체 생성
db = SQLAlchemy()

# 데이터베이스를 초기화하는 함수
def init_db(app):
    # 애플리케이션과 SQLAlchemy 객체를 연결
    db.init_app(app)
    
    # 테이블 생성
    with app.app_context():
        db.create_all()