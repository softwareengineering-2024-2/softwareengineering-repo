from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app, create_tables=False):
    db.init_app(app)
    if create_tables:
        with app.app_context():
            db.create_all()
