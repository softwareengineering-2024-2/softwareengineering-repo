import os
from flask import Flask, render_template
from controllers.auth import auth_bp, init_login_manager  # auth.py에서 가져오기
from controllers.profile import profile_bp 
from controllers.create_project import create_project_bp
from controllers.project_main import project_main_bp
from dotenv import load_dotenv
 
# .env 파일 로드
load_dotenv()

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)


# LoginManager 초기화
init_login_manager(app)

# Register the authentication blueprint
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(profile_bp, url_prefix='/profile')
app.register_blueprint(create_project_bp, url_prefix='/create_project')  
app.register_blueprint(project_main_bp, url_prefix='/project_main')  


@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)  # HTTP로 실행