"""属性系统：能量/饥饿/清洁/心情"""
import copy
import time
from dataclasses import dataclass, field

from config import ATTRIBUTE_DECAY, DEFAULT_ATTRIBUTES


@dataclass
class AttributeSystem:
    values: dict = field(default_factory=lambda: copy.deepcopy(DEFAULT_ATTRIBUTES))

    def __post_init__(self):
        for k in DEFAULT_ATTRIBUTES:
            if k not in self.values:
                self.values[k] = DEFAULT_ATTRIBUTES[k]

    def tick(self):
        """随时间流逝更新属性。"""
        for key, rate in ATTRIBUTE_DECAY.items():
            if key == "energy":
                self.values[key] -= rate
            elif key == "hunger":
                self.values[key] += rate
            elif key == "clean":
                self.values[key] -= rate
            elif key == "mood":
                self.values[key] -= rate
            self._clamp(key)

    def _clamp(self, key: str):
        self.values[key] = max(0.0, min(100.0, self.values[key]))

    def feed(self, amount: float = 25.0):
        self.values["hunger"] -= amount
        self.values["mood"] += 5.0
        self._clamp("hunger")
        self._clamp("mood")

    def bath(self, amount: float = 40.0):
        self.values["clean"] += amount
        self.values["mood"] += 8.0
        self._clamp("clean")
        self._clamp("mood")

    def stroke(self, amount: float = 6.0):
        self.values["mood"] += amount
        self._clamp("mood")

    def play(self, amount: float = 10.0):
        self.values["mood"] += amount
        self.values["energy"] -= 3.0
        self._clamp("mood")
        self._clamp("energy")

    def sleep(self, amount: float = 30.0):
        self.values["energy"] += amount
        self.values["hunger"] += 5.0
        self._clamp("energy")
        self._clamp("hunger")

    def to_dict(self) -> dict:
        return copy.deepcopy({k: round(v, 1) for k, v in self.values.items()})

    def summary(self) -> str:
        return "、".join(f"{k}:{int(v)}" for k, v in self.values.items())
