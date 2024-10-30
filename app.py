import os
from flask import Flask, render_template
from controllers.auth import auth_bp, init_login_manager  # auth.py에서 가져오기
from controllers.profile import profile_bp 
from controllers.create_project import create_project_bp
from controllers.project_main import project_main_bp
from models.project_model import init_db
from views.project_view import project_bp
from dotenv import load_dotenv

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
app.register_blueprint(profile_bp, url_prefix='/profile')
app.register_blueprint(create_project_bp, url_prefix='/create_project')  
app.register_blueprint(project_main_bp, url_prefix='/project_main')  
app.register_blueprint(project_bp, url_prefix='/manage_project')

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    with app.app_context():
        from models.project_model import db  # 데이터베이스 테이블 생성하기 위해 가져오기
        db.create_all()
    app.run(debug=True)  # HTTP로 실행