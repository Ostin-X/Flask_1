from peewee import *
from src.flask_report.config import pilots


db = SqliteDatabase('pilots.db')

teams = [['Sauber', 'Ferrari', 'Switzerland', 'Hinwill, CH'],
         ['Toro Rosso', 'Red Bull', 'Maranello, IT', 'Faenza, IT'],
         ['Renault', 'Renault', 'France', 'Enstone, UK'],
         ['Force India', 'Mercedes', 'United Kingdom', 'Silverstone, UK'],
         ['Ferrari', 'Ferrari', 'Italy', 'Maranello, IT'], ['Haas', 'Ferrari', 'United States', 'Kannapolis, US'],
         ['McLaren', 'Mercedes', 'United Kingdom', 'Woking, UK'], ['Mercedes', 'Mercedes', 'Germany', 'Brackley, UK'],
         ['Red Bull', 'Red Bull', 'Austria', 'Milton Keynes, UK'],
         ['Williams', 'Mercedes', 'United Kingdom', 'Grove, UK']]
pilot_nations = {'RIC': 'Australia', 'VET': 'Germany', 'HAM': 'United Kingdom', 'RAI': 'Finland', 'BOT': 'Finland',
                 'OCO': 'France', 'ALO': 'Spain', 'SAI': 'Spain', 'PER': 'Mexico', 'GAS': 'France', 'HUL': 'Germany',
                 'VAN': 'Belgium', 'SIR': 'ass', 'LEC': 'Monaco', 'GRO': 'France', 'HAR': 'United Kingdom',
                 'ERI': 'Sweden', 'STR': 'United Kingdom', 'MAG': 'Denmark'}


class Team(Model):
    abbr = CharField(primary_key=True)
    name = CharField()
    engine = CharField()
    nation = CharField()
    base = CharField()

    class Meta:
        database = db


class Pilot(Model):
    abbr = CharField(primary_key=True)
    name = CharField()
    team = ForeignKeyField(Team, backref='pilots', )
    nation = CharField()

    class Meta:
        database = db


class SessionTime(Model):
    pilot_abbr = ForeignKeyField(Pilot, backref='lap_time')
    lap_time = CharField()

    class Meta:
        database = db


db.connect()
db.create_tables([Team, Pilot, SessionTime])


def create_teams(teams):
    for team in teams:
        team_abbr = team[0][:3].upper()
        try:
            locals()[team_abbr] = Team.create(abbr=team_abbr, name=team[0], engine=team[1], nation=team[2],
                                              base=team[3])
        except IntegrityError:
            pass


def create_pilots_and_lap_times(pilots, pilot_nations):
    for ab, pi in pilots.items():
        try:
            locals()[ab] = Pilot.create(abbr=ab, name=pi.name, team=pi.team[:3].upper(), nation=pilot_nations[ab])
        except IntegrityError:
            pass
        try:
            time = SessionTime.create(pilot_abbr=ab, lap_time=pi.lap_time)
        except IntegrityError:
            pass


# for pilot_ in Pilot.select():
#     print(pilot_.name)

hami = Pilot.select().where(Pilot.name == 'Lewis Hamilton').get()
print(hami.name)
hami = Pilot.get('Lewis Hamilton' == Pilot.name)
print(hami.team.name)
for pi in Pilot.select().join(Team).where(Team.abbr == 'FER'):
    print(pi.name)
print('_______________________')
query = (Pilot
         .select(Pilot, Team)
         .join(Team)
         .where(Pilot.abbr == 'HAM'))
for pi in query:
    print(pi.name,pi.team.name)
