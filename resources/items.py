import models
from flask import Blueprint, jsonify, request
from flask_login import current_user
from playhouse.shortcuts import model_to_dict

item = Blueprint('items', 'item')


#List all items in shop
@item.route('/', methods=['GET'])
def list_items():
	try:
		all_items = [model_to_dict(l) for i in models.Item.select()]
		return jsonify(data=all_items, status={'code': 200, 'message': 'Success'})
	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'Error getting the resources'})

#create item
@item.route('/', methods=['POST'])
def create_item():
	payload = request.get_json()
	print(payload)
	payload['user'] = current_user.id
	created_item = models.Item.create(**payload)
	created_item_dict = model_to_dict(created_item)
	return jsonify(data=created_item_dict, status={'code': 201, 'message': 'success'})

#delete item
@item.route('/<id>/', methods=['DELETE'])
def delete_items(id):
	deleted_item = models.Item.get(id=id)
	deleted_item.delete()
	return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})


