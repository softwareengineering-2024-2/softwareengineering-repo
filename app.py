import os
from flask import Flask, render_template
from controllers.auth import auth_bp, init_login_manager
from views.project_main_view import project_main_bp
from views.manage_project_view import manage_project_bp
from views.userstory_view import userstory_bp
from views.notlist_view import notlist_bp
from views.milestone_view import milestone_bp
from views.productbacklog_view import productbacklog_bp
from views.sprint_view import sprint_bp
from views.calendar_view import calendar_bp
from dotenv import load_dotenv
from database import init_db

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
app.register_blueprint(manage_project_bp, url_prefix='/manage_project')
app.register_blueprint(milestone_bp, url_prefix='/milestone')
app.register_blueprint(productbacklog_bp, url_prefix='/productbacklog')
app.register_blueprint(sprint_bp, url_prefix='/sprint')
app.register_blueprint(userstory_bp, url_prefix='/userstory_view')
app.register_blueprint(notlist_bp, url_prefix='/notlist_view')
app.register_blueprint(calendar_bp, url_prefix='/calendar')

@app.route("/")
def index():
    return render_template("login.html")

#------------------------------------------------
#view로 이동 요청
@app.route("/main")
def main():
    total_tasks = 100  # 전체 작업 수 (예시)
    completed_tasks = 25  # 완료된 작업 수 (예시)
    # 달성률 계산
    progress_percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    return render_template('main.html', progress_percentage=progress_percentage)

# @app.route("/milestone")
# def milestone():
#     return render_template("milestone.html")

# @app.route("/userstory")
# def userstory():
#     return render_template("userstory.html")

# @app.route("/backlog")
# def backlog():
#     return render_template("backlog.html")

# @app.route("/sprint")
# def sprint():
#     return render_template("sprint.html")

@app.route("/board")
def board():
    return render_template("board.html")

@app.route("/review")
def review():
    return render_template("review.html")

# @app.route('/project')
# def project():
#     return render_template('manage_project.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/guide')
def guide():
    return render_template('guide.html')
#-------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)  # HTTP로 실행
