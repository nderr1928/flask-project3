import models
from flask import Blueprint, jsonify, request
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict

user = Blueprint('users', 'user')

#Register 

@user.route('/register', methods=['POST'])
def register():
    payload = request.get_json()
    print(payload)
    if not payload['email'] or not payload['password']:
        return jsonify(status=400)

    try:

        models.User.get(models.User.email ** payload['email']) 
        return jsonify(data={}, status={'code': 400, 'message': 'A user with that email already exists.'}) 
    except models.DoesNotExist:  
        payload['password'] = generate_password_hash(payload['password']) 
        new_user = models.User.create(**payload)

        login_user(new_user)

        user_dict = model_to_dict(new_user)
        print(user_dict)
        print(type(user_dict))

        del user_dict['password']

        return jsonify(data=user_dict, status={'code': 201, 'message': 'User created'})

#Login
@user.route('/login', methods=['POST'])
def login():
    payload = request.get_json()   
    print(payload)     

    try:
        user = models.User.get(models.User.email ** payload['email'])
        user_dict = model_to_dict(user)
        
        if (check_password_hash(user_dict['password'], payload['password'])):
            del user_dict['password']
            login_user(user) 
            print('User is:', user)
            return jsonify(data=user_dict, status={'code': 200, 'message': 'User authenticated'})
        return jsonify(data={}, status={'code': 401, 'message': "Email or password is incorrect"})
    
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': "Email or password is incorrect"})


#Show individual user
@user.route('/<user_id>/', methods=['GET'])
def current_user(user_id):
    print(user_id)
    user = model_to_dict(models.User.get(id=user_id))
    return jsonify(user)



#Update user gold 
@user.route('/<user_id>/gold', methods=['PATCH'])
def update_user(user_id):
    user_data = request.get_json()
    updated_data = models.User.update(
        gold=user_data['gold']
    ).where(models.User.id==user_id).execute()
    updated_user_dict = model_to_dict(models.User.get(id=user_id))
    return jsonify(data=updated_user_dict, status={'code': 200, 'msg': 'success'})






