from flask import Blueprint, render_template, request, jsonify, redirect, url_for,flash
from controllers.notlist_controller import create_keywords, delete_keyword, show_notlist, get_user_role
from flask_login import current_user

notlist_bp = Blueprint('notlist_view', __name__)

# not list 페이지 렌더링
@notlist_bp.route('/notlist/<int:project_id>', methods=['GET'])
def notlist_back(project_id):
    user_id = request.args.get('user_id')
    not_list = show_notlist(project_id)
    user_role = get_user_role(project_id, user_id)  # 사용자 역할 가져오기
    return render_template('notlist_back.html', not_list=not_list, project_id=project_id, user_id=user_id, user_role=user_role)

# not list 키워드 추가
@notlist_bp.route('/notlist/<int:project_id>', methods=['POST'])
def create_keywords_route(project_id):
    keywords = request.form.get('keywords')
    
    result = create_keywords(keywords, project_id)
    if isinstance(result, tuple):
        return jsonify({"error": result[0]}), result[1]
    not_list = show_notlist(project_id)
    
    return render_template('notlist_back.html', not_list=not_list, project_id=project_id)

# not list 키워드 삭제
@notlist_bp.route('/notlist/<int:project_id>/<int:not_list_id>', methods=['POST'])
def delete_keyword_route(project_id, not_list_id):
    user_id = current_user.id
    result = delete_keyword(not_list_id, project_id, user_id)
    flash(result)
    return redirect(url_for('notlist_view.notlist_back', project_id=project_id))