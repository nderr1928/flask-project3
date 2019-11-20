import models
from flask import Blueprint, jsonify, request
from flask_login import current_user
from playhouse.shortcuts import model_to_dict

companion = Blueprint('companions', 'companion')


#List all party
@companion.route('/', methods=['GET'])
def list_party():
	print(current_user)
	try:
		party = [model_to_dict(d) for d in models.Companion.select()]
		return jsonify(data=party, status={'code': 200, 'message': 'Success'})
	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'Error getting the resources'})


#List individual companion based on ID
@companion.route('/<companion_id>/', methods=['GET'])
def get_companion(companion_id):
	companion = model_to_dict(models.Companion.get(id=companion_id))
	return jsonify(companion)


#Adding a companion to party
@companion.route('/', methods=['POST'])
def create_companion():
	payload = request.get_json()
	created_companion = models.Companion.create(**payload)
	created_companion_dict = model_to_dict(created_companion)
	return jsonify(data=created_companion_dict, status={'code': 201, 'message': 'success'})

#Delete companion
@companion.route('/', methods=['DELETE'])
def delete_companion(id):
	deleted_companion = models.Companion.get(id=id)
	deleted_companion.delete()
	return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})

#Edit Route
@companion.route('/<companion_id>/', methods=['PUT'])
def update_companion(companion_id):
    edit_companion = request.get_json()

    updated_companion = models.Companion.update(
        name=new_companion_data['name']
    ).where(models.Companion.id==companion_id).execute()
    update_companion_dict = model_to_dict(models.Companion.get(id=companion_id))
    return jsonify(data=update_companion_dict, status={'code': 200, 'message': 'success'})








