#!/usr/bin/python3
"""create api for PLACE same as State"""

from flask import jsonify, abort, make_response, request
import sys
sys.path.insert(1, "/tmp_api/AirBnB_clone_v3")
from models import storage
from models.city import City
from models.place import Place
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places/',\
    methods=['GET'], strict_slashes=False)
def place_by_city(city_id):
    """list all places"""
    city = storage.get("City", city_id)
    if city is not None:
        _list_of_city = [] 
        for place in city.places:
            _list_of_city.append(place.to_dict())
        return jsonify(_list_of_city)
    abort(404)


@app_views.route('/places/<place_id>/', methods=['GET'],\
    strict_slashes=False)
def get_place(place_id=None):
    """retrieve place by id"""
    place = storage.get("Place", place_id)
    print(dir(place))
    if place is not None:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/', methods=['GET'], strict_slashes=False)
def all_tmp_places():
    """retrieve all state object"""
    _list_of_dict = []
    for city in list(storage.all("Place").values()):
        _list_of_dict.append(city.to_dict())
    return jsonify(_list_of_dict)


@app_views.route('/cities/<city_id>/places/', methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """post new state"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    kwargs = request.get_json()
    kwargs['city_id'] = city_id
    user_id = kwargs['user_id']
    if not storage.get("User", user_id):
        abort(404)
    new_place = Place(**kwargs) # request.get_json())
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>/',\
    methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """if place_id is not None find and update place"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    update_place = storage.get("Place", place_id)
    if update_place is not None:
        for key, value in request.get_json().items():
            if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
                setattr(update_city, key, value)
        update_city.save()
        return make_response(jsonify(update_city.to_dict()), 200)
    else:
        abort(404)


@app_views.route('/places/<place_id>/',\
    methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """if place_id is not None find and \
        delete place_info"""
    place_info = storage.get("Place", place_id)
    if place_info is None:
        abort(404)
    place_info.delete()
    storage.save()
    return make_response(jsonify({}), 200)
