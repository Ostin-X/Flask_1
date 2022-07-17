from peewee import *

db = SqliteDatabase('pilots.db')


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
    team = ForeignKeyField(Team, backref='pilot', )
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
            Team.create(abbr=team_abbr, name=team[0], engine=team[1], nation=team[2],
                        base=team[3])
        except IntegrityError:
            pass


def create_pilots(pilots, pilot_nations):
    for ab, pi in pilots.items():
        try:
            Pilot.create(abbr=ab, name=pi.name, team=pi.team[:3].upper(), nation=pilot_nations[ab])
        except IntegrityError:
            pass


def create_times(pilots):
    for ab, pi in pilots.items():
        try:
            SessionTime.create(pilot_abbr=ab, lap_time=pi.lap_time)
        except IntegrityError:
            pass
