from peewee import *
from datetime import date
import os

os.remove('people.db')

db = SqliteDatabase('people.db')


class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = db  # This model uses the "people.db" database.


class Pet(Model):
    owner = ForeignKeyField(Person, backref='pets')
    name = CharField()
    animal_type = CharField()

    class Meta:
        database = db  # this model uses the "people.db" database


db.connect()
db.create_tables([Person, Pet])

uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15))
uncle_bob.save()  # bob is now stored in the database
# Returns: 1
grandma = Person.create(name='Grandma', birthday=date(1935, 3, 1))
herb = Person.create(name='Herb', birthday=date(1950, 5, 5))

grandma.name = 'Grandma L.'
grandma.save()

bob_kitty = Pet.create(owner=uncle_bob, name='Kitty', animal_type='cat')
herb_fido = Pet.create(owner=herb, name='Fido', animal_type='dog')
herb_mittens = Pet.create(owner=herb, name='Mittens', animal_type='cat')
herb_mittens_jr = Pet.create(owner=herb, name='Mittens Jr', animal_type='cat')

herb_mittens.delete_instance()
herb_fido.owner = uncle_bob
herb_fido.save()

query = (Pet
         .select(Pet, Person)
         .join(Person))

# for pet in query:
#     print(pet.name, pet.owner.name)

tryy = Person.select(Person, Pet).join(Pet).group_by(Person, JOIN.LEFT_OUTER)
query = Person.select(Person, Pet).join(Pet, JOIN.LEFT_OUTER).order_by(Person.name, Pet.name)
for person in query:
    if person.pets.count():
        print(person.name, type(person.pets), type(person.pet))
    else:
        print(person.name, person.pets.count())

