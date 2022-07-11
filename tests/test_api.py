import pytest
import flask


@pytest.mark.parametrize('test_input, format_res, bytes_res1, bytes_res2', [('/api/v1/drivers', 'application/json',
                                                                             b'{"RIC": {"abbr": "RIC", "name": "Daniel Ricciardo", "team": "Red Bull Racing"',
                                                                             b'main Grosjean", "team": "Haas F1", "lap_time": "0:01:12.930"}, "HAR": {"abbr'),
                                                                            ('/api/v1/drivers?format=xml',
                                                                             'application/xml',
                                                                             b'<?xml version="1.0" encoding="UTF-8" ?><root><RIC><abbr>RIC</abbr><name>Dani',
                                                                             b'2.941</lap_time></GAS><HUL><abbr>HUL</abbr><name>Nico Hulkenberg</name><team')])
def test_drivers_api_v1_json_xml(client, test_input, format_res, bytes_res1, bytes_res2):
    response = client.get(test_input)
    assert response.status_code == 200
    assert response.content_type == format_res
    assert bytes_res1 in response.data
    assert bytes_res2 in response.data


@pytest.mark.parametrize('test_input, format_res, bytes_res1, bytes_res2', [('/api/v1/drivers/LEC', 'application/json',
                                                                             b'{"abbr": "LEC", "name": "Charles Leclerc", "team": "Sauber", "lap_time": "0:',
                                                                             b'01:12.829"}\n'),
                                                                            ('/api/v1/drivers/BOT?format=xml',
                                                                             'application/xml',
                                                                             b'<?xml version="1.0" encoding="UTF-8" ?><root><abbr>BOT</abbr><name>Valtteri ',
                                                                             b'Bottas</name><team>Mercedes F1</team><lap_time>0:01:12.434</lap_time></root>')])
def test_single_driver_api_v1_json_xml(client, test_input, format_res, bytes_res1, bytes_res2):
    response = client.get(test_input)
    assert response.status_code == 200
    assert response.content_type == format_res
    assert bytes_res1 in response.data
    assert bytes_res2 in response.data


def test_test_request_context():
    app = flask.Flask(__name__)
    with app.test_request_context('/api/v1/drivers/LEC?format=xml'):
        assert flask.request.path == '/api/v1/drivers/LEC'
        assert flask.request.args['format'] == 'xml'
