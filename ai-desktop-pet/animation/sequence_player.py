"""序列帧/GIF 播放器"""
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel


class SequencePlayer:
    """播放 PNG 序列帧动画。帧由外部按时序更新。"""

    def __init__(self, frames_dir, fps=10):
        self._pixmaps = []
        self._load(frames_dir)
        self._fps = fps

    def _load(self, frames_dir):
        from pathlib import Path

        d = Path(frames_dir)
        if not d.exists():
            return
        for f in sorted(d.glob("*.png")):
            pm = QPixmap(str(f))
            if not pm.isNull():
                self._pixmaps.append(pm)

    def has_frames(self) -> bool:
        return bool(self._pixmaps)

    def frame_count(self) -> int:
        return len(self._pixmaps)

    def frame(self, index: int) -> QPixmap | None:
        if not self._pixmaps:
            return None
        return self._pixmaps[index % len(self._pixmaps)]

    def frame_interval_ms(self) -> int:
        return max(1, int(1000 / self._fps))
