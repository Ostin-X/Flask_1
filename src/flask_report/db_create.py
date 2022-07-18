from src.flask_report.db.models import *
from config import teams, pilots_list, pilot_nations

db.create_tables([Team, Pilot, SessionTime])
create_teams(teams)
create_pilots(pilots_list, pilot_nations)
create_times(pilots_list)
db.close()
