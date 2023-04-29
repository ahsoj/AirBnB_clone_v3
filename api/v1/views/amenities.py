#!/usr/bin/python3
"""retrieve amenity objects to api"""
import sys
from flask import jsonify, make_response, abort, request
sys.path.insert(1, "/tmp_api/AirBnB_clone_v3")
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET'], strict_slashes=False)
def all_amenities():
    """retrieve all amenity object"""
    _list_of_dict = []
    for state in list(storage.all("Amenity").values()):
        # print(state.to_dict())
        _list_of_dict.append(state.to_dict())
    # print([_list_of_dict])
    return jsonify(_list_of_dict)


@app_views.route('/amenities/<amenity_id>',\
   methods=['GET'], strict_slashes=False)
def single_amenity(amenity_id):
    """if amenity_id not None return singel amenity_info"""
    amenity_info = storage.get("Amenity", amenity_id)
    if amenity_info is not None:
        return jsonify(amenity_info.to_dict())
    abort(404)


@app_views.route('/amenities/', methods=['POST'], strict_slashes=False)
def post_amenity():
    """post new amenity"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_amenity = Amenity(**request.get_json())
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',\
    methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """if user_id is not None find and update amenity"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    update_amenity = storage.get("Amenity", amenity_id)
    if update_amenity is not None:
        for key, value in request.get_json().items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(update_amenity, key, value)
        update_amenity.save()
        return make_response(jsonify(update_amenity.to_dict()), 200)
    else:
        abort(404)
    


@app_views.route('/amenities/<amenity_id>',\
    methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """if amenity_id is not None find and \
        delete amenity_info"""
    amenity_info = storage.get("Amenity", amenity_id)
    if amenity_info is None:
        abort(404)
    amenity_info.delete()
    storage.save()
    return make_response(jsonify({}), 200)
