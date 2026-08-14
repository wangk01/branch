"""系统托盘"""
from PySide6.QtGui import QAction, QIcon, QPixmap
from PySide6.QtWidgets import QMenu, QSystemTrayIcon

from animation.procedural_renderer import ProceduralRenderer
from core.state_machine import PetState


class TrayIcon(QSystemTrayIcon):
    def __init__(self, app_name: str, callbacks: dict):
        super().__init__(None)
        self.setIcon(self._make_icon())
        self.setToolTip(app_name)
        self._callbacks = callbacks

        menu = QMenu()
        menu.addAction(QAction("显示/隐藏宠物", menu))
        menu.addAction(QAction("切换角色", menu))
        menu.addAction(QAction("设置", menu))
        menu.addSeparator()
        menu.addAction(QAction("退出", menu))

        for action in menu.actions():
            if action.text() == "显示/隐藏宠物":
                action.triggered.connect(callbacks["toggle_visible"])
            elif action.text() == "切换角色":
                action.triggered.connect(callbacks["switch_character"])
            elif action.text() == "设置":
                action.triggered.connect(callbacks["open_settings"])
            elif action.text() == "退出":
                action.triggered.connect(callbacks["quit"])
        self.setContextMenu(menu)
        self.activated.connect(self._on_activated)

    def _make_icon(self) -> QIcon:
        pm = ProceduralRenderer(colors={"body": "#ff6b9d", "belly": "#ffd6e0", "accent": "#ff3b6b"}).render(
            PetState.IDLE, 0.0
        )
        return QIcon(pm)

    def _on_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self._callbacks.get("toggle_visible")()
