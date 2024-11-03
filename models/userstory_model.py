# userstory_model.py
from database import db

class UserStory(db.Model):
    __tablename__ = 'UserStory'

    story_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('Project.project_id'), nullable=False)
    user_story_content = db.Column(db.String(100), nullable=False)
    product_backlog_id = db.Column(db.Integer, db.ForeignKey('ProductBacklog.product_backlog_id'), nullable=True)

    # Relationships
    # product_backlog = db.relationship("ProductBacklog", foreign_keys=[product_backlog_id], back_populates="user_story")

    def __init__(self, project_id, user_story_content, product_backlog_id=None):
        self.project_id = project_id
        self.user_story_content = user_story_content
        self.product_backlog_id = product_backlog_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
