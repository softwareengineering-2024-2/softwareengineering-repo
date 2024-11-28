from database import db

# Calendar 모델
class Calendar(db.Model):
    # Calendar 테이블 스키마 정의
    __tablename__ = 'Calendar'
    calendar_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.String(255), db.ForeignKey('User.user_id', ondelete='CASCADE'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('Project.project_id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(20), nullable=False)
    place = db.Column(db.String(20), nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    team = db.Column(db.Boolean, nullable=False)
    color = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(40), nullable=True)
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

    # 데이터베이스에 저장하는 메서드
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # 데이터베이스에서 삭제하는 메서드
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # 데이터베이스에서 수정하는 메서드
    def update_calendar(self, title, place, start_date, due_date, team, color, content, important):
        self.title = title
        self.place = place
        self.start_date = start_date
        self.due_date = due_date
        self.team = team
        self.color = color
        self.content = content
        self.important = important
        db.session.commit()
