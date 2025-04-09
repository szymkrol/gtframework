import math
from typing import Self, Any
from Game import Game


class TreeNode:
    """
    Class characterizing a node of a Game Tree
    """

    __slots__ = (
        "_exploration_const", "_parent", "_move_from_parent",
        "_num_wins", "_num_sims", "_children"
    )

    def __init__(self, exploration_const: float, parent: Self = None, move_from_parent: Any = None):
        """

        :param exploration_const: an exploration constant used for MCTS,
        :param parent: parent TreeNode,
        :param move_from_parent: move from parent in a game represented by GameTree.
        """
        self._exploration_const = exploration_const
        self._parent = parent
        self._move_from_parent = move_from_parent
        self._num_wins = 0
        self._num_sims = 0
        self._children = []

    def get_parent(self) -> Self:
        return self._parent

    def get_move_from_parent(self) -> Any:
        return self._move_from_parent

    def get_num_wins(self) -> int:
        return self._num_wins

    def get_num_sims(self) -> int:
        return self._num_sims

    def increment_num_wins(self) -> None:
        self._num_wins += 1

    def increment_num_sims(self) -> None:
        self._num_sims += 1

    def append_child(self, child: Self) -> None:
        self._children.append(child)

    def add_child(self, move_from_parent: Any) -> None:
        self._children.append(TreeNode(self._exploration_const, self, move_from_parent))

    def create_children(self, available_moves: list[Any]) -> None:
        """Create children based on moves available from this node."""
        if not self._children:
            self._children = [TreeNode(self._exploration_const, self, move) for move in available_moves]

    def get_children(self) -> list[Self]:
        return self._children

    def get_UCB(self) -> float:
        """Return the node's UCB score used for MCTS."""
        if self._num_sims == 0:
            return float('inf')
        parent_sims = self._parent._num_sims
        if parent_sims == 0:
            return float('-inf')
        exploitation = self._num_wins / self._num_sims
        exploration = self._exploration_const * math.sqrt(math.log(parent_sims) / self._num_sims)
        return exploitation + exploration

    def get_max_UCB_child(self) -> Self:
        """Return the child with the maximum UCB score."""
        return max(self._children, key=TreeNode.get_UCB)


class GameTree:
    """
    Class stores game tree.

    Intended to use with MCTS.
    """

    def __init__(self, root: TreeNode, root_game: Game) -> None:
        """

        :param root: a root of the tree.
        :param root_game: a Game object representing game state in root
        """
        self._root_game = root_game.get_semi_copy()
        self._root = root

    def get_root(self) -> TreeNode:
        return self._root

    def get_root_game_copy(self, is_revertible: bool = True, remember_past: bool = True) -> Game:
        return self._root_game.get_semi_copy(is_revertible=is_revertible, remember_past=remember_past)
