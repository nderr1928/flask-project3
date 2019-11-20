from peewee import *
from flask_login import UserMixin

DATABASE = SqliteDatabase('project3.sqlite')

class User(UserMixin, Model):
	email = CharField(unique=True)
	password = CharField()

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
	experience = IntegerField()
	health = IntegerField(default=10)
	damage = IntegerField(default=1)
	image = CharField();

	class Meta:
		db_table = 'companions'
		database = DATABASE

class Item(Model):
	name = CharField()
	description = CharField()
	effect = CharField()

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

	class Meta:
		db_table = 'monsters'
		database = DATABASE

class Location(Model):
	name = CharField()
	monsters = ForeignKeyField(Monster, backref='locations')
	items = ForeignKeyField(Item, backref='locations')

	class Meta:
		db_table = 'locations'
		database = DATABASE

def initialize(): 
	DATABASE.connect()
	DATABASE.create_tables([User, Profile, Companion, Item, Monster, Location])
	monster_pop = [
    {'mons_type': 'Slime', 'level': '1', 'health': '1', 'image': 'x'},
    {'mons_type': 'Wolf', 'level': '5', 'health': '5', 'image': 'x'},
    {'mons_type': 'Dragon', 'level': '10', 'health': '10', 'image': 'x'}]
	Monster.insert_many(monster_pop).execute()

	item_pop = [
	{'name': 'Minor Healing Potion', 'description': 'Heals a small amount of health.', 'effect': '1'},
    {'name': 'Healing Potion', 'description': 'Heals a substantial amount of health.', 'effect': '5'},
    {'name': 'Super Healing Potion', 'description': 'Heals a large amount of health.', 'effect': '10'}]
	Item.insert_many(item_pop).execute()

	

	print("Database tables and data have been created")
	DATABASE.close()