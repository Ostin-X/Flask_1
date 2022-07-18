from peewee import *

db = SqliteDatabase('pilots.db')


class BaseModel(Model):
    class Meta:
        database = db


class Team(BaseModel):
    abbr = CharField()
    name = CharField()
    engine = CharField()
    nation = CharField()
    base = CharField()


class Pilot(BaseModel):
    abbr = CharField()
    name = CharField()
    nation = CharField()
    team = ForeignKeyField(Team, backref='pilot', field='name')


class SessionTime(BaseModel):
    pilot_abbr = ForeignKeyField(Pilot, backref='lap_time', field='abbr')
    lap_time = CharField()


def create_teams(teams):
    # Team.insert_many(teams, fields=[Team.abbr, Team.name, Team.engine, Team.nation, Team.base]).execute()
    for team in teams:
        if not Team.select().where(Team.abbr == team[0]):
            Team.create(abbr=team[0], name=team[1], engine=team[2], nation=team[3], base=team[4])


def create_pilots(pilots, pilot_nations):
    for ab, pi in pilots.items():
        if not Pilot.select().where(Pilot.abbr == ab):
            Pilot.create(abbr=ab, name=pi.name, team=pi.team, nation=pilot_nations[ab])


def create_times(pilots):
    for ab, pi in pilots.items():
        if not SessionTime.select().where(SessionTime.pilot_abbr == ab):
            SessionTime.create(pilot_abbr=ab, lap_time=pi.lap_time)
