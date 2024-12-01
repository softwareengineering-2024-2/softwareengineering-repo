from database import db

# 번업 차트 데이터 모델
class BacklogChanges(db.Model):
    __tablename__ = 'BacklogChanges'
    change_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('Project.project_id', ondelete='CASCADE'), nullable=False)
    changed_date = db.Column(db.Date, nullable=False)
    total_backlog = db.Column(db.Integer, nullable=False)
    completed_backlog = db.Column(db.Integer, nullable=False)

    def __init__(self, project_id, changed_date, total_backlog, completed_backlog):
        self.project_id = project_id
        self.changed_date = changed_date
        self.total_backlog = total_backlog
        self.completed_backlog = completed_backlog

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # 프로젝트의 모든 백로그 수량 변경사항을 조회하는 함수
    @classmethod
    def get_changes_by_project(cls, project_id):
        return cls.query.filter_by(project_id=project_id).order_by(cls.changed_date).all()

    # 프로젝트의 마지막 백로그 수량 변경사항을 조회하는 함수
    @classmethod
    def get_last_change(cls, project_id):
        return cls.query.filter_by(project_id=project_id).order_by(BacklogChanges.changed_date.desc()).first()