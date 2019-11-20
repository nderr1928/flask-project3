import models
from flask import Blueprint, jsonify, request
from flask_login import current_user
from playhouse.shortcuts import model_to_dict

profile = Blueprint('profiles', 'profile')


#List all profiles
@profile.route('/', methods=['GET'])
def list_profiles():
	print(current_user)
	try:
		all_profiles = [model_to_dict(d) for d in models.Profile.select()]
		return jsonify(data=all_profiles, status={'code': 200, 'message': 'Success'})
	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'Error getting the resources'})


#List individual profile based on ID
@profile.route('/<profile_id>/', methods=['GET'])
def get_profile(profile_id):
	profile = model_to_dict(models.Profile.get(id=profile_id))
	return jsonify(profile)


#Creation of profile
@profile.route('/', methods=['POST'])
def create_profile():
	payload = request.get_json()
	created_profile = models.Profile.create(**payload)
	created_profile_dict = model_to_dict(created_profile)
	return jsonify(data=created_profile_dict, status={'code': 201, 'message': 'success'})

#Delete profile
@profile.route('/', methods=['DELETE'])
def delete_profile(id):
	deleted_profile = models.Profile.get(id=id)
	deleted_profile.delete()
	return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})

#Edit Route
@profile.route('/<profile_id>/', methods=['PUT'])
def update_profile(profile_id):
    edit_profile = request.get_json()

    updated_profile = models.Profile.update(
        display_name=new_profile_data['name']
    ).where(models.Profile.id==profile_id).execute()
    update_profile_dict = model_to_dict(models.Profile.get(id=profile_id))
    return jsonify(data=update_profile_dict, status={'code': 200, 'message': 'success'})