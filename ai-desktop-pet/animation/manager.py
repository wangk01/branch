"""动画管理器：统一角色包动画槽位调度"""
from pathlib import Path

from animation.procedural_renderer import ProceduralRenderer
from animation.sequence_player import SequencePlayer
from core.state_machine import PetState

SLOT_MAP = {
    PetState.IDLE: "idle",
    PetState.SIDEBAR_IDLE: "idle",
    PetState.WALK: "walk",
    PetState.SLEEP: "sleep",
    PetState.DROWSY: "drowsy",
    PetState.PLAY: "play",
    PetState.EAT: "eat",
    PetState.BATH: "bath",
    PetState.STROKE: "stroke",
    PetState.DOUBLE_CLICK: "double_click",
    PetState.DIRTY: "dirty",
    PetState.HUNGRY: "hungry",
    PetState.SAD: "sad",
    PetState.CARRIED: "carried",
}


class AnimationManager:
    """给定角色包配置，为每个状态提供当前帧。有序列帧则用序列帧，否则程序绘制。"""

    def __init__(self, character_dir: Path, config: dict):
        self._character_dir = character_dir
        self._config = config or {}
        self._procedural = ProceduralRenderer(
            colors=self._config.get("colors"),
            species=self._config.get("species", "slime"),
        )
        self._sequences: dict[PetState, SequencePlayer] = {}
        self._load_sequences()

    def _load_sequences(self):
        animations = self._config.get("animations", {})
        for state, slot in SLOT_MAP.items():
            spec = animations.get(slot)
            if isinstance(spec, dict) and spec.get("type") == "sequence":
                frames_dir = self._character_dir / spec.get("frames_dir", slot)
                fps = spec.get("fps", 10)
                player = SequencePlayer(frames_dir, fps)
                if player.has_frames():
                    self._sequences[state] = player

    def uses_sequence(self, state: PetState) -> bool:
        return state in self._sequences

    def frame(self, state: PetState, phase: float):
        player = self._sequences.get(state)
        if player:
            idx = int(phase * player.frame_count())
            return player.frame(idx), "sequence"
        return self._procedural.render(state, phase), "procedural"

    def has_slot(self, state: PetState) -> bool:
        return self.uses_sequence(state) or True
