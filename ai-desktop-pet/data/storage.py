"""JSON 数据持久化"""
import json
import os
import shutil
from typing import Any

from data.paths import data_file


class Storage:
    """负责 settings/state/chat_history 的读写与损坏恢复。"""

    def __init__(self, settings: dict | None = None, state: dict | None = None):
        self._settings_cache = settings
        self._state_cache = state

    # ---- settings ----
    def load_settings(self) -> dict:
        if self._settings_cache is not None:
            return self._settings_cache
        return self._read("settings.json", default={})

    def save_settings(self, settings: dict):
        self._write("settings.json", settings)

    # ---- state ----
    def load_state(self) -> dict:
        if self._state_cache is not None:
            return self._state_cache
        return self._read("state.json", default={})

    def save_state(self, state: dict):
        self._write("state.json", state)

    # ---- chat history ----
    def load_chat(self) -> list:
        return self._read("chat_history.json", default=[])

    def save_chat(self, messages: list):
        self._write("chat_history.json", messages)

    def _read(self, name: str, default: Any) -> Any:
        path = data_file(name)
        if not os.path.exists(path):
            return default
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            backup = path + ".bak"
            try:
                shutil.copyfile(path, backup)
            except OSError:
                pass
            return default

    def _write(self, name: str, data: Any):
        path = data_file(name)
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError:
            pass
