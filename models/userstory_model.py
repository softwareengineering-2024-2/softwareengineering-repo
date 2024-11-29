from database import db

class UserStory(db.Model):
    __tablename__ = 'UserStory'

    story_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('Project.project_id', ondelete='CASCADE'), nullable=False)
    user_story_content = db.Column(db.String(100), nullable=False)
    product_backlog_id = db.Column(db.Integer, db.ForeignKey('ProductBacklog.product_backlog_id'), nullable=True)

    # 관계 설정
    project = db.relationship('Project', backref=db.backref('user_stories', lazy=True))

    # 생성자
    def __init__(self, project_id, user_story_content, product_backlog_id=None):
        self.project_id = project_id
        self.user_story_content = user_story_content
        self.product_backlog_id = product_backlog_id


    # 데이터베이스에 저장하는 메서드
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # 데이터베이스에서 삭제하는 메서드
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        

    # 데이터베이스에서 수정하는 메서드
    def update_in_db(self, user_story_content=None, product_backlog=None):
        
        if user_story_content is not None:
            self.user_story_content = user_story_content
        # if product_backlog is not None:
        #     self.product_backlog = product_backlog
        db.session.commit()
