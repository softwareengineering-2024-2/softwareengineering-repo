from database import db
class NotList(db.Model):
    __tablename__ = 'NotList'

    not_list_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('Project.project_id', ondelete='CASCADE'))
    keyword = db.Column(db.String(20))

    # 관계 설정
    project = db.relationship('Project', backref=db.backref('not_list', lazy=True))

    # 생성자
    def __init__(self, project_id, keyword):
        self.project_id = project_id
        self.keyword = keyword

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
