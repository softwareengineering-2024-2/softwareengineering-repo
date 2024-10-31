import os
from flask import Flask, render_template
from controllers.auth import auth_bp, init_login_manager
from controllers.create_project import create_project_bp
from controllers.project_main import project_main_bp
from views.project_view import project_bp
from dotenv import load_dotenv
from models import init_db

# .env 파일 로드
load_dotenv()

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# MySQL 데이터베이스 연결 설정
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 모델 초기화 함수 호출
init_db(app)

# LoginManager 초기화
init_login_manager(app)

# Register the authentication blueprint
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(project_main_bp, url_prefix='/project_main')
app.register_blueprint(project_bp, url_prefix='/manage_project')

@app.route("/")
def index():
    return render_template("index.html")

#------------------------------------------------
#view로 이동 요청
@app.route("/main")
def main():
    return render_template("base.html")

@app.route("/milestone")
def milestone():
    return render_template("milestone.html")

@app.route("/userstory")
def userstory():
    return render_template("userstory.html")

@app.route("/backlog")
def backlog():
    return render_template("backlog.html")

@app.route("/sprint")
def sprint():
    return render_template("sprint.html")

@app.route("/board")
def board():
    return render_template("board.html")

@app.route("/review")
def review():
    return render_template("review.html")
#-------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)  # HTTP로 실행