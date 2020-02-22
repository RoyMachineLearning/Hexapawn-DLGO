import enum
from collections import namedtuple

__all__ = [
    'Player',
    'Point',
]


class Player(enum.Enum):
    x = 'x'
    o = 'o'

    @property
    def other(self):
        return Player.x if self == Player.o else Player.o

    @property
    def prefix(self):
        return 'x' if self == Player.x else 'o'

    @staticmethod
    def from_prefix(prefix):
        return Player.x if prefix == 'x' else Player.o


class Point(namedtuple('Point', 'row col')):
    def __deepcopy__(self, memodict={}):
        # These are very immutable.
        return self