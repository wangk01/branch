"""程序绘制卡通角色渲染器（无外部素材依赖）"""
import math

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QBrush, QColor, QPainter, QPen, QPixmap

from core.state_machine import PetState


class ProceduralRenderer:
    """用 QPainter 绘制参数化卡通角色。动画通过帧相位模拟动作。"""

    PIXMAP_SIZE = 160
    BODY_RADIUS = 38

    def __init__(self, colors: dict | None = None, species: str = "slime"):
        self.colors = colors or {"body": "#ff6b9d", "belly": "#ffd6e0", "accent": "#ff3b6b"}
        self.species = species

    def render(self, state: PetState, phase: float) -> QPixmap:
        pm = QPixmap(self.PIXMAP_SIZE, self.PIXMAP_SIZE)
        pm.fill(Qt.transparent)
        p = QPainter(pm)
        try:
            p.setRenderHint(QPainter.Antialiasing)
            cx = self.PIXMAP_SIZE / 2
            cy = self.PIXMAP_SIZE / 2 + 10
            if self.species == "dog":
                self._draw_dog(p, cx, cy, state, phase)
            else:
                self._draw_slime(p, cx, cy, state, phase)
        finally:
            p.end()
        return pm

    @staticmethod
    def _pen(color, width, cap_round: bool = True) -> QPen:
        pen = QPen(QColor(color), width)
        if cap_round:
            pen.setCapStyle(Qt.RoundCap)
        return pen

    def _draw_slime(self, p: QPainter, cx, cy, state, phase):
        body = QColor(self.colors["body"])
        belly = QColor(self.colors["belly"])
        accent = QColor(self.colors["accent"])
        wobble = math.sin(phase * 6.28) * 3 if state in (PetState.IDLE, PetState.SIDEBAR_IDLE) else 0

        if state == PetState.SLEEP:
            self._squash(p, cx, cy + 6, 1.18, 0.85, body)
        elif state in (PetState.WALK, PetState.PLAY):
            self._squash(p, cx + wobble, cy, 0.95 + abs(wobble) / 20, 1.05 - abs(wobble) / 20, body)
        elif state in (PetState.CARRIED, PetState.DOUBLE_CLICK):
            self._squash(p, cx, cy - 6, 1.15, 1.25, body)
        else:
            self._squash(p, cx, cy + wobble / 3, 1.0, 1.0, body)

        r = self.BODY_RADIUS
        p.setBrush(QBrush(belly))
        p.setPen(Qt.NoPen)
        p.drawEllipse(QPointF(cx - r * 0.42, cy + r * 0.3), r * 0.5, r * 0.62)

        eye_y = cy - r * 0.35 + wobble / 4
        blink = state in (PetState.SLEEP, PetState.DROWSY) or int(phase * 2) % 8 == 0
        p.setPen(self._pen(Qt.black, 3))
        if blink:
            for ex in (cx - r * 0.4, cx + r * 0.4):
                p.drawLine(QPointF(ex - 3, eye_y + 3), QPointF(ex + 3, eye_y + 3))
        else:
            for ex in (cx - r * 0.4, cx + r * 0.4):
                p.setBrush(QBrush(Qt.black))
                p.setPen(Qt.NoPen)
                p.drawEllipse(QPointF(ex, eye_y), 3.5, 4.5)

        mouth = self._mouth(state)
        if mouth:
            p.setPen(self._pen(Qt.black, 2.5))
            m_y = cy + r * 0.35
            if mouth == "open":
                p.setBrush(QBrush(accent))
                p.setPen(Qt.NoPen)
                p.drawEllipse(QPointF(cx, m_y), r * 0.22, r * 0.16)
            elif mouth == "yawn":
                p.setBrush(QBrush(accent))
                p.setPen(Qt.NoPen)
                p.drawEllipse(QPointF(cx, m_y), r * 0.3, r * 0.22)
            elif mouth == "pout":
                p.drawArc(QRectF(cx - 8, m_y - 4, 16, 12), 20 * 16, 140 * 16)
            else:
                p.drawArc(QRectF(cx - 10, m_y - 6, 20, 12), 200 * 16, 140 * 16)

        if state in (PetState.HUNGRY, PetState.DIRTY, PetState.SAD, PetState.DROWSY):
            p.setBrush(QColor(accent))
            p.setPen(Qt.NoPen)
            p.drawEllipse(QPointF(cx - r * 0.55, cy - r * 0.1), 4, 6)
            p.drawEllipse(QPointF(cx + r * 0.55, cy - r * 0.1), 4, 6)

        if state == PetState.DIRTY:
            p.setPen(self._pen(QColor(120, 90, 50), 3))
            for i in range(3):
                x = cx + (i - 1) * 18
                p.drawLine(QPointF(x - 4, cy + r * 0.15), QPointF(x + 4, cy + r * 0.45))
                p.drawLine(QPointF(x - 4, cy + r * 0.45), QPointF(x + 4, cy + r * 0.15))

        if state == PetState.SLEEP:
            p.setPen(QPen(QColor(80, 80, 90), 2))
            p.drawArc(QRectF(cx + r * 0.35, cy - r * 1.05, 20, 12), 210 * 16, 120 * 16)
            p.drawArc(QRectF(cx + r * 0.35, cy - r * 1.05, 20, 12), 210 * 16, 120 * 16)

        self._draw_zzz(p, cx, cy, state, phase)

    def _draw_dog(self, p: QPainter, cx, cy, state, phase):
        body = QColor(self.colors["body"])
        accent = QColor(self.colors["accent"])
        r = self.BODY_RADIUS
        wobble = math.sin(phase * 6.28) * 2 if state in (PetState.IDLE, PetState.SIDEBAR_IDLE) else 0

        p.setBrush(QBrush(body))
        p.setPen(Qt.NoPen)
        p.drawEllipse(QPointF(cx, cy + 6 + wobble / 3), r, r * 0.88)

        p.setBrush(QBrush(accent))
        p.drawEllipse(QPointF(cx, cy + 2 + wobble / 3), r * 0.8, r * 0.7)

        ear_wave = math.sin(phase * 6.28) * 4 if state in (PetState.WALK, PetState.PLAY) else 0
        p.drawEllipse(QPointF(cx - r * 0.85, cy - r * 0.55 + ear_wave), r * 0.3, r * 0.55)
        p.drawEllipse(QPointF(cx + r * 0.85, cy - r * 0.55 - ear_wave), r * 0.3, r * 0.55)

        eye_y = cy - r * 0.25 + wobble / 4
        blink = state in (PetState.SLEEP, PetState.DROWSY) or int(phase * 2) % 8 == 0
        p.setBrush(QBrush(Qt.black))
        p.setPen(Qt.NoPen)
        if blink:
            p.setPen(self._pen(Qt.black, 3))
            for ex in (cx - r * 0.4, cx + r * 0.4):
                p.drawLine(QPointF(ex - 3, eye_y + 3), QPointF(ex + 3, eye_y + 3))
        else:
            for ex in (cx - r * 0.4, cx + r * 0.4):
                p.drawEllipse(QPointF(ex, eye_y), 3.5, 4.5)

        p.setPen(self._pen(Qt.black, 2.5))
        m_y = cy + r * 0.25
        if state == PetState.SLEEP:
            p.drawArc(QRectF(cx - 12, m_y - 4, 24, 14), 200 * 16, 140 * 16)
        elif state in (PetState.EAT, PetState.PLAY):
            p.drawEllipse(QPointF(cx, m_y + 2), r * 0.2, r * 0.14)
        else:
            p.drawArc(QRectF(cx - 10, m_y - 4, 20, 12), 200 * 16, 140 * 16)

        tail = math.sin(phase * 6.28) * 6 if state in (PetState.WALK, PetState.PLAY) else math.sin(phase * 2) * 2
        p.setPen(self._pen(body, 6))
        p.drawLine(QPointF(cx + r * 0.9, cy - r * 0.2), QPointF(cx + r * 0.9 + tail, cy - r * 0.7))

        if state == PetState.SLEEP:
            self._draw_zzz(p, cx, cy, state, phase)

    def _draw_zzz(self, p: QPainter, cx, cy, state, phase):
        if state not in (PetState.SLEEP, PetState.DROWSY):
            return
        p.setPen(QPen(QColor(100, 100, 120), 2.5))
        off = int(phase * 4) % 3
        sizes = [14, 18, 22]
        for i in range(3):
            s = sizes[(off + i) % 3] * 0.7
            x = cx + 46 + i * 8
            y = cy - 40 - i * 16
            p.drawLine(QPointF(x, y), QPointF(x + s * 0.5, y))
            p.drawLine(QPointF(x + s * 0.5, y), QPointF(x + s * 0.5, y - s * 0.5))
            p.drawLine(QPointF(x + s * 0.5, y - s * 0.5), QPointF(x + s, y - s * 0.5))
            p.drawLine(QPointF(x + s, y - s * 0.5), QPointF(x + s, y - s))

    def _squash(self, p: QPainter, cx, cy, sx, sy, color):
        r = self.BODY_RADIUS
        p.setBrush(QBrush(color))
        p.setPen(Qt.NoPen)
        p.save()
        p.translate(cx, cy)
        p.scale(sx, sy)
        p.drawEllipse(QPointF(0, 0), r, r)
        p.restore()

    @staticmethod
    def _mouth(state: PetState) -> str | None:
        if state in (PetState.SLEEP, PetState.DROWSY):
            return "open"
        if state == PetState.SAD:
            return "pout"
        if state in (PetState.EAT, PetState.PLAY, PetState.DOUBLE_CLICK):
            return "open"
        if state in (PetState.HUNGRY,):
            return "open"
        return "smile"
