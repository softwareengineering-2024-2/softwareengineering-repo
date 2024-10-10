from flask import Blueprint, render_template, session
from flask_login import login_required

# 블루프린트 생성
project_main_bp = Blueprint('project_main', __name__)

@project_main_bp.route('/project_main')
@login_required
def project_main():
    return render_template('project_main.html', project_name=session.get('project_name'))
        