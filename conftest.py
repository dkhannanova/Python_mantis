import pytest
from fixture.application import Application
import json
import jsonpickle
import os.path
import importlib
from fixture.db import DbFixture
from fixture.soap import SoapHelper
import ftputil
from suds.client import Client

fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(path) as config:
            target = json.load(config)
    return target



@pytest.fixture
def app(request, config):
    global fixture
    global target
    browser = request.config.getoption("--browser")
    web_config = config['web']
    web_admin = config['webadmin']
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=web_config['base_url'])
        fixture.session.login(username=web_admin['username'], password=web_admin['password'])
    return fixture

#@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture

@pytest.fixture(scope="session")
def db(request):
    db_config = load_config(request.config.getoption("--target"))['db']
    #инициализируем собственный класс DbFixture
    dbfixture = DbFixture(host=db_config['host'], name=db_config['name'], user=db_config['user'], password=db_config['password'])

    def fin():
        dbfixture.destroy()
    request.addfinalizer(fin)
    return dbfixture

#def autorize(request):
 #   autorize_config = load_config(request.config.getoption("--target"))['webadmin']
  #  autorizefixture = SoapHelper(soapuser=autorize_config['username'], soappass=autorize_config['password'])

    #def fin():
        #autorizefixture.destroy()
    #request.addfinalizer(fin)
   # return autorizefixture


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")
    parser.addoption("--check_ui", action="store_true")

#через объект metafunc можно получить всю информацию о тестовой функции, в частности информацию о фикстурах, ниже ищем фикстуры, которые начинаются с превикса data
def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            testdata = load_from_module(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])
        elif fixture.startswith("json_"):
            testdata = load_from_json(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])

def load_from_module(module):
    return importlib.import_module("data.%s" % module).testdata

def load_from_json(file):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/%s.json" % file)) as f:
        return jsonpickle.decode(f.read())

@pytest.fixture
def check_ui(request):
    request.config.getoption("--check_ui")
    return fixture


#2 фикстуры ниже необходимы для подключения к ftp серверу(для файла, который отключает капчу, из одной фикстуры configure_server вызывется другая, в которо1 подгружается файл с настройкой подключения к ftp)
@pytest.fixture(scope="session", autouse=True)
def configure_server(request, config):
    install_server_configuration(config['ftp']['host'], config['ftp']['login'], config['ftp']['password'])
    def fin():
        restore_server_configuration(config['ftp']['host'], config['ftp']['login'], config['ftp']['password'])
    request.addfinalizer(fin)
    return fixture

@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption("--target"))


def install_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        #если на удаленной машине существует файл с именем, на который мы переименуем оригинальный конфиг файл, удалаем его
        if remote.path.isfile("config_defaults_inc.php.bak"):
            remote.remove("config_defaults_inc.php.bak")
        #если на удаленной машине присуствует файл с названием ниже, то его переименовываем
        if remote.path.isfile("config_defaults_inc.php"):
            remote.rename("config_defaults_inc.php", "config_defaults_inc.php.bak")
        remote.upload(os.path.join(os.path.dirname(__file__), "resources/config_defaults_inc.php"), "config_defaults_inc.php")

def restore_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_defaults_inc.php.bak"):
            if remote.path.isfile("config_defaults_inc.php"):
                remote.remove("config_defaults_inc.php")
            remote.rename("config_defaults_inc.php.bak", "config_defaults_inc.php")