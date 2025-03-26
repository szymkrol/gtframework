from abc import ABC, abstractmethod

class Player:
    def __init__(self, id, attributes=None):
        self.__id = id
        # Optional attributes
        self.__attributes = attributes

    def get_id(self):
        return self.__id

    def get_attributes(self):
        return self.__attributes
