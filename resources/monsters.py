import models
from flask import Blueprint, jsonify, request
from flask_login import current_user
from playhouse.shortcuts import model_to_dict

monster = Blueprint('monsters', 'monster')


#Grab a monster
@monster.route('/<monster_id>/', methods=['GET'])
def get_location(monster_id):
	monster = model_to_dict(models.Monster.get(id=monster_id))
	return jsonify(monster)