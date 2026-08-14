"""透明置顶的宠物窗口"""
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QMenu, QWidget

from animation.manager import AnimationManager
from config import DEFAULT_WINDOW_SIZE, SIDEBAR_DOCK_DISTANCE, SIDEBAR_MARGIN, WALK_SPEED
from core.attributes import AttributeSystem
from core.behavior import BehaviorDecider
from core.state_machine import PetState, StateMachine


class PetWindow(QWidget):
    def __init__(
        self,
        state_machine: StateMachine,
        attrs: AttributeSystem,
        decider: BehaviorDecider,
        anim_mgr: AnimationManager,
        settings: dict,
        on_chat=None,
    ):
        super().__init__(None)
        self.state_machine = state_machine
        self.attrs = attrs
        self.decider = decider
        self.anim_mgr = anim_mgr
        self.settings = settings
        self._on_chat = on_chat

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(*DEFAULT_WINDOW_SIZE)

        self._phase = 0.0
        self._state_started_at = 0.0
        self._idle_since = 0.0
        self._sidebar = False
        self._walking = False
        self._walk_target = None

        self.tick_timer = QTimer(self)
        self.tick_timer.timeout.connect(self._on_tick)
        self.tick_timer.start(100)

        self.state_machine.add_listener(self._on_state_changed)
        self._apply_state(PetState.IDLE)

    # ---- 对外接口 ----
    def play(self, state: PetState, duration: float | None = None):
        self._duration_override = duration
        self.state_machine.set_state(state)

    # ---- 内部逻辑 ----
    def _on_state_changed(self, old, new):
        self._state_started_at = self._phase
        if new == PetState.WALK:
            self._start_walk()
        else:
            self._walking = False
            self._walk_target = None
        self.update()

    def _apply_state(self, state: PetState):
        self._state_started_at = self._phase
        self.update()

    def _start_walk(self):
        self._walking = True
        target = self.x() + self.settings["behavior"].get("walk_range", 120)
        screen = self.screen()
        max_x = (screen.availableGeometry().right() if screen else 1920) - self.width()
        self._walk_target = max(0, min(target, max_x))

    def _on_tick(self):
        self._phase += 0.1
        state = self.state_machine.state

        if self._walking and self._walk_target is not None:
            step = WALK_SPEED
            if abs(self._walk_target - self.x()) <= step:
                self.move(self._walk_target, self.y())
                self._walking = False
                self.state_machine.set_state(PetState.IDLE)
            else:
                self.move(self.x() + (step if self._walk_target > self.x() else -step), self.y())

        now = self._phase
        duration = getattr(self, "_duration_override", None)
        elapsed = now - self._state_started_at
        if state not in (PetState.IDLE, PetState.SIDEBAR_IDLE) and duration:
            if elapsed >= duration:
                self._duration_override = None
                self._return_to_idle()
                return

        if state in (PetState.IDLE, PetState.SIDEBAR_IDLE):
            self._idle_since += 0.1
            if self.decider.should_act(self._idle_since):
                self._idle_since = 0.0
                next_state = self.decider.decide(self.attrs)
                self._duration_override = BehaviorDecider.duration_for(next_state)
                self.state_machine.set_state(next_state)
        else:
            self._idle_since = 0.0

        self._check_sidebar_dock()
        self.update()

    def _return_to_idle(self):
        target = PetState.SIDEBAR_IDLE if self._sidebar else PetState.IDLE
        self.state_machine.set_state(target)

    def _check_sidebar_dock(self):
        if self._walking:
            return
        screen = self.screen()
        if not screen:
            return
        geo = screen.availableGeometry()
        near_left = self.x() <= geo.left() + SIDEBAR_DOCK_DISTANCE
        near_right = self.x() + self.width() >= geo.right() - SIDEBAR_DOCK_DISTANCE
        if (near_left or near_right) and not self._sidebar:
            self._enter_sidebar(near_left)
        elif not near_left and not near_right and self._sidebar:
            self._leave_sidebar()

    def _enter_sidebar(self, on_left: bool):
        self._sidebar = True
        screen = self.screen()
        geo = screen.availableGeometry()
        x = geo.left() + SIDEBAR_MARGIN if on_left else geo.right() - self.width() - SIDEBAR_MARGIN
        self.move(x, self.y())
        if self.state_machine.state in (PetState.IDLE,):
            self.state_machine.set_state(PetState.SIDEBAR_IDLE)

    def _leave_sidebar(self):
        self._sidebar = False
        if self.state_machine.state == PetState.SIDEBAR_IDLE:
            self.state_machine.set_state(PetState.IDLE)

    def is_sidebar(self) -> bool:
        return self._sidebar

    # ---- 绘制 ----
    def paintEvent(self, event):
        from PySide6.QtGui import QPainter

        state = self.state_machine.state
        frame, kind = self.anim_mgr.frame(state, self._phase)
        p = QPainter(self)
        p.drawPixmap(0, 0, frame)
        p.end()

    # ---- 交互 ----
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._drag_offset = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
        self._idle_since = 0.0
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() & Qt.LeftButton and hasattr(self, "_drag_offset"):
            self.state_machine.set_state(PetState.CARRIED)
            self.move(event.globalPosition().toPoint() - self._drag_offset)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.state_machine.state == PetState.CARRIED:
            self._return_to_idle()
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        self.play(PetState.DOUBLE_CLICK, 1.2)
        self.attrs.stroke(8)
        super().mouseDoubleClickEvent(event)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        menu.addAction("抚摸", lambda: self._interact(PetState.STROKE, self.attrs.stroke))
        menu.addAction("喂食", lambda: self._interact(PetState.EAT, self.attrs.feed))
        menu.addAction("洗澡", lambda: self._interact(PetState.BATH, self.attrs.bath))
        menu.addAction("玩耍", lambda: self._interact(PetState.PLAY, self.attrs.play))
        menu.addSeparator()
        if self._on_chat is not None:
            menu.addAction("聊天", self._on_chat)
            menu.addSeparator()
        menu.exec(event.globalPos())

    def _interact(self, state: PetState, action):
        action()
        self.play(state, 3.0)
        self._idle_since = 0.0
