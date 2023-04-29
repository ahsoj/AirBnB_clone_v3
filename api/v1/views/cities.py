#!/usr/bin/python3
"""create api for CITY same as State"""

from flask import jsonify, abort, make_response, request
# import sys
# sys.path.insert(1, "/tmp_api/AirBnB_clone_v3")
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route(
    '/states/<state_id>/cities/', methods=['GET'], strict_slashes=False)
def city_by_state(state_id):
    """list all cities"""
    states = storage.get("State", state_id)
    if states is not None:
        _list_of_city = []
        for city in states.cities:
            _list_of_city.append(city.to_dict())
        return jsonify(_list_of_city)
    abort(404)


@app_views.route(
    '/cities/<city_id>/', methods=['GET'], strict_slashes=False)
def get_city(city_id=None):
    """retrieve city by id"""
    city = storage.get("City", city_id)
    if city is not None:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route(
    '/states/<state_id>/cities/', methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """post new state"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    kwargs = request.get_json()
    kwargs['state_id'] = state_id
    new_city = State(**kwargs)
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>/', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """if state_id is not None find and update state"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    update_city = storage.get("City", city_id)
    if update_city is not None:
        for key, value in request.get_json().items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(update_city, key, value)
        update_city.save()
        return make_response(jsonify(update_city.to_dict()), 200)
    else:
        abort(404)


@app_views.route(
    '/cities/<city_id>/', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """if state_id is not None find and \
        delete state_info"""
    city_info = storage.get("City", city_id)
    if city_info is None:
        abort(404)
    city_info.delete()
    storage.save()
    return make_response(jsonify({}), 200)
