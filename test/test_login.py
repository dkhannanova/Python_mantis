def test_login(app):
    app.soap.can_login(username="administrator", password="root")


