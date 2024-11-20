from database import db

class TodoList(db.Model):
    __tablename__ = 'todolist'

    todo_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(255), db.ForeignKey('User.user_id', ondelete='CASCADE'),nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('Project.project_id', ondelete='CASCADE'),nullable=False)
    todo_content = db.Column(db.String(255))
    status = db.Column(db.Boolean, nullable=True, default=False)

    # 생성자
    def __init__(self, user_id, project_id, todo_content, status):
        self.user_id = user_id
        self.project_id = project_id
        self.todo_content = todo_content
        self.status = status

    # 데이터베이스에 저장하는 메서드
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # 데이터베이스에서 삭제하는 메서드
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # 데이터베이스에서 수정하는 메서드
    def update_in_db(self, todo_content=None, status=None):
        if todo_content is not None:
            self.todo_content = todo_content
        if status is not None:
            self.status = status
        db.session.commit()