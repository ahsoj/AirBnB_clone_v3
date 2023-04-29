#!/usr/bin/python3
"""initiaize the api"""

from flask import jsonify
import sys
sys.path.insert(1, "/tmp_api/AirBnB_clone_v3")
from api.v1.views import app_views # _classes
from models import storage

_classes = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
}


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def checkStatus():
    """return api status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def count_stats():
    """retireve number of each objects by type"""
    _dict = {}
    for k, v in _classes.items():
        _dict[k] = storage.count(v)
    return jsonify(_dict)
