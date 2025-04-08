from typing import Any, Self

def get_neigh_coords(coord: tuple[int, int], size: int) -> list[tuple[int, int]]:
    x, y = coord
    neighbors = []

    differences = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in differences:
        nx, ny = x + dx, y + dy
        if 0 <= nx < size and 0 <= ny < size:
            neighbors.append((nx, ny))
    return neighbors


class LatticeNode:
    def __init__(self, coords: tuple[int, int], attr: str='') -> None:
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
        if neigh is None:
            return
        neigh.add_neighbour(self)
        self.add_neighbour(neigh)

    def remove_connection(self, neigh: Self) -> None:
        if neigh is None:
            return
        if self not in neigh.get_neighbours():
            return
        neigh.remove_neighbour(self)
        self.remove_neighbour(neigh)

    def get_coords(self) -> tuple[int, int]:
        return self._coords

    def is_closed(self) -> bool:
        if len(self._neighbours) == 0:
            return True
        else:
            return False


class Lattice:
    def __init__(self, size: int) -> None:
        self._board = [([None] * size).copy() for _ in range(size)]
        self._size = size

        for i in range(size):
            for j in range(size):
                if (i == 0 or i == size - 1) and (j == 0 or j == size - 1):
                    self._board[i][j] = None
                else:
                    if i == 0 or i == size - 1 or j == 0 or j == size - 1:
                        new_node = LatticeNode((i, j), 'b')
                    else:
                        new_node = LatticeNode((i, j), '_')
                    neighs = get_neigh_coords((i, j), self._size)
                    for neigh in neighs:
                        if self.get_field(neigh) is not None:
                            if new_node.get_attribute() != 'b' or self.get_field(neigh).get_attribute() != 'b':
                                new_node.add_connection(self.get_field(neigh))
                    self._board[i][j] = new_node

    def get_field(self, coord: tuple[int, int]) -> LatticeNode:
        return self._board[coord[0]][coord[1]]

    def get_connections(self, coord: tuple[int, int]) -> list[LatticeNode]:
        node = self.get_field(coord)
        if node is None:
            return []
        else:
            return node.get_neighbours()

    def get_lower_right_connections(self, coord: tuple[int, int]) -> list[LatticeNode]:
        conn = self.get_connections(coord)
        x, y = self.get_field(coord).get_coords()
        good_neighs = []
        for neigh in conn:
            x_n, y_n = neigh.get_coords()
            if x_n > x or y_n > y:
                good_neighs.append(neigh)
        return good_neighs
    def are_connected(self, coord1: tuple[int, int], coord2: tuple[int, int]) -> bool:
        return self.get_field(coord1) in self.get_connections(coord2)

    def __str__(self) -> str:
        output = ''
        for i in range(2*self._size-1):
            for j in range(2*self._size-1):
                if i % 2 == 0:
                    if j % 2 == 0:
                        field = self.get_field((int(i/2), int(j/2)))
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
                        if self.are_connected((int((i - 1) / 2), int(j / 2)), (int((i + 1) / 2), int(j  / 2))):
                            output += '|'
                        else:
                            output += ' '
            output += '\n'
        return output
