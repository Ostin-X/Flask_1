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


def test_db2(database_create):
    elements_number = 3
    assert isinstance(db, SqliteDatabase)
    assert Team.get(Team.abbr == f'te{elements_number}').name == f'team_name_{elements_number}'
    assert Pilot.get(Pilot.nation == f'driver_nation_{elements_number}').name == f'driver_name_{elements_number}'
    assert SessionTime.get(
        SessionTime.pilot_abbr == f'dr{elements_number}').lap_time == f'{elements_number}:0{elements_number}:0{elements_number}.{elements_number}00'
