#!/usr/bin/python3
""" Test .get() and .count() methods
"""
import sys
sys.path.insert(1, '/tmp_api/AirBnB_clone_v3')
from models import storage
from models.state import State

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

first_state_id = list(storage.all(State).values())[0].id
print("First state: {}".format(storage.get(State, first_state_id)))
