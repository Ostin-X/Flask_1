import pytest
from src.flask_report.flask_main import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config['TESTING'] = True
    # return app.test_client()
    # with app.test_client() as client:
    client = app.test_client()
    yield client


@pytest.fixture()
def runner():
    app = create_app()
    return app.test_cli_runner()
