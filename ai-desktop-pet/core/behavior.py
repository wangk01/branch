"""自主行为决策"""
import random

from core.attributes import AttributeSystem
from core.state_machine import PetState


class BehaviorDecider:
    """根据属性值与空闲时长决策自主行为。"""

    def __init__(self, behavior_params: dict | None = None):
        params = behavior_params or {}
        self.idle_trigger_seconds = params.get("idle_trigger_seconds", 15)
        self.probabilities = params.get(
            "behavior_probabilities",
            {"walk": 0.4, "sleep": 0.15, "play": 0.2, "drowsy": 0.05, "sad": 0.1, "hungry": 0.05, "dirty": 0.05},
        )

    def should_act(self, idle_seconds: float) -> bool:
        return idle_seconds >= self.idle_trigger_seconds

    def decide(self, attrs: AttributeSystem) -> PetState:
        """根据属性与随机权重返回下一个自主行为状态。"""
        if attrs.values["energy"] < 20:
            return PetState.SLEEP
        if attrs.values["hunger"] > 80:
            return PetState.HUNGRY
        if attrs.values["clean"] < 20:
            return PetState.DIRTY
        if attrs.values["mood"] < 20:
            return PetState.SAD
        return self._random_behavior()

    def _random_behavior(self) -> PetState:
        pool = self.probabilities
        choices = list(pool.keys())
        weights = [pool[c] for c in choices]
        name = random.choices(choices, weights=weights, k=1)[0]
        return PetState[name.upper()]

    @staticmethod
    def duration_for(state: PetState) -> float:
        """行为默认持续时间（秒）。"""
        return {
            PetState.WALK: 6.0,
            PetState.PLAY: 8.0,
            PetState.SLEEP: 20.0,
            PetState.DROWSY: 4.0,
            PetState.HUNGRY: 4.0,
            PetState.DIRTY: 4.0,
            PetState.SAD: 5.0,
        }.get(state, 4.0)
