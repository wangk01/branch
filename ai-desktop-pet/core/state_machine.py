"""行为状态定义与状态机"""
from enum import Enum, auto


class PetState(Enum):
    IDLE = auto()
    WALK = auto()
    SLEEP = auto()
    DROWSY = auto()
    PLAY = auto()
    EAT = auto()
    BATH = auto()
    STROKE = auto()
    DOUBLE_CLICK = auto()
    DIRTY = auto()
    HUNGRY = auto()
    SAD = auto()
    CARRIED = auto()
    SIDEBAR_IDLE = auto()


class StateMachine:
    """管理宠物行为状态迁移。交互事件优先级高于自主行为。"""

    def __init__(self, initial: PetState = PetState.IDLE):
        self._state = initial
        self._listeners = []

    @property
    def state(self) -> PetState:
        return self._state

    def add_listener(self, fn):
        self._listeners.append(fn)

    def set_state(self, new_state: PetState) -> bool:
        if new_state == self._state:
            return False
        old = self._state
        self._state = new_state
        for fn in self._listeners:
            fn(old, new_state)
        return True

    def get_state(self) -> PetState:
        return self._state
