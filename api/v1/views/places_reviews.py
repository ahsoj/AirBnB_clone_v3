#!/usr/bin/python3
"""create api for Review same as State"""

from flask import jsonify, abort, make_response, request
import sys
sys.path.insert(1, "/tmp_api/AirBnB_clone_v3")
from models import storage
from models.city import Review
from models.place import Place
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews/',\
    methods=['GET'], strict_slashes=False)
def review_by_place(place_id):
    """list all reviews"""
    place = storage.get("Place", place_id)
    if place is not None:
        _list_of_city = [] 
        for review in place.reviews:
            _list_of_city.append(place.to_dict())
        return jsonify(_list_of_city)
    abort(404)


@app_views.route('/reviews/<review_id>/', methods=['GET'],\
    strict_slashes=False)
def get_review(review_id=None):
    """retrieve review by id"""
    review = storage.get("Review", review_id)
    print(dir(review))
    if review is not None:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/', methods=['GET'], strict_slashes=False)
def all_tmp_reviews():
    """retrieve all state object"""
    _list_of_dict = []
    for review in list(storage.all("Review").values()):
        _list_of_dict.append(review.to_dict())
    return jsonify(_list_of_dict)


@app_views.route('/places/<place_id>/reviews/', methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """post new review"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    kwargs = request.get_json()
    user_id = kwargs['user_id']
    if not storage.get("User", user_id):
        abort(404)
    if not storage.get("Place", place_id):
        abort(404)
    new_review = Review(**kwargs) # request.get_json())
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


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
