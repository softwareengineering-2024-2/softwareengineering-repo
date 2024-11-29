from database import db

class Alert(db.Model):
    __tablename__ = 'alert'

    alert_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #user_id = db.Column(db.String(255), db.ForeignKey('User.user_id', ondelete='CASCADE'),nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('Project.project_id', ondelete='CASCADE'),nullable=False)
    alert_content = db.Column(db.String(255))
    #status = db.Column(db.Boolean, nullable=True, default=False)

    # 생성자
    def __init__(self, project_id, alert_content):
        #self.user_id = user_id
        self.project_id = project_id
        self.alert_content = alert_content
        #self.status = status

    # 데이터베이스에 저장하는 메서드
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # 데이터베이스에서 삭제하는 메서드
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # 데이터베이스에서 수정하는 메서드
    def update_in_db(self, keyword=None):
        if keyword is not None:
            self.keyword = keyword
        db.session.commit()