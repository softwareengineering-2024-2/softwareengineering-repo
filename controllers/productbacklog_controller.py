# productbacklog_controller.py

from models.productbacklog_model import ProductBacklog
from models.userstory_model import UserStory
from database import db

# 특정 프로젝트의 유저스토리 목록을 가져오는 함수
def get_user_stories(project_id):
    print(f"Fetching user stories for project_id: {project_id}")  # 디버깅용 출력
    try:
        user_stories = UserStory.query.filter_by(project_id=project_id).order_by(UserStory.story_id).all()
        # return user_stories
        return user_stories if user_stories else []
    except Exception as e:
        print(f"Error fetching user stories: {e}")
        return None

# 유저스토리를 지정된 프로덕트 백로그에 추가하는 함수
def update_product_backlog(story_id, backlog_id):
    try:
        user_story = UserStory.query.get(story_id)
        if user_story:
            user_story.product_backlog_id = backlog_id
            db.session.commit()
            return True
        else:
            print("User story not found")
            return False
    except Exception as e:
        print(f"Error updating product backlog: {e}")
        db.session.rollback()
        return False

# 새로운 ProductBacklog 그룹을 생성하고, 유저스토리들을 해당 그룹으로 업데이트하는 함수
def create_product_backlog_group(group_name, story_ids):
    try:
        # 첫 번째 유저스토리에서 프로젝트 ID 가져오기 (모든 유저스토리가 동일한 프로젝트 ID를 가진다고 가정)
        first_story = UserStory.query.get(story_ids[0])
        if not first_story:
            print("Error: No valid user story found.")
            return None
        project_id = first_story.project_id

        # 동일한 이름의 ProductBacklog 그룹이 있는지 확인
        existing_backlog = ProductBacklog.query.filter_by(project_id=project_id, product_backlog_content=group_name).first()

        if existing_backlog:
            # 이미 존재하는 백로그에 유저스토리 업데이트
            for story_id in story_ids:
                user_story = UserStory.query.get(story_id)
                if user_story:
                    user_story.product_backlog_id = existing_backlog.product_backlog_id
            db.session.commit()
            return existing_backlog.product_backlog_id

        # 동일한 이름의 백로그가 없으면 새로운 ProductBacklog 레코드 생성
        new_backlog = ProductBacklog(
            story_id=first_story.story_id,  # 첫 번째 story_id 임시 설정 (필수 항목 채우기 위해)
            project_id=project_id,
            product_backlog_content=group_name
        )
        db.session.add(new_backlog)
        db.session.commit()

        # 유저스토리의 product_backlog_id를 새로운 백로그 ID로 업데이트
        for story_id in story_ids:
            user_story = UserStory.query.get(story_id)
            if user_story:
                user_story.product_backlog_id = new_backlog.product_backlog_id
        db.session.commit()
        
        return new_backlog.product_backlog_id
    except Exception as e:
        print(f"Error creating product backlog group: {e}")
        db.session.rollback()
        return None
    
# 전달된 모든 백로그 그룹 데이터를 저장하는 함수
# def save_all_backlog_groups(backlog_groups, unassigned_story_ids):
#     try:
#         success = True
#         for group in backlog_groups:
#             group_name = group['backlogName']
#             story_ids = group['storyIds']

#             backlog_id = create_product_backlog_group(group_name, story_ids)
#             if backlog_id is None:
#                 success = False

#         # 백로그에 속하지 않는 유저 스토리의 product_backlog_id를 None으로 업데이트
#         for story_id in unassigned_story_ids:
#             user_story = UserStory.query.get(story_id)
#             if user_story:
#                 user_story.product_backlog_id = None
#                 db.session.add(user_story)
#         db.session.commit()
#         return success
#     except Exception as e:
#         print(f"Error saving backlog groups: {e}")
#         db.session.rollback()
#         return False
def save_all_backlog_groups(backlog_groups, unassigned_story_ids):
    try:
        success = True
        for group in backlog_groups:
            group_name = group['backlogName']
            story_ids = group['storyIds']
            backlog_id = group.get('backlogId')

            if backlog_id:
                # 이미 존재하는 백로그 그룹의 이름 업데이트
                existing_backlog = ProductBacklog.query.get(backlog_id)
                if existing_backlog:
                    existing_backlog.product_backlog_content = group_name
                    db.session.add(existing_backlog)

                    # 유저스토리들을 해당 백로그에 업데이트
                    for story_id in story_ids:
                        user_story = UserStory.query.get(story_id)
                        if user_story:
                            user_story.product_backlog_id = backlog_id
                            db.session.add(user_story)
            else:
                # 새로운 백로그 생성이 필요한 경우에만 생성
                if story_ids:
                    first_story = UserStory.query.get(story_ids[0])
                    if first_story:
                        project_id = first_story.project_id
                        new_backlog = ProductBacklog(
                            story_id=first_story.story_id,
                            project_id=project_id,
                            product_backlog_content=group_name
                        )
                        db.session.add(new_backlog)
                        db.session.commit()

                        # 새로운 백로그와 유저스토리들을 연결
                        for story_id in story_ids:
                            user_story = UserStory.query.get(story_id)
                            if user_story:
                                user_story.product_backlog_id = new_backlog.product_backlog_id
                                db.session.add(user_story)

        # 백로그에 속하지 않는 유저스토리들을 업데이트
        for story_id in unassigned_story_ids:
            user_story = UserStory.query.get(story_id)
            if user_story:
                user_story.product_backlog_id = None
                db.session.add(user_story)

        db.session.commit()
        return True
    except Exception as e:
        print(f"Error saving backlog groups: {e}")
        db.session.rollback()
        return False
    
# 백로그와 해당 백로그에 포함된 유저스토리의 참조를 삭제하는 함수
def delete_product_backlog(backlog_id):
    try:
        backlog = ProductBacklog.query.get(backlog_id)
        if backlog:
            user_stories = UserStory.query.filter_by(product_backlog_id=backlog_id).all()
            for story in user_stories:
                story.product_backlog_id = None  # 초기화하여 유저스토리 박스로 이동하도록 설정
                db.session.add(story)
            
            db.session.delete(backlog)  # 백로그 삭제
            db.session.commit()
            return True
    except Exception as e:
        print(f"Error deleting backlog: {e}")
        db.session.rollback()
    return False

# 백로그 박스의 순서를 저장하는 함수
def save_backlog_order(backlog_order_list):
    try:
        for order, backlog_id in enumerate(backlog_order_list):
            backlog = ProductBacklog.query.get(backlog_id)
            if backlog:
                backlog.backlog_order = order
                db.session.add(backlog)
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error saving backlog order: {e}")
        db.session.rollback()
        return False
