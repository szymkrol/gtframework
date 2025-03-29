import math


class GameTree:
    def __init__(self, root, root_game):
        self._root_game = root_game.get_semi_copy()
        self._root = root

    def get_root(self):
        return self._root

    def get_root_game_copy(self):
        return self._root_game.get_semi_copy()


class TreeNode:
    def __init__(self, exploration_const, parent=None, move_from_parent=None):
        self._exploration_const = exploration_const
        self._parent = parent
        self._move_from_parent = move_from_parent
        self._num_wins = 0
        self._num_sims = 0
        self._children = []

    def get_parent(self):
        return self._parent

    def get_move_from_parent(self):
        return self._move_from_parent

    def get_num_wins(self):
        return self._num_wins

    def get_num_sims(self):
        return self._num_sims

    def increment_num_wins(self):
        self._num_wins += 1

    def increment_num_sims(self):
        self._num_sims += 1

    def append_child(self, child):
        self._children.append(child)

    def add_child(self, move_from_parent):
        child = TreeNode(self._exploration_const, self, move_from_parent)
        self._children.append(child)

    def create_children(self, available_moves):
        if not self._children:
            for move in available_moves:
                self._children.append(TreeNode(self._exploration_const, self, move))

    def get_children(self):
        return self._children

    def get_UCB(self):
        if self.get_num_sims() == 0:
            return float('inf')
        if self._parent.get_num_sims() == 0:
            return float('-inf')
        return (self.get_num_wins() / self.get_num_sims()) + self._exploration_const * math.sqrt(
            math.log(self._parent.get_num_sims()) / self.get_num_sims())


    def get_max_UCB_child(self):
        best_child = self._children[0]
        max_UCB = best_child.get_UCB
        for child in self._children:
            if child.get_UCB() > max_UCB:
                max_UCB = child.get_UCB()
                best_child = child
        return best_child
