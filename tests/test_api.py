import pytest
import flask
import requests


@pytest.mark.parametrize('test_input, format_res, bytes_res1, bytes_res2', [('/api/v1/report', 'application/json',
                                                                             b'"team":"Toro Rosso","lap_tim',
                                                                             b'ame":"Romain Grosjean","team":"Haas"'),
                                                                            ('/api/v1/report?order=desc',
                                                                             'application/json',
                                                                             b'"team":"Toro Rosso","lap_tim',
                                                                             b':"SAI","name":"Carlos Sainz","team":"Renault"'),
                                                                            ('/api/v1/report?format=xml',
                                                                             'application/xml',
                                                                             b'ndoorne</name><team type="str">McLaren</team><lap_time type="str">0:01:12.46',
                                                                             b't"><abbr type="str">LEC</abbr><name type="str">Charles Leclerc</name><team t'),
                                                                            ('/api/v1/report?format=xml&order=desc',
                                                                             'application/xml',
                                                                             b'ndoorne</name><team type="str">McLaren</team><lap_time type="str">0:01:12.46',
                                                                             b't"><abbr type="str">LEC</abbr><name type="str">Charles Leclerc</name><team t')])
def test_report_api_v1_json_xml(client, test_input, format_res, bytes_res1, bytes_res2):
    response = client.get(test_input)
    assert response.status_code == 200
    assert response.content_type == format_res
    assert bytes_res1 in response.data
    assert bytes_res2 in response.data


@pytest.mark.parametrize('test_input, format_res, bytes_res1, bytes_res2',
                         [('/api/v1/report/drivers', 'application/json',
                           b'"abbr":"RAI","name":"Kimi R',
                           b'"RIC","name":"Daniel Ricciar'), ('/api/v1/report/drivers?order=desc', 'application/json',
                                                              b'team":"Renault"},{"abbr":"HAR","name"',
                                                              b'"RIC","name":"Daniel Ricciar'),
                          ('/api/v1/report/drivers?format=xml',
                           'application/xml',
                           b'><LEC type="dict"><abbr type="str">L',
                           b' type="str">Kimi R'), ('/api/v1/report/drivers?order=desc&format=xml',
                                                    'application/xml',
                                                    b'><LEC type="dict"><abbr type="str">L',
                                                    b' type="str">Kimi R')])
def test_drivers_api_v1_json_xml(client, test_input, format_res, bytes_res1, bytes_res2):
    response = client.get(test_input)
    assert response.status_code == 200
    assert response.content_type == format_res
    assert bytes_res1 in response.data
    assert bytes_res2 in response.data


@pytest.mark.parametrize('test_input, format_res, bytes_res1, bytes_res2', [('/api/v1/report/LEC', 'application/json',
                                                                             b'{"abbr":"LEC","name":"Charles Leclerc","team":"Sauber"}\n',
                                                                             b'01:12.829"}\n'),
                                                                            ('/api/v1/report/BOT?format=xml',
                                                                             'application/xml',
                                                                             b'<?xml version="1.0" encoding="UTF-8" ?><root><abbr type="str">BOT</abbr><nam',
                                                                             b'e type="str">Valtteri Bottas</name><team type="str">Mercedes F1</team><lap_t')])
def test_single_report_api_v1_json_xml(client, test_input, format_res, bytes_res1, bytes_res2):
    response = client.get(test_input)
    assert response.status_code == 200
    assert response.content_type == format_res
    assert bytes_res1 in response.data
    assert bytes_res2 in response.data


@pytest.mark.parametrize('test_input, format_res, bytes_res1', [('/api/v1/report/drivers/LEC', 'application/json',
                                                                 b'{"abbr":"LEC","name":"Charles Leclerc","team":"Sauber"}'),
                                                                ('/api/v1/report/drivers/BOT?format=xml',
                                                                 'application/xml',
                                                                 b'<?xml version="1.0" encoding="UTF-8" ?><root><abbr type="str">BOT</abbr><nam')])
def test_single_report_api_v1_json_xml(client, test_input, format_res, bytes_res1):
    response = client.get(test_input)
    assert response.status_code == 200
    assert response.content_type == format_res
    assert bytes_res1 in response.data


def test_report_request_context():
    app = flask.Flask(__name__)
    with app.test_request_context('/api/v1/report/LEC?format=xml'):
        assert flask.request.path == '/api/v1/report/LEC'
        assert flask.request.args['format'] == 'xml'


def test_drivers_request_context():
    app = flask.Flask(__name__)
    with app.test_request_context('/api/v1/report/drivers/LEC?format=xml'):
        assert flask.request.path == '/api/v1/report/drivers/LEC'
        assert flask.request.args['format'] == 'xml'


def test_report_requests():
    response = requests.get('http://127.0.0.1:5000/api/v1/report/drivers/VET?format=xml')
    assert response.status_code == 200
