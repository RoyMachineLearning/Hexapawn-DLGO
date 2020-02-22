import copy

from .hxptypes import Player, Point

__all__ = [
    'Board',
    'GameState',
    'Move',
]


class IllegalMoveError(Exception):
    pass


BOARD_SIZE = 3
ROWS = tuple(range(1, BOARD_SIZE + 1))
COLS = tuple(range(1, BOARD_SIZE + 1))
PLAYERS = (Player.x, Player.o)


class Board:
    def __init__(self):
        self.minion_map = {}
        self.minion_map.update({'{}{}'.format(Player.x.prefix, idx): Point(1, idx) for idx in COLS})
        self.minion_map.update({'{}{}'.format(Player.o.prefix, idx): Point(BOARD_SIZE, idx) for idx in COLS})
        self.next_player = Player.x
        self.possibles = {}
        self.win = {}
        self.update()

    def place(self, player, move):
        assert move in self.possibles[player]

        to_pop = self.grid.get(move.point)
        if to_pop:
            self.minion_map.pop(to_pop)
        self.minion_map[move.minion] = move.point
        self.next_player = player.other
        self.update()

    @staticmethod
    def is_on_grid(point):
        return 1 <= point.row <= BOARD_SIZE and \
            1 <= point.col <= BOARD_SIZE

    def get(self, point):
        return self.grid.get(point)

    def _render_grid(self):
        self.grid = {val: key for key, val in self.minion_map.items()}

    def update(self):
        def _minions(player):
            return ('{}{}'.format(player.prefix, idx) for idx in COLS)

        def _row_diff(player):
            return 1 if player == Player.x else -1

        def _row_reach(player):
            return 1 if player == Player.o else BOARD_SIZE

        def _move_point(point, row_diff, col_diff):
            return Point(point[0] + row_diff, point[1] + col_diff)

        def _check_capture(player, minion, col_diff):
            row_diff = _row_diff(player)
            new_point = _move_point(self.minion_map[minion], row_diff, col_diff)
            occupant = self.grid.get(new_point)
            if occupant and Player.from_prefix(occupant[:1]) != player:
                return Move(minion, new_point)
            else:
                return None

        def _check_forward(player, minion):
            row_diff = _row_diff(player)
            new_point = _move_point(self.minion_map[minion], row_diff, 0)
            if not self.grid.get(new_point):
                return Move(minion, new_point)
            else:
                return None

        def _minion_possibles(player, minion):
            return list(filter(bool, (
                [_check_capture(player, minion, col_diff) for col_diff in [-1, 1]] +
                [_check_forward(player, minion)])))

        def _minion_reach(player, minion):
            return self.minion_map[minion][0] == _row_reach(player)

        def _analyze_player(player):
            alive_minions = list(filter(lambda m: m in self.minion_map, _minions(player)))
            possibles = sum([_minion_possibles(player, minion) for minion in alive_minions], [])
            reach = any([_minion_reach(player, minion) for minion in alive_minions])

            stuck = (not possibles) and player == self.next_player
            die = (not alive_minions) or stuck

            return possibles, reach, die

        self._render_grid()

        possibles = {}
        win = {player: False for player in PLAYERS}
        for player in PLAYERS:
            possibles[player], reach, die = _analyze_player(player)
            win[player] |= reach
            win[player.other] |= die

        self.possibles.update(possibles)
        self.win.update(win)


class Move:
    def __init__(self, minion, point):
        self.minion = minion
        self.point = point

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.minion == other.minion and self.point == other.point
        return False

    def __repr__(self):
        return 'Move {} to {}'.format(self.minion, self.point)


class GameState:
    def __init__(self, board, next_player, move):
        self.board = board
        self.next_player = next_player
        self.last_move = move

    def apply_move(self, move):
        """Return the new GameState after applying the move."""
        next_board = copy.deepcopy(self.board)
        next_board.place(self.next_player, move)
        return GameState(next_board, self.next_player.other, move)

    @classmethod
    def new_game(cls):
        board = Board()
        return GameState(board, Player.x, None)

    def legal_moves(self):
        return self.board.possibles[self.next_player]

    def is_over(self):
        return any(self.board.win.values())

    def winner(self):
        return next(p for p in PLAYERS if self.board.win[p])