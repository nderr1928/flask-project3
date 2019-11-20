from peewee import *
from flask_login import UserMixin

DATABASE = SqliteDatabase('project3.sqlite')


class Companion(Model):
	name = CharField()
	race = CharField()
	char_class = CharField()
	level = IntegerField(default=1)
	experience = IntegerField()
	health = IntegerField(default=10)
	damage = IntegerField(default=1)
	image = CharField();

	class Meta:
		db_table = 'companions'
		database = DATABASE

class Location(Model):
	name = CharField()
	description = CharField()


	class Meta:
		db_table = 'locations'
		database = DATABASE

class Item(Model):
	name = CharField()
	description = CharField()
	effect = CharField()
	location = ForeignKeyField(Location, backref='items')

	class Meta:
		db_table = 'items'
		database = DATABASE

class Profile(Model):
	user_id = ForeignKeyField(User, primary_key=True)
	display_name = CharField();
	main_character = ForeignKeyField(Companion, backref='profiles') 
	party = ForeignKeyField(Companion, backref='profiles')  
	gold = IntegerField(default=0)
	inventory = ForeignKeyField(Item, backref='profiles') 

	class Meta:
		db_table = 'profiles'
		database = DATABASE

class Monster(Model):
	mons_type = CharField()
	level = IntegerField(default=1)
	health = IntegerField(default=1)
	image = CharField()
	location = ForeignKeyField(Location, backref='monster')

	class Meta:
		db_table = 'monsters'
		database = DATABASE

class User(UserMixin, Model):
	email = CharField(unique=True)
	password = CharField()
	display_name = CharField();
	main_character = ForeignKeyField(Companion, backref='profiles') 
	party = ForeignKeyField(Companion, backref='profiles')  
	gold = IntegerField(default=0)
	inventory = ForeignKeyField(Item, backref='profiles') 

	def __str__(self):
		return '<User: {}, id: {}>'.format(self.email, self.id)

	def __repr__(self):
		return '<User: {}, id: {}>'.format(self.email, self.id)

	class Meta:
		db_table = 'users'
		database = DATABASE

def initialize(): 
	DATABASE.connect()
	DATABASE.create_tables([User, Profile, Companion, Item, Monster, Location], safe=True)

	#Populating our tables upon initialization
	location_pop = [
	{'name': 'Market', 'description': 'Exchange gold for items'},
	{'name': 'Dungeon', 'description': 'Battle monsters for experience and gold'}]
	Location.insert_many(location_pop).execute()

	monster_pop = [
    {'mons_type': 'Slime', 'level': 1, 'health': 1, 'image': 'x', 'location': 2},
    {'mons_type': 'Wolf', 'level': 5, 'health': 5, 'image': 'x', 'location': 2},
    {'mons_type': 'Dragon', 'level': 10, 'health': 10, 'image': 'x', 'location': 2}]
	Monster.insert_many(monster_pop).execute()

	item_pop = [
	{'name': 'Minor Healing Potion', 'description': 'Heals a small amount of health.', 'effect': 1, 'location': 1},
    {'name': 'Healing Potion', 'description': 'Heals a substantial amount of health.', 'effect': 5, 'location': 1},
    {'name': 'Super Healing Potion', 'description': 'Heals a large amount of health.', 'effect': 10, 'location': 1}]
	Item.insert_many(item_pop).execute()
	#End of population queries 

	print("Database tables and data have been created")
	DATABASE.close()