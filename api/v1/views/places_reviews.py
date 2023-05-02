#!/usr/bin/python3
"""create api for Review same as State"""

from flask import jsonify, abort, make_response, request
# import sys
# sys.path.insert(1, "/tmp_api/AirBnB_clone_v3")
from models import storage
from models.user import User
from models.review import Review
from models.place import Place
from api.v1.views import app_views


@app_views.route(
    '/places/<place_id>/reviews/', methods=['GET'], strict_slashes=False)
def review_by_place(place_id):
    """list all reviews"""
    place = storage.get("Place", place_id)
    if place is not None:
        _list_of_review = []
        for review in place.reviews:
            _list_of_review.append(review.to_dict())
        return jsonify(_list_of_review)
    else:
        abort(404)


@app_views.route(
    '/reviews/<review_id>/', methods=['GET'], strict_slashes=False)
def get_review(review_id=None):
    """retrieve review by id"""
    review_obj = storage.get("Review", review_id)
    if review_obj is not None:
        return jsonify(review_obj.to_dict())
    else:
        abort(404)


@app_views.route(
    '/places/<place_id>/reviews/', methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """post new review"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'text' not in request.get_json():
        return make_response(jsonify({"error": "Missing text"}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    kwargs = request.get_json()
    user_id = kwargs['user_id']
    kwargs['place_id'] = place_id
    if storage.get("User", user_id) is None:
        abort(404)
    if storage.get("Place", place_id)is None:
        abort(404)
    new_review = Review(**kwargs)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route(
    '/reviews/<review_id>/', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """if place_id is not None find and update review"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    update_review = storage.get("Review", review_id)
    if update_review is not None:
        for key, value in request.get_json().items():
            if key not in \
                    ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
                setattr(update_review, key, value)
        update_review.save()
        return make_response(jsonify(update_review.to_dict()), 200)
    else:
        abort(404)


@app_views.route(
    '/reviews/<review_id>/', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """if review_id is not None find and \
        delete review_info"""
    review_info = storage.get("Review", review_id)
    if review_info is None:
        abort(404)
    review_info.delete()
    storage.save()
    return make_response(jsonify({}), 200)
