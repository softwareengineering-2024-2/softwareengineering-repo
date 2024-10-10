from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy 객체 생성
db = SQLAlchemy()

# 앱을 사용하여 데이터베이스를 초기화하는 메서드
def init_db(app):
    db.init_app(app)

class Project(db.Model):
    __tablename__ = 'project'

    project_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_name = db.Column(db.String(20), nullable=False)

    def __init__(self, project_name):
        self.project_name = project_name

    # 프로젝트를 데이터베이스에 저장하는 메서드
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # ID를 기준으로 프로젝트를 검색하는 메서드
    @classmethod
    def find_by_id(cls, project_id):
        return cls.query.get(project_id)

    # 모든 프로젝트를 가져오는 메서드
    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    # 데이터베이스에서 프로젝트를 삭제하는 메서드
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
