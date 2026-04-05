from enum import IntEnum

class GameState:
    pass

class StartGame(GameState):
    pass

class RoundInProgress(GameState):
    pass

class RoundResults(GameState):
    pass

class GameEnd(GameState):
    pass

class GameStateIDs(IntEnum):
    START_GAME = 0
    ROUND_IN_PROGRESS = 1
    ROUND_RESULTS = 2
    GAME_END = 3

    @staticmethod
    def from_state(state: GameState):
        if isinstance(state, StartGame): return 0
        elif isinstance(state, RoundInProgress): return 1
        elif isinstance(state, RoundResults): return 2
        elif isinstance(state, GameEnd): return 3
        return -1
    
    @staticmethod
    def to_state(id: int):
        if id == 0: return StartGame()
        elif id == 1: return RoundInProgress()
        elif id == 2: return RoundResults()
        elif id == 3: return GameEnd()
        return -1