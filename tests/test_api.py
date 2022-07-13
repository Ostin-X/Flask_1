import pytest
import flask


@pytest.mark.parametrize('test_input, format_res, bytes_res1, bytes_res2', [('/api/v1/report', 'application/json',
                                                                             b'", "lap_time": "No time"}, "VET": {"abbr": "VET", "name": "Sebastian Vettel"',
                                                                             b'main Grosjean", "team": "Haas F1", "lap_time": "0:01:12.930"}, "HAR": {"abbr'),
                                                                            ('/api/v1/report?format=xml',
                                                                             'application/xml',
                                                                             b'"><abbr type="str">VET</abbr><name type="str">Sebastian Vettel</name><team t',
                                                                             b'0</lap_time></SAI><PER type="dict"><abbr type="str">PER</abbr><name type="st')])
def test_report_api_v1_json_xml(client, test_input, format_res, bytes_res1, bytes_res2):
    response = client.get(test_input)
    assert response.status_code == 200
    assert response.content_type == format_res
    assert bytes_res1 in response.data
    assert bytes_res2 in response.data


@pytest.mark.parametrize('test_input, format_res, bytes_res1, bytes_res2', [('/api/v1/report/drivers', 'application/json',
                                                                             b'", "lap_time": "No time"}, "VET": {"abbr": "VET", "name": "Sebastian Vettel"',
                                                                             b'main Grosjean", "team": "Haas F1", "lap_time": "0:01:12.930"}, "HAR": {"abbr'),
                                                                            ('/api/v1/report/drivers?format=xml',
                                                                             'application/xml',
                                                                             b'"><abbr type="str">VET</abbr><name type="str">Sebastian Vettel</name><team t',
                                                                             b'0</lap_time></SAI><PER type="dict"><abbr type="str">PER</abbr><name type="st')])
def test_drivers_api_v1_json_xml(client, test_input, format_res, bytes_res1, bytes_res2):
    response = client.get(test_input)
    assert response.status_code == 200
    assert response.content_type == format_res
    assert bytes_res1 in response.data
    assert bytes_res2 in response.data


@pytest.mark.parametrize('test_input, format_res, bytes_res1, bytes_res2', [('/api/v1/report/LEC', 'application/json',
                                                                             b'{"abbr": "LEC", "name": "Charles Leclerc", "team": "Sauber", "lap_time": "0:',
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


@pytest.mark.parametrize('test_input, format_res, bytes_res1, bytes_res2', [('/api/v1/report/drivers/LEC', 'application/json',
                                                                             b'{"abbr": "LEC", "name": "Charles Leclerc", "team": "Sauber", "lap_time": "0:',
                                                                             b'01:12.829"}\n'),
                                                                            ('/api/v1/report/drivers/BOT?format=xml',
                                                                             'application/xml',
                                                                             b'<?xml version="1.0" encoding="UTF-8" ?><root><abbr type="str">BOT</abbr><nam',
                                                                             b'e type="str">Valtteri Bottas</name><team type="str">Mercedes F1</team><lap_t')])
def test_single_report_api_v1_json_xml(client, test_input, format_res, bytes_res1, bytes_res2):
    response = client.get(test_input)
    assert response.status_code == 200
    assert response.content_type == format_res
    assert bytes_res1 in response.data
    assert bytes_res2 in response.data


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
