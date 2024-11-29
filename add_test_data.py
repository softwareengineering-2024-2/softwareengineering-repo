# add_test_data.py

from app import app
from database import db
from models.userstory_model import UserStory

with app.app_context():
    # 임의의 유저스토리 데이터 추가
    # user_story1 = UserStory(project_id=3, user_story_content="User Story 1")
    # user_story2 = UserStory(project_id=3, user_story_content="User Story 2")
    # user_story4 = UserStory(project_id=3, user_story_content="User Story 3")
    user_story5 = UserStory(project_id=3, user_story_content="User Story 5")
    user_story6 = UserStory(project_id=3, user_story_content="User Story 6")
    user_story7 = UserStory(project_id=3, user_story_content="User Story 7")
    user_story8 = UserStory(project_id=3, user_story_content="User Story 8")
    user_story9 = UserStory(project_id=3, user_story_content="User Story 9")
    user_story10 = UserStory(project_id=3, user_story_content="User Story 10")

    db.session.add(user_story5)
    db.session.add(user_story6)
    db.session.add(user_story7)
    db.session.add(user_story8)
    db.session.add(user_story9)
    db.session.add(user_story10)
    db.session.commit()

    print("Test data added successfully.")
