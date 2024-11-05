from database import db
from datetime import date

# Calendar 모델
class Calendar(db.Model):
    # Calendar 테이블 스키마 정의
    __tablename__ = 'Calendar'
    calendar_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.String, db.ForeignKey('User.user_id', ondelete='CASCADE'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('Project.project_id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(20), nullable=False)
    place = db.Column(db.String(20), nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    team = db.Column(db.String(20), nullable=False, default=True)
    color = db.Column(db.Boolean, nullable=False)
    content = db.Column(db.String(40), nullable=False)
    important = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, user_id, project_id, title, place, start_date, due_date, team, color, content, important):
        self.user_id = user_id
        self.project_id = project_id
        self.title = title
        self.place = place
        self.start_date = start_date
        self.due_date = due_date
        self.team = team
        self.color = color
        self.content = content
        self.important = important

    # 일정을 데이터베이스에 저장하는 메서드
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Calendar 테이블에서 해당 데이터를 삭제하는 메서드
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    # 캘린더 ID를 기준으로 일정을 검색하는 메서드
    @classmethod
    def find_by_id(cls, calendar_id):
        return cls.query.filter_by(calendar_id=calendar_id).first()
    
    # 프로젝트 ID를 기준으로 일정을 검색하는 메서드
    @classmethod
    def find_by_project(cls, project_id):
        return cls.query.filter_by(project_id=project_id).all()
    
    # 프로젝트 ID와 팀/개인 여부를 기준으로 일정을 검색하는 메서드
    @classmethod
    def find_by_project_and_team(cls, project_id, team):
        return cls.query.filter_by(project_id=project_id, team=team).all()
    
    # 사용자 ID와 프로젝트 ID를 기준으로 사용자의 프로필 정보를 저장하는 메서드
    @classmethod
    def update_calendar(cls, calendar_id, title, place, start_date, due_date, team, color, content, important):
        schedule = Calendar.find_by_id(calendar_id)
        schedule.title = title
        schedule.place = place
        schedule.start_date = start_date
        schedule.due_date = due_date
        schedule.team = team
        schedule.color = color
        schedule.content = content
        schedule.important = important
        schedule.save_to_db()
