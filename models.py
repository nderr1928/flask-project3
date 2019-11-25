import os
import models
from playhouse.db_url import connect
from peewee import *
from flask_login import UserMixin

if 'ON_HEROKU' in os.environ:
	DATABASE = connect(os.environ.get('DATABASE_URL'))
else:
	DATABASE = SqliteDatabase('project3.sqlite')

class Location(Model):
	name = CharField()
	description = CharField()


	class Meta:
		db_table = 'locations'
		database = DATABASE

class Monster(Model):
	mons_type = CharField()
	level = IntegerField(default=1)
	health = IntegerField(default=1)
	damage = IntegerField(default=1)
	image = CharField()
	location = ForeignKeyField(Location, backref='monsters')

	class Meta:
		db_table = 'monsters'
		database = DATABASE


class User(UserMixin, Model):
	email = CharField(unique=True)
	password = CharField()
	display_name = CharField()
	gold = IntegerField(default=0)

	def __str__(self):
		return '<User: {}, id: {}>'.format(self.email, self.id)

	def __repr__(self):
		return '<User: {}, id: {}>'.format(self.email, self.id)

	class Meta:
		db_table = 'users'
		database = DATABASE

class Companion(Model):
	name = CharField()
	race = CharField()
	char_class = CharField()
	level = IntegerField(default=1)
	experience = IntegerField(default=0)
	health = IntegerField(default=10)
	damage = IntegerField(default=1)
	image = CharField()
	user = ForeignKeyField(User, backref='companions')  

	class Meta:
		db_table = 'companions'
		database = DATABASE

class Item(Model):
	item_name = CharField()
	description = CharField()
	effect = CharField()
	user = ForeignKeyField(User, backref='items')

	class Meta:
		db_table = 'items'
		database = DATABASE

def initialize(): 
	DATABASE.connect()
	DATABASE.create_tables([User, Item, Companion, Monster, Location], safe=True)

	#Populating our tables upon initialization

	numOfRowsLocations = Location.select().count()
	if numOfRowsLocations == 0:
		location_pop = [
		{'name': 'Market', 'description': 'Exchange gold for items'},
		{'name': 'Dungeon', 'description': 'Battle monsters for experience and gold'}]
		Location.insert_many(location_pop).execute()

	numOfRowsMonster = Monster.select().count()
	if numOfRowsMonster == 0:
		monster_pop = [
	    {'mons_type': 'Scout', 'level': 1, 'health': 25, 'damage': 5, 'image': '/images/Avatars/Icons/PNG/female_Cat1.png', 'location': 2},
	    {'mons_type': 'Warrior', 'level': 5, 'health': 50, 'damage': 10,'image': '/images/Avatars/Icons/PNG/female_Cat3.png', 'location': 2},
	    {'mons_type': 'Elite Guard', 'level': 10, 'health': 100,'damage': 15,'image': '/images/Avatars/Icons/PNG/male_Cat3.png', 'location': 2}]
		Monster.insert_many(monster_pop).execute()

	# numOfRowsItems = Item.select().count()
	# if numOfRowsItems == 0:
	# 	item_pop = [
	# 	{'name': 'Minor Healing Potion', 'description': 'Heals a small amount of health.', 'effect': 1, 'location': 1},
	# 	{'name': 'Healing Potion', 'description': 'Heals a substantial amount of health.', 'effect': 5, 'location': 1},
	# 	{'name': 'Super Healing Potion', 'description': 'Heals a large amount of health.', 'effect': 10, 'location': 1}]
	# 	Item.insert_many(item_pop).execute()
	#End of population queries 

	print("Database tables and data have been created")
	DATABASE.close()
