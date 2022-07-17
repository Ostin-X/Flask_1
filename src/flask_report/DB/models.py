from peewee import *

db = SqliteDatabase('pilots.db')


class BaseModel(Model):
    abbr = CharField(primary_key=True)
    name = CharField()
    nation = CharField()

    class Meta:
        database = db


class Team(BaseModel):
    engine = CharField()
    nation = CharField()


class Pilot(BaseModel):
    team = ForeignKeyField(Team, backref='pilot', )


class SessionTime(Model):
    pilot_abbr = ForeignKeyField(Pilot, backref='lap_time')
    lap_time = CharField()

    class Meta:
        database = db


def create_teams(teams):
    for team in teams:
        team_abbr = team[0][:3].upper()
        if not Team.select().where(Team.abbr == team_abbr).exists():
            Team.create(abbr=team_abbr, name=team[0], engine=team[1], nation=team[2],
                        base=team[3])


def create_pilots(pilots, pilot_nations):
    for ab, pi in pilots.items():
        if not Pilot.select().where(Pilot.abbr == ab).exists():
            Pilot.create(abbr=ab, name=pi.name, team=pi.team[:3].upper(), nation=pilot_nations[ab])


def create_times(pilots):
    for ab, pi in pilots.items():
        if not SessionTime.select().where(SessionTime.pilot_abbr == ab).exists():
            SessionTime.create(pilot_abbr=ab, lap_time=pi.lap_time)
