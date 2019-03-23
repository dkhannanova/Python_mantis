def test_login(app):
    app.session.login("administrator", "root")
    user = app.is_logged_in()
    assert user == "administrator"
    app.project.open_projects_page()
    app.project.manage()


