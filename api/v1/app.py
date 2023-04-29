#!/usr/bin/python3
"""create v1 api"""

from flask import Flask, jsonify, make_response
import sys
import os
sys.path.insert(1, "/tmp_api/AirBnB_clone_v3")
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)

host = os.environ.get('HBNB_API_HOST') or '0.0.0.0'
port = os.environ.get('HBNB_API_PORT') or 5000


@app.errorhandler(404)
def not_found(error):
    """ json 404 page """
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def teardownContext(exp):
    """close storage after routing finished """
    storage.close()


if __name__ == "__main__":
    app.run(host=str(host), port=int(port), debug=True, threaded=True)
