# sprint_model.py
from database import db

class Sprint(db.Model):
    __tablename__ = 'Sprint'

    sprint_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('Project.project_id'), nullable=False)
    sprint_name = db.Column(db.String(30), nullable=False)

    # Relationships
    product_backlog = db.relationship("ProductBacklog", back_populates="sprint", lazy="joined")

    def __init__(self, project_id, sprint_name, duration=None):
        self.project_id = project_id
        self.sprint_name = sprint_name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
