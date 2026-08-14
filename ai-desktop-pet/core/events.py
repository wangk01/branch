"""简单事件总线，解耦 UI 与核心逻辑"""
from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable


class EventBus:
    def __init__(self):
        self._subs: dict[str, list[Callable]] = defaultdict(list)

    def subscribe(self, event: str, fn: Callable):
        self._subs[event].append(fn)

    def emit(self, event: str, *args, **kwargs):
        for fn in list(self._subs.get(event, [])):
            fn(*args, **kwargs)

    def unsubscribe(self, event: str, fn: Callable):
        if event in self._subs and fn in self._subs[event]:
            self._subs[event].remove(fn)
