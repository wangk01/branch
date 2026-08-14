import os
import sys
import tempfile

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest  # noqa: E402
from core.attributes import AttributeSystem  # noqa: E402
from core.behavior import BehaviorDecider  # noqa: E402
from core.state_machine import PetState, StateMachine  # noqa: E402
from data.storage import Storage  # noqa: E402


class TestStateMachine:
    def test_initial_state(self):
        sm = StateMachine()
        assert sm.get_state() == PetState.IDLE

    def test_set_state_fires_listener(self):
        sm = StateMachine()
        events = []
        sm.add_listener(lambda old, new: events.append((old, new)))
        sm.set_state(PetState.WALK)
        assert events == [(PetState.IDLE, PetState.WALK)]

    def test_same_state_no_event(self):
        sm = StateMachine()
        events = []
        sm.add_listener(lambda old, new: events.append((old, new)))
        sm.set_state(PetState.IDLE)
        assert events == []


class TestAttributes:
    def test_default_values_in_range(self):
        attrs = AttributeSystem()
        for v in attrs.values.values():
            assert 0 <= v <= 100

    def test_tick_decay(self):
        attrs = AttributeSystem()
        attrs.values["energy"] = 50
        attrs.values["hunger"] = 20
        attrs.tick()
        assert attrs.values["energy"] < 50
        assert attrs.values["hunger"] > 20

    def test_clamp_lower(self):
        attrs = AttributeSystem()
        attrs.values["energy"] = 1
        attrs.tick()
        assert attrs.values["energy"] >= 0

    def test_feed_bath(self):
        attrs = AttributeSystem()
        attrs.values["hunger"] = 90
        attrs.values["clean"] = 10
        attrs.feed()
        attrs.bath()
        assert attrs.values["hunger"] < 90
        assert attrs.values["clean"] > 10

    def test_roundtrip_dict(self):
        attrs = AttributeSystem()
        attrs.values["energy"] = 42.3
        data = attrs.to_dict()
        assert abs(data["energy"] - 42.3) < 0.01


class TestBehavior:
    def test_should_act(self):
        dec = BehaviorDecider({"idle_trigger_seconds": 15})
        assert not dec.should_act(10)
        assert dec.should_act(20)

    def test_forced_sleep_when_low_energy(self):
        attrs = AttributeSystem()
        attrs.values["energy"] = 5
        dec = BehaviorDecider()
        assert dec.decide(attrs) == PetState.SLEEP

    def test_hungry_when_high_hunger(self):
        attrs = AttributeSystem()
        attrs.values["hunger"] = 90
        dec = BehaviorDecider()
        assert dec.decide(attrs) == PetState.HUNGRY

    def test_random_behavior_in_pool(self):
        attrs = AttributeSystem()
        dec = BehaviorDecider()
        seen = {dec.decide(attrs) for _ in range(50)}
        assert seen.intersection({PetState.WALK, PetState.SLEEP, PetState.PLAY, PetState.DROWSY})


class TestStorage:
    def _patch(self, tmp_path, monkeypatch):
        import data.paths as paths_module

        monkeypatch.setattr(paths_module, "data_dir", lambda: tmp_path)

    def test_settings_roundtrip(self, tmp_path, monkeypatch):
        self._patch(tmp_path, monkeypatch)
        storage = Storage()
        storage.save_settings({"character": "dog"})
        assert Storage().load_settings()["character"] == "dog"

    def test_corrupt_file_restores_default(self, tmp_path, monkeypatch):
        self._patch(tmp_path, monkeypatch)
        (tmp_path / "settings.json").write_text("{not-json", encoding="utf-8")
        storage = Storage()
        assert storage.load_settings() == {}
