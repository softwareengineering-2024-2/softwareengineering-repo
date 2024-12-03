from models.not_list_model import NotList

# not list 보여주기
def show_notlist(project_id):

    not_list_keywords = NotList.query.filter_by(project_id=project_id).all()
    return not_list_keywords

# not list 키워드 추가
def create_keywords(keyword, project_id):
    
    # not list 키워드 추가하기
    new_keyword = NotList(project_id=project_id, keyword=keyword)
    new_keyword.save_to_db()

    return new_keyword

# not list 삭제
def delete_keyword(not_list_id):
    not_list_item = NotList.query.filter_by(not_list_id=not_list_id).first()
    if not_list_item:
        not_list_item.delete_from_db()
    return None