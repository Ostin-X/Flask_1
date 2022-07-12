import pytest
import flask
from src.flask_report.flask_main import *
from report_f1.funcs import Pilot


@pytest.mark.parametrize('test_input', ['/drivers', '/ham', '/'])
def test_get(client, test_input):
    response = client.get(test_input)
    assert response.status_code == 200
    assert response.content_type == 'text/html; charset=utf-8'


# def test_request_example(client):
#     response = client.get('/report')
#     assert b"table table-striped table-hover" in response.data
#     assert b'"https://en.wikipedia.org/wiki/' in response.data


@pytest.mark.parametrize('test_input', ['/drivers', '/drivers?order=Ascending', '/drivers?order=Descending'])
def test_drivers_request(client, test_input):
    response = client.get(test_input)
    assert response.status_code == 200
    assert b'Lewis Hamilton' in response.data
    assert b'Force India' in response.data
    assert b'ALO' in response.data
    assert b'0:01:12.848' in response.data


@pytest.mark.parametrize('test_input', ['/drivers?driver_id=HAM', '/drivers?driver_id=HUL', '/drivers?driver_id=LEC'])
def test_single_driver_request(client, test_input):
    response = client.get(test_input)
    assert response.status_code == 200
    assert bytes(str(pilots[test_input[-3:]].name), 'utf-8') in response.data
    assert bytes(str(pilots[test_input[-3:]].team), 'utf-8') in response.data
    assert b'Force India' not in response.data


def test_pilots():
    assert type(pilots) == dict
    assert len(pilots) == 19
    assert 'HAM' in pilots
    assert 'VER' not in pilots.keys()
    assert type(pilots['VET']) == Pilot
    assert pilots['BOT'].name == 'Valtteri Bottas'
    assert pilots['RAI'].team == 'Scuderia Ferrari'


def test_test_request_context():
    app = flask.Flask(__name__)
    with app.test_request_context('/drivers?driver_id=LEC'):
        assert flask.request.path == '/drivers'
        assert flask.request.args['driver_id'] == 'LEC'
