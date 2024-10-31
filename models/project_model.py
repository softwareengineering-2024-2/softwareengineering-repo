from models import db

# Project 모델
class Project(db.Model):
    # Project 테이블 생성
    __tablename__ = 'Project'
    project_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    project_name = db.Column(db.String(20), nullable=False)
    project_link = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, project_name, project_link):
        self.project_name = project_name
        self.project_link = project_link

    # 프로젝트를 데이터베이스에 저장하는 메서드
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # ID를 기준으로 프로젝트를 검색하는 메서드
    @classmethod
    def find_by_id(cls, project_id):
        return cls.query.get(project_id)

    # 링크를 기준으로 프로젝트를 검색하는 메서드
    @classmethod
    def find_by_link(cls, project_link):
        return cls.query.filter_by(project_link=project_link).first()
    
    
# UserProject 모델
class UserProject(db.Model):
    # UserProject 테이블 생성
    __tablename__ = 'UserProject'
    index = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    user_id = db.Column(db.String(255), db.ForeignKey('User.user_id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('Project.project_id'), nullable=False)
    user_name = db.Column(db.String(20))
    user_role = db.Column(db.String(20))

    def __init__(self, user_id, project_id, user_name, user_role):
        self.user_id = user_id
        self.project_id = project_id
        self.user_name = user_name
        self.user_role = user_role

    # UserProject 테이블에 데이터를 저장하는 메서드
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # UserProject 테이블에서 해당 데이터를 삭제하는 메서드
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # 프로젝트 ID를 기준으로 UserProject를 검색하는 메서드
    @classmethod
    def find_by_project(cls, project_id):
        return cls.query.filter_by(project_id=project_id).first()
    
    # 사용자 ID와 프로젝트 ID를 기준으로 UserProject를 검색하는 메서드
    @classmethod
    def find_by_user_and_project(cls, user_id, project_id):
        return cls.query.filter_by(user_id=user_id, project_id=project_id).first()
    
    # 사용자 ID를 기준으로 프로젝트 ID 목록을 반환하는 메서드
    @classmethod
    def get_projects_by_user_id(cls, user_id):
        user_projects = cls.query.filter_by(user_id=user_id).all()
        project_list = [Project.find_by_id(up.project_id) for up in user_projects if Project.find_by_id(up.project_id)]
        return project_list
    
    # 사용자 ID와 프로젝트 ID를 기준으로 사용자의 프로필 정보를 저장하는 메서드
    @classmethod
    def set_user_profile(cls, user_id, project_id, user_name, user_role):
        user_project = cls.query.filter_by(user_id=user_id, project_id=project_id).first()
        user_project.user_name = user_name
        user_project.user_role = user_role
        user_project.save_to_db()