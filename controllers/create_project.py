from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required


# 블루프린트 생성
create_project_bp = Blueprint('create_project', __name__)

@create_project_bp.route('/create_project', methods=['GET', 'POST'])
@login_required
def create_project():
    # 일단 프로젝트 하나만 생성하게 해둠 (나중에 DB 연결해서 여러개 생성하고 저장하기)
    if session.get('project_name'):
        flash('이미 프로젝트가 존재합니다.')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        project_name = request.form.get('project_name')

        # 프로젝트 생성 (나중에 DB에 저장하기?)
        session['project_name'] = project_name
        return redirect(url_for('project_main.project_main')) # 생성된 프로젝트의 메인 페이지로 리다이렉트
       
    return render_template('create_project.html')
