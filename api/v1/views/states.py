#!/usr/bin/python3
"""retrieve state objects to api"""

# import sys
from flask import jsonify, make_response, abort, request
# sys.path.insert(1, "/tmp_api/AirBnB_clone_v3")
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def all_states():
    """retrieve all state object"""
    _list_of_dict = []
    for state in list(storage.all("State").values()):
        # print(state.to_dict())
        _list_of_dict.append(state.to_dict())
    # print([_list_of_dict])
    return jsonify(_list_of_dict)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def single_state(state_id):
    """if state_id not None return singel state_info"""
    state_info = storage.get("State", state_id)
    print(dir(state_info))
    if state_info is not None:
        return jsonify(state_info.to_dict())
    abort(404)


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_state():
    """post new state"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_state = State(**request.get_json())
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """if state_id is not None find and update state"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    update_state = storage.get("State", state_id)
    if update_state is not None:
        for key, value in request.get_json().items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(update_state, key, value)
        update_state.save()
        return make_response(jsonify(update_state.to_dict()), 200)
    else:
        abort(404)

@app_views.route(
        '/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """if state_id is not None find and \
        delete state_info"""
    state_info = storage.get("State", state_id)
    if state_info is None:
        abort(404)
    state_info.delete()
    storage.save()
    return make_response(jsonify({}), 200)
