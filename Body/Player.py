from typing import Any


class Player:
    def __init__(self, id: int, attributes: Any=None) -> None:
        self._id = id
        # Optional attributes
        self._attributes = attributes

    def get_id(self) -> int:
        return self._id

    def get_attributes(self) -> Any:
        return self._attributes
