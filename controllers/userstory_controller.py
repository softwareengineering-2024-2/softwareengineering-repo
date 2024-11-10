from models.userstory_model import UserStory

from database import db

# 유저스토리 보여주기
def show_stories(project_id):
   
    if not project_id:
        return "Project ID is missing", 400
    
    stories = UserStory.query.filter_by(project_id=project_id).all()
    return stories

# 유저스토리 작성
def create_story(user_story_content, project_id):
    if not project_id:
        return "Project ID is missing", 400

    new_userstory = UserStory(project_id=project_id, user_story_content=user_story_content)
    new_userstory.save_to_db()

    return new_userstory

 

# 유저스토리 수정
def update_story(story_id, user_story_content):
    story = UserStory.query.get_or_404(story_id)    
    story.update_in_db(user_story_content=user_story_content)
    
    return story

# 유저스토리 삭제
def delete_story(story_id):
    story = UserStory.query.filter_by(story_id=story_id).first_or_404()
    if story:
        story.delete_from_db()
    return None