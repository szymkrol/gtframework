from abc import ABC, abstractmethod

class Player:
    def __init__(self, id, attributes=None):
        self._id = id
        # Optional attributes
        self._attributes = attributes

    def get_id(self):
        return self._id

    def get_attributes(self):
        return self._attributes
