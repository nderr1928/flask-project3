import models
from flask import Blueprint, jsonify, request
from flask_login import current_user
from playhouse.shortcuts import model_to_dict

location = Blueprint('locations', 'location')


#List all locations
@location.route('/', methods=['GET'])
def list_location():
	try:
		locations = [model_to_dict(l) for l in models.Location.select()]
		return jsonify(data=locations, status={'code': 200, 'message': 'Success'})
	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'Error getting the resources'})


#List individual locations based on ID
@location.route('/<location_id>/', methods=['GET'])
def get_location(location_id):
	location = model_to_dict(models.Location.get(id=location_id))
	return jsonify(companion)

