from fixture.session import SessionHelper
from fixture.project import ProjectHelper
from model.project import Project


def test_project_list(app,db):
    app_list = app.project.get_proj_list()
    db_list = db.get_project_list()
    #def clean(project):
     #   return Project(id=project.id, name=project.name.strip())
    #db_list = map(clean, db.get_project_list())
    assert sorted(app_list, key=Project.prid_or_max) == sorted(db_list, key=Project.prid_or_max)