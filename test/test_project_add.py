from model.project import Project
from fixture.soap import SoapHelper



def test_project_add(app, json_project, config):
    project = json_project
    soapuser = config['webadmin']['username']
    soappass = config['webadmin']['password']
    soap_list = []
    #def clean(project):
     #   return Project(id=project.id, name=project.name.strip('\n'))
    #soap_list = map(clean, app.soap.mc_projects_get_user_accessible(soapuser, soappass))
    print(soap_list)
    soap_list=app.soap.mc_projects_get_user_accessible(soapuser, soappass)
    print(soap_list)
    app.project.open_projects_page()
    app.project.manage()
    app.project.add_project_button()
    app.project.fill_project(project)
    app_list = app.project.get_proj_list()
    assert sorted(app_list, key=Project.prid_or_max) == sorted(soap_list, key=Project.prid_or_max)
