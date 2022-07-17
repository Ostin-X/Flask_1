import pytest
import os
from src.flask_report.DB.models import *
from src.flask_report.config import *


def test_db1():
    assert isinstance(db, SqliteDatabase)


def test_db2():
    os.remove('pilots.db')
    db.create_tables([Team, Pilot, SessionTime])
    create_teams(teams)
    create_pilots(pilots_list, pilot_nations)
    create_times(pilots_list)
    assert Team.get(Team.abbr == 'MER').name == 'Mercedes'
    assert Pilot.get(Pilot.nation == 'United Kingdom').name == 'Lewis Hamilton'
    assert SessionTime.get(SessionTime.pilot_abbr == 'HAM').lap_time == 'No time'
