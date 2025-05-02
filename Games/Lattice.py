from typing import Any, Self
from collections.abc import Hashable


def get_neigh_coords(coord: tuple[int, int], size: int) -> list[tuple[int, int]]:
    x, y = coord
    diffs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    return [(x + dx, y + dy) for dx, dy in diffs if 0 <= x + dx < size and 0 <= y + dy < size]


class LatticeNode:
    __slots__ = ('_neighbours', '_attribute', '_coords')

    def __init__(self, coords: tuple[int, int], attr: str = '') -> None:
        self._neighbours = []
        self._attribute = attr
        self._coords = coords

    def get_attribute(self) -> Any:
        return self._attribute

    def set_attribute(self, attr: Any) -> None:
        self._attribute = attr

    def add_neighbour(self, neigh: Self) -> None:
        self._neighbours.append(neigh)

    def remove_neighbour(self, neigh: Self) -> None:
        self._neighbours.remove(neigh)

    def get_neighbours(self) -> list[Self]:
        return self._neighbours

    def add_connection(self, neigh: Self) -> None:
        if neigh:
            neigh.add_neighbour(self)
            self.add_neighbour(neigh)

    def remove_connection(self, neigh: Self) -> None:
        if neigh and self in neigh.get_neighbours():
            neigh.remove_neighbour(self)
            self.remove_neighbour(neigh)

    def get_coords(self) -> tuple[int, int]:
        return self._coords

    def is_closed(self) -> bool:
        return not self._neighbours


class Lattice:
    def __init__(self, size: int) -> None:
        self._board: list[list[None | LatticeNode]] = [([None] * size).copy() for _ in range(size)]
        self._size = size

        for i in range(size):
            for j in range(size):
                if (i == 0 or i == size - 1) and (j == 0 or j == size - 1):
                    continue  # corners stay None
                attr = 'b' if i == 0 or i == size - 1 or j == 0 or j == size - 1 else '_'
                new_node = LatticeNode((i, j), attr)
                for ni, nj in get_neigh_coords((i, j), size):
                    neighbor = self._board[ni][nj]
                    if neighbor and (new_node.get_attribute() != 'b' or neighbor.get_attribute() != 'b'):
                        new_node.add_connection(neighbor)
                self._board[i][j] = new_node

    def get_field(self, coord: tuple[int, int]) -> LatticeNode | None:
        return self._board[coord[0]][coord[1]]

    def get_connections(self, coord: tuple[int, int]) -> list[LatticeNode]:
        node = self.get_field(coord)
        return node.get_neighbours() if node else []

    def get_lower_right_connections(self, coord: tuple[int, int]) -> list[LatticeNode]:
        node = self.get_field(coord)
        if node is None:
            return []
        x, y = node.get_coords()
        return [n for n in node.get_neighbours() if n.get_coords()[0] > x or n.get_coords()[1] > y]

    def are_connected(self, coord1: tuple[int, int], coord2: tuple[int, int]) -> bool:
        node2 = self.get_field(coord2)
        return node2 and self.get_field(coord1) in node2.get_neighbours()

    def get_state_repr(self) -> Hashable:
        representation = [self._size]
        for i in range(self._size):
            for j in range(self._size):
                node = self.get_field((i, j))
                if node is None:
                    continue
                if i + 1 < self._size:
                    representation.append(1 if self.are_connected((i, j), (i+1, j)) else 0)
                if j + 1 < self._size:
                    representation.append(1 if self.are_connected((i, j), (i, j+1)) else 0)
                return tuple(representation)

    def __str__(self) -> str:
        output = ''
        for i in range(2 * self._size - 1):
            for j in range(2 * self._size - 1):
                if i % 2 == 0:
                    if j % 2 == 0:
                        field = self.get_field((int(i / 2), int(j / 2)))
                        if field is None:
                            output += "N"
                        else:
                            output += field.get_attribute()
                    else:
                        if self.are_connected((int(i / 2), int((j - 1) / 2)), (int(i / 2), int((j + 1) / 2))):
                            output += '-'
                        else:
                            output += ' '
                else:
                    if j % 2 == 1:
                        output += ' '
                    else:
                        if self.are_connected((int((i - 1) / 2), int(j / 2)), (int((i + 1) / 2), int(j / 2))):
                            output += '|'
                        else:
                            output += ' '
            output += '\n'
        return output
