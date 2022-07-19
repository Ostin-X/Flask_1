import sqlite3

import pytest
from src.flask_report.flask_main import create_app
from report_f1.funcs import Pilot as Pi_class
from src.flask_report.db.models import *


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


@pytest.fixture()
def database_create_in_memory():
    elements_number = 3
    test_teams_list, test_drivers_nations_dict, test_pilots_dict = [], {}, {}
    while elements_number:
        test_teams_list.append(
            [f'te{elements_number}', f'team_name_{elements_number}', f'team_engine_{elements_number}',
             f'team_nation_{elements_number}', f'team_base_{elements_number}'])

        test_drivers_nations_dict[f'dr{elements_number}'] = f'driver_nation_{elements_number}'

        test_pilots_dict[f'dr{elements_number}'] = Pi_class(f'dr{elements_number}', f'driver_name_{elements_number}',
                                                            f'team_name_{elements_number}')

        test_pilots_dict[f'dr{elements_number}'].set_end_time(
            f'2022-01-15_{elements_number}:{elements_number}:{elements_number}.{elements_number}')
        test_pilots_dict[f'dr{elements_number}'].set_start_time(f'2022-01-15_0:0:0.0')

        elements_number -= 1

    db.init(':memory:')
    db.create_tables([Team, Pilot, SessionTime])
    create_teams(test_teams_list)
    create_pilots(test_pilots_dict, test_drivers_nations_dict)
    create_times(test_pilots_dict)
