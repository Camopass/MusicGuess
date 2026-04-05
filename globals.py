from enum import IntEnum
from json import dumps

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 6967
class GameStateIDs(IntEnum):
    IN_ROUND = 1
    NOT_IN_ROUND = 0

START_MESSAGE = dumps({"type": "gamestate",
                 "state": GameStateIDs.IN_ROUND}).encode("utf-8")
END_ROUND_MESSAGE = dumps({"type": "gamestate",
                 "state": GameStateIDs.NOT_IN_ROUND}).encode("utf-8")
