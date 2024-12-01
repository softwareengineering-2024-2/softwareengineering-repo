import os
from flask import Flask, render_template
from controllers.auth import auth_bp, init_login_manager
from views.project_main_view import project_main_bp
from views.manage_project_view import manage_project_bp
from views.userstory_view import userstory_bp
from views.milestone_view import milestone_bp
from views.productbacklog_view import productbacklog_bp
from views.sprint_view import sprint_bp
from views.calendar_view import calendar_bp
from views.retrospect_view import retrospect_bp
from views.burnup_view import burnup_bp
from views.scrum_view import scrum_bp
from views.guide_view import guide_bp
from dotenv import load_dotenv
from database import init_db

# .env 파일 로드
load_dotenv()

def create_app(test_config=None):
    """Flask 애플리케이션 팩토리 함수"""
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

    if test_config:
        app.config.update(test_config)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 데이터베이스 초기화
    init_db(app)

    # LoginManager 초기화
    init_login_manager(app)

    # 블루프린트 등록
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(project_main_bp, url_prefix='/project_main')
    app.register_blueprint(manage_project_bp, url_prefix='/manage_project')
    app.register_blueprint(milestone_bp, url_prefix='/milestone')
    app.register_blueprint(productbacklog_bp, url_prefix='/productbacklog')
    app.register_blueprint(sprint_bp, url_prefix='/sprint')
    app.register_blueprint(userstory_bp, url_prefix='/userstory')
    app.register_blueprint(calendar_bp, url_prefix='/calendar')
    app.register_blueprint(retrospect_bp, url_prefix='/retrospect')
    app.register_blueprint(burnup_bp, url_prefix='/burnup')
    app.register_blueprint(scrum_bp, url_prefix='/scrum')
    app.register_blueprint(guide_bp, url_prefix='/guide')

    @app.route("/")
    def index():
        return render_template("login.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)