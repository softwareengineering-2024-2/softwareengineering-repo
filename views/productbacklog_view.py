# productbacklog_view.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from controllers.productbacklog_controller import get_user_stories, update_product_backlog, create_product_backlog_group, delete_product_backlog, save_backlog_order
from models.productbacklog_model import ProductBacklog
from models.userstory_model import UserStory
from database import db

# Blueprint 객체 생성
productbacklog_bp = Blueprint('productbacklog', __name__)

# Product Backlog 관리 페이지
@productbacklog_bp.route('/product_backlog', methods=['GET'])
def product_backlog_view():
    project_id = request.args.get('project_id')
    print(f"Received project_id: {project_id}")  # 디버깅용 출력
    user_stories = get_user_stories(project_id) or [] # 프로젝트 ID에 따른 유저스토리 목록 가져오기

    # 저장된 ProductBacklog 그룹 가져오기
    product_backlog_groups = ProductBacklog.query.filter_by(project_id=project_id).all()

    return render_template('productbacklog_back.html', user_stories=user_stories,
                           product_backlog_groups=product_backlog_groups)

# 새로운 백로그 그룹 생성
@productbacklog_bp.route('/product_backlog/create_group', methods=['POST'])
def create_backlog_group():
    group_name = request.form.get('group_name')  # 사용자 입력으로 받은 백로그 이름
    story_ids = request.form.getlist('story_ids')  # 그룹화할 유저스토리 ID 목록
    product_backlog_id = create_product_backlog_group(group_name, story_ids)
    return jsonify({"success": True, "product_backlog_id": product_backlog_id})

@productbacklog_bp.route('/product_backlog/move', methods=['POST'])
def move_user_story():
    story_id = request.form.get('story_id')
    backlog_id = request.form.get('backlog_id')
    success = update_product_backlog(story_id, backlog_id)
    return jsonify({"success": success})

@productbacklog_bp.route('/product_backlog/save_groups', methods=['POST'])
def save_backlog_groups():
    data = request.get_json()
    success = True

    for group in data:
        group_name = group['backlogName']
        story_ids = group['storyIds']

        # ProductBacklog 그룹 생성
        backlog_id = create_product_backlog_group(group_name, story_ids)
        if backlog_id is None:
            success = False

    return jsonify({"success": success})

@productbacklog_bp.route('/product_backlog/delete/<int:backlog_id>', methods=['DELETE'])
def delete_backlog_view(backlog_id):
    success = delete_product_backlog(backlog_id)
    return jsonify({"success": success})

# 백로그 박스 순서를 저장
@productbacklog_bp.route('/product_backlog/save_order', methods=['POST'])
def save_backlog_order_view():
    backlog_order_list = request.get_json().get('backlogOrderList', [])
    success = save_backlog_order(backlog_order_list)
    return jsonify({"success": success})