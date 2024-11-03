from database import db
from datetime import date

# Milestone 모델
class Milestone(db.Model):
    # Milestone 테이블 스키마 정의
    __tablename__ = 'Milestone'
    milestone_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('Project.project_id', ondelete='CASCADE'), nullable=False)
    milestone_content = db.Column(db.String(40), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    check = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, project_id, milestone_content, due_date, check):
        self.project_id = project_id
        self.milestone_content = milestone_content
        self.due_date = due_date
        self.check = check

    # 마일스톤을 데이터베이스에 저장하는 메서드
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Milestone 테이블에서 해당 데이터를 삭제하는 메서드
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    # 마일스톤 ID를 기준으로 마일스톤을 검색하는 메서드
    @classmethod
    def find_by_id(cls, milestone_id):
        return cls.query.filter_by(milestone_id=milestone_id).first()
    
    # 프로젝트 ID를 기준으로 마일스톤을 due_date 순서대로 검색하는 메서드
    @classmethod
    def find_by_project_ordered_by_due_date(cls, project_id):
        return cls.query.filter_by(project_id=project_id).order_by(cls.due_date).all()
    
    # 사용자 ID와 프로젝트 ID를 기준으로 사용자의 프로필 정보를 저장하는 메서드
    @classmethod
    def update_milestone(cls, milestone_id, milestone_content, due_date):
        milestone = cls.query.filter_by(milestone_id=milestone_id).first()
        milestone.milestone_content = milestone_content
        milestone.due_date = due_date
        milestone.save_to_db()

    # 현재 날짜와 마일스톤의 날짜를 비교하여 check 속성값을 업데이트하는 메서드
    @classmethod
    def update_check_status(cls, project_id):
        today = date.today()
        milestones = cls.query.filter_by(project_id=project_id).all()
        for milestone in milestones:
            if milestone.due_date <= today:
                milestone.check = True
                milestone.save_to_db()
            else:
                milestone.check = False
                milestone.save_to_db()