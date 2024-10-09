from flask import render_template

def init_project_views(app):
    @app.route('/project/create')
    def create_project():
        return render_template('create_project.html')

    @app.route('/project/select')
    def select_project():
        return render_template('select_project.html')

    @app.route('/project/delete')
    def delete_project():
        return "Project deleted"
