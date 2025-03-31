def get_neigh_coords(coord, size):
    x, y = coord
    neighbors = []

    differences = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in differences:
        nx, ny = x + dx, y + dy
        if 0 <= nx < size and 0 <= ny < size:
            neighbors.append((nx, ny))
    return neighbors


class LatticeNode:
    def __init__(self, coords, attr=''):
        self._neighbours = []
        self._attribute = attr
        self._coords = coords

    def get_attribute(self):
        return self._attribute

    def set_attribute(self, attr):
        self._attribute = attr

    def add_neighbour(self, neigh):
        self._neighbours.append(neigh)

    def remove_neighbour(self, neigh):
        self._neighbours.remove(neigh)

    def get_neighbours(self):
        return self._neighbours

    def add_connection(self, neigh):
        if neigh is None:
            return
        neigh.add_neighbour(self)
        self.add_neighbour(neigh)

    def remove_connection(self, neigh):
        if neigh is None:
            return
        if self not in neigh.get_neighbours():
            return
        neigh.remove_neighbour(self)
        self.remove_neighbour(neigh)
    def get_coords(self):
        return self._coords

    def is_closed(self):
        if len(self._neighbours) == 0:
            return True
        else:
            return False


class Lattice:
    def __init__(self, size):
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
                        new_node.add_connection(self.get_field(neigh))
                    self._board[i][j] = new_node

    def get_field(self, coord):
        return self._board[coord[0]][coord[1]]

    def get_connections(self, coord):
        return self.get_field(coord).get_neighbours()

    def get_lower_right_connections(self, coord):
        conn = self.get_connections(coord)
        x, y = self.get_field(coord).get_coords()
        good_neighs = []
        for neigh in conn:
            x_n, y_n = neigh.get_coords()
            if x_n > x or y_n > y:
                good_neighs.append(neigh)
        return good_neighs
