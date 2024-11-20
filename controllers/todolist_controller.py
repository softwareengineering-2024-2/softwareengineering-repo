from flask import jsonify
from models.todolist_model import TodoList

# 투두리스트 작성
def write_todo(user_id, project_id, todo_content, status):
    todo = TodoList(user_id=user_id, project_id=project_id, todo_content=todo_content, status=status)
    todo.save_to_db()

# 투두리스트 조회
def show_todos(project_id, user_id):
    todos = TodoList.query.filter_by(project_id=project_id, user_id=user_id).all()
    return [{'todo' : todo.todo_content} for todo in todos]


# 투두리스트 수정
def update_todo(todo_id, todo_content):
    todo = TodoList.query.get_or_404(todo_id)
    todo.update_in_db(todo_content=todo_content)
    return todo

# 투두리스트 삭제
def delete_todo(todo_id):
    todo = TodoList.query.filter_by(todo_id=todo_id).first_or_404()
    todo.delete_from_db()
    return None

#투두리스트 상태 변경
def change_todo_status(todo_id):
    todo = TodoList.query.get_or_404(todo_id)
    todo.update_in_db(status=not todo.status)
    return todo