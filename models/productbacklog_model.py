# productbacklog_model.py
from database import db

class ProductBacklog(db.Model):
    __tablename__ = 'ProductBacklog'

    product_backlog_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    story_id = db.Column(db.Integer, db.ForeignKey('UserStory.story_id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('Project.project_id'), nullable=False)
    product_backlog_content = db.Column(db.String(50), nullable=True)
    status = db.Column(db.Boolean, nullable=True)
    backlog_order = db.Column(db.Integer, nullable=True)
    sprint_id = db.Column(db.Integer, db.ForeignKey('Sprint.sprint_id'), nullable=True)

    # Relationships
    user_story = db.relationship("UserStory", foreign_keys=[story_id])
    sprint = db.relationship("Sprint", back_populates="product_backlog", lazy="joined")  # Sprint를 문자열로 참조

    def __init__(self, story_id, project_id, product_backlog_content=None, status=None, backlog_order=None, sprint_id=None):
        self.story_id = story_id
        self.project_id = project_id
        self.product_backlog_content = product_backlog_content
        self.status = status
        self.backlog_order = backlog_order
        self.sprint_id = sprint_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            "product_backlog_id": self.product_backlog_id,
            "story_id": self.story_id,
            "project_id": self.project_id,
            "product_backlog_content": self.product_backlog_content,
            "status": self.status,
            "backlog_order": self.backlog_order,
            "sprint_id": self.sprint_id,
        }