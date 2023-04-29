#!/usr/bin/python3
"""retrieve user objects to api"""

# import sys
from flask import jsonify, make_response, abort, request
# sys.path.insert(1, "/tmp_api/AirBnB_clone_v3")
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users/', methods=['GET'], strict_slashes=False)
def all_users():
    """retrieve all user object"""
    _list_of_dict = []
    for user in list(storage.all("User").values()):
        _list_of_dict.append(user.to_dict())
    return jsonify(_list_of_dict)


@app_views.route('/users/<user_id>/', methods=['GET'], strict_slashes=False)
def single_user(user_id):
    """if user_id not None return singel user_info"""
    user_info = storage.get("User", user_id)
    if user_info is not None:
        return jsonify(user_info.to_dict())
    abort(404)


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def post_user():
    """create new user"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({"error": "Missing email"}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({"error": "Missing password"}), 400)
    new_user = User(**request.get_json())
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """if user_id is not None find and update user"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    update_user = storage.get("User", user_id)
    if update_user is not None:
        for key, value in request.get_json().items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(update_user, key, value)
        update_user.save()
        return make_response(jsonify(update_user.to_dict()), 200)
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """if user_id is not None find and \
        delete uer_info"""
    user_info = storage.get("User", user_id)
    if user_info is None:
        abort(404)
    user_info.delete()
    storage.save()
    return make_response(jsonify({}), 200)
