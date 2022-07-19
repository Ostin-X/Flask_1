import pytest
from src.flask_report.db.models import *
from src.flask_report.config import *


def test_db():
    db.init(':memory:')
    db.create_tables([Team, Pilot, SessionTime])
    create_teams(teams)
    create_pilots(pilots_list, pilot_nations)
    create_times(pilots_list)
    assert isinstance(db, SqliteDatabase)
    assert Team.get(Team.abbr == 'MER').name == 'Mercedes'
    assert Pilot.get(Pilot.nation == 'United Kingdom').name == 'Lewis Hamilton'
    assert SessionTime.get(SessionTime.pilot_abbr == 'HAM').lap_time == 'No time'


def test_db2():
    elements_number = 3
    test_teams_list = []
    while elements_number:
        test_teams_list.append(
            [f'te{elements_number}', f'team_name_{elements_number}', f'team_engine_{elements_number}',
             f'team_nation_{elements_number}', f'team_base_{elements_number}'])
        elements_number -= 1
    assert test_teams_list == 4
