# retrospect_model.py
from database import db

class Retrospect(db.Model):
    __tablename__ = 'Retrospect'

    retrospect_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(255), db.ForeignKey('User.user_id', ondelete='CASCADE'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('Project.project_id', ondelete='CASCADE'), nullable=False)
    sprint_id = db.Column(db.Integer, db.ForeignKey('Sprint.sprint_id', ondelete='CASCADE'), nullable=False)
    retrospect_title = db.Column(db.String(50), nullable=True)
    retrospect_content = db.Column(db.Text, nullable=True)
    label = db.Column(db.String(10), nullable=True)
    file_link = db.Column(db.String(2083), nullable=True)

    def __init__(self, user_id, project_id, sprint_id, retrospect_title=None, retrospect_content=None, label=None, file_link=None):
        self.user_id = user_id
        self.project_id = project_id
        self.sprint_id = sprint_id
        self.retrospect_title = retrospect_title
        self.retrospect_content = retrospect_content
        self.label = label
        self.file_link = file_link

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
