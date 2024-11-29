import os
from flask import Flask, render_template
from controllers.auth import auth_bp, init_login_manager  # auth.py에서 가져오기
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

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)  # HTTP로 실행