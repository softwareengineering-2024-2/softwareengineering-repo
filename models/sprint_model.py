# sprint_model.py
from database import db
from datetime import date

# Sprint 모델
class Sprint(db.Model):
    # Sprint 테이블 스키마 정의
    __tablename__ = 'Sprint'
    sprint_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('Project.project_id', ondelete='CASCADE'), nullable=False)
    sprint_name = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(30), nullable=True)
    sprint_start_date = db.Column(db.Date, nullable=False)
    sprint_end_date = db.Column(db.Date, nullable=False)

     # Relationships
    product_backlog = db.relationship("ProductBacklog", back_populates="sprint", lazy="joined")
    backlogs = db.relationship("SprintBacklog", back_populates="sprint", cascade="all, delete-orphan")

    def __init__(self, project_id, sprint_name, status, sprint_start_date, sprint_end_date):
        self.project_id = project_id
        self.sprint_name = sprint_name
        self.status = status
        self.sprint_start_date = sprint_start_date
        self.sprint_end_date = sprint_end_date

    # 날짜 검증
    def is_valid_dates(self):
        # 검증 조건: 시작 날짜는 오늘 이후여야 하고, 종료 날짜는 시작 날짜 이후여야 함
        if self.sprint_start_date < date.today():
            return False
        if self.sprint_end_date < self.sprint_start_date:
            return False
        return True
    
    # 스프린트 테이블에 데이터를 저장하는 메서드
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # 스프린트 테이블에서 해당 데이터를 삭제하는 메서드
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

# Sprint Backlog 모델
class SprintBacklog(db.Model):
    # Sprint Backlog 테이블 스키마 정의
    __tablename__ = 'SprintBacklog'
    sprint_backlog_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sprint_id = db.Column(db.Integer, db.ForeignKey('Sprint.sprint_id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.String(50), default='To Do', nullable=False)
    sprint_backlog_content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.String(255), db.ForeignKey('User.user_id', ondelete='CASCADE'), nullable=False)
    product_backlog_id = db.Column(db.Integer, db.ForeignKey('ProductBacklog.product_backlog_id', ondelete='CASCADE'), nullable=False)

    sprint = db.relationship("Sprint", back_populates="backlogs")

    def __init__(self, sprint_id, status, sprint_backlog_content, user_id, product_backlog_id):
        self.sprint_id = sprint_id
        self.status = status
        self.sprint_backlog_content = sprint_backlog_content
        self.user_id = user_id
        self.product_backlog_id = product_backlog_id

    # 스프린트 백로그 테이블에 데이터를 저장하는 메서드
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # 스프린트 백로그 테이블에서 해당 데이터를 삭제하는 메서드
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # id를 통해 스프린트 백로그 검색
    @classmethod
    def find_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def find_all_by_sprint_id(cls, sprint_id):
        return cls.query.filter_by(sprint_id=sprint_id).all()