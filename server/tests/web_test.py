import os
import tempfile
import os.path
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import pytest
import gaia_server.server_web as server_web
import gaia_server.database as database
import gaia_server.constants as constants

@pytest.fixture
def client():
    server_web.webserver.config['TESTING'] = True
    web_client = server_web.webserver.test_client()

    db = database.Database()
    db.recreate_database()
    db.delete_all_commands()

    yield web_client


def test_server_is_up_and_running(client):
    rv = client.get('/')
    assert rv.status_code == 200


def test_asset_css(client):
    rv = client.get('/public/css/gaia.css')
    assert rv.status_code == 200


def test_asset_js(client):
    rv = client.get('/public/img/gaia.jpg')
    assert rv.status_code == 200


def test_asset_img(client):
    rv = client.get('/public/js/jquery-3.3.1.min.js')
    assert rv.status_code == 200


def test_command_only_post(client):
    rv = client.get('/command')
    assert rv.status_code == 404


def test_command_no_pwd(client):
    data = {}
    rv = client.post('/command', data=data)
    assert rv.status_code == 401


def test_command_no_pwd(client):
    data = {'passphrase': ''}
    rv = client.post('/command', data=data)
    assert rv.status_code == 401


def test_command_no_data(client):
    data = {'passphrase': constants.AUTHENTICATION_TOKEN}
    rv = client.post('/command', data=data)
    assert rv.status_code == 406


def test_command_data_but_no_update(client):
    data = dict()
    data['passphrase'] = constants.AUTHENTICATION_TOKEN
    data['newCommand'] = '2'  # ='REBOOT'
    # no update config

    rv = client.post('/command', data=data)
    assert rv.status_code == 201

    db = database.Database()
    cmd = db.get_command()
    assert cmd is not None
    assert cmd['text'] == 'REBOOT'
    assert cmd['config'] is None


def test_command_no_data(client):
    data = dict()
    data['passphrase'] = constants.AUTHENTICATION_TOKEN
    data['newCommand'] = '1'  # ='SHUTDOWN'
    data['updateConfig'] = '1'
    data['feedingEnabled'] = '1'
    data['wateringEnabled'] = '1'
    data['feedingCron'] = '15h 0,3,4,5,6'
    data['wateringCron'] = '14h 1,2'
    data['pump1Duration'] = '101'
    data['pump2Duration'] = '102'
    data['pump3Duration'] = '103'
    data['pump4Duration'] = '104'

    rv = client.post('/command', data=data)
    assert rv.status_code == 201


    db = database.Database()
    cmd = db.get_command()
    assert cmd is not None
    assert cmd['text'] == 'SHUTDOWN'
    assert cmd['config'] is not None

    assert cmd['config']['feeding_module_activated'] == int(data['feedingEnabled'])
    assert cmd['config']['watering_module_activated'] == int(data['wateringEnabled'])
    assert cmd['config']['feeding_module_cronstring'] == data['feedingCron']
    assert cmd['config']['watering_module_cronstring'] == data['wateringCron']
    assert cmd['config']['watering_pump_1_duration'] == int(data['pump1Duration'])
    assert cmd['config']['watering_pump_2_duration'] == int(data['pump2Duration'])
    assert cmd['config']['watering_pump_3_duration'] == int(data['pump3Duration'])
    assert cmd['config']['watering_pump_4_duration'] == int(data['pump4Duration'])
