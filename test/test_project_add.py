from model.project import Project


def test_project_add(app, db, json_project):
    project = json_project
    db_list_0 = db.get_project_list()
    app.project.open_projects_page()
    app.project.manage()
    app.project.add_project_button()
    app.project.fill_project(project)
    app_list = app.project.get_proj_list()
    db_list = db.get_project_list()
    # def clean(project):
    #   return Project(id=project.id, name=project.name.strip())
    # db_list = map(clean, db.get_project_list())
    assert sorted(app_list, key=Project.prid_or_max) == sorted(db_list, key=Project.prid_or_max)
    print (len(db_list))
