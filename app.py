from flask import Flask
from view.project_view import init_project_views

app = Flask(__name__)

init_project_views(app)

if __name__ == '__main__':
    app.run(debug = True)
