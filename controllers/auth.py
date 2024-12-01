import json
import os
from flask import Blueprint, redirect, request, session, url_for, render_template, flash
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
    UserMixin,
)

from oauthlib.oauth2 import WebApplicationClient
import requests
from dotenv import load_dotenv
from models.user_model import Users

# .env 파일 로드
load_dotenv()

# 블루프린트 생성
auth_bp = Blueprint("auth", __name__)

#로컬환경에서 HTTP로 연결하기
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# OAuth2 클라이언트 설정
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = os.getenv("GOOGLE_DISCOVERY_URL")
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# LoginManager 설정
login_manager = LoginManager()

# User 클래스 정의
class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic


def init_login_manager(app):
    """LoginManager를 Flask 앱에 연결하는 함수"""
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        if "user_info" in session:
            user_info = session["user_info"]
            return User(id_=user_info["id"], name=user_info["name"], email=user_info["email"], profile_pic=user_info["profile_pic"])
        return None

    @login_manager.unauthorized_handler
    def unauthorized():
        return render_template("login.html")

@auth_bp.route("/login")
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=url_for("auth.callback", _external=True),  # 콜백 URL
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@auth_bp.route("/login/callback")
def callback():
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )
    
    if token_response.status_code != 200:
        return "Failed to obtain token from Google.", 400
    
    client.parse_request_body_response(json.dumps(token_response.json()))
    
    # 액세스 토큰 저장
    access_token = token_response.json().get("access_token")
    
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400
    
    # 사용자 정보를 세션에 저장
    session["user_info"] = {
        "id": unique_id,
        "name": users_name,
        "email": users_email,
        "profile_pic": picture,
    }
    
    # 사용자 생성 후 로그인
    Users.create_user(unique_id, access_token)
    
    user = User(id_=unique_id, name=users_name, email=users_email, profile_pic=picture)
    
    login_user(user)
        
    return redirect(url_for("manage_project.manage_project_view"))

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop("user_info", None)  # 세션에서 사용자 정보 제거
    return redirect(url_for("index"))  # 로그아웃 후 인덱스 페이지로 리다이렉트

def get_google_provider_cfg():
    try:
        return requests.get(GOOGLE_DISCOVERY_URL).json()
    except requests.exceptions.RequestException as e:
        return f"Error in getting Google provider configuration: {str(e)}"
