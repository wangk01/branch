"""AI 桌宠主程序入口"""
import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from ai.client import AIClient
from animation.manager import AnimationManager
from config import APP_NAME, APP_VERSION, DEFAULT_SETTINGS
from core.attributes import AttributeSystem
from core.character import discover_characters, load_character
from core.behavior import BehaviorDecider
from core.state_machine import StateMachine
from data.storage import Storage
from ui.chat_window import ChatWindow
from ui.pet_window import PetWindow
from ui.settings_window import SettingsWindow
from ui.tray import TrayIcon


class DesktopPetApp:
    def __init__(self):
        self.storage = Storage()
        self.settings = DEFAULT_SETTINGS | self.storage.load_settings()
        for key, val in DEFAULT_SETTINGS.items():
            self.settings.setdefault(key, val)

        self.characters = discover_characters()
        current = self.settings.get("character", "slime_chan")
        if current not in self.characters:
            current = next(iter(self.characters)) if self.characters else "slime_chan"
            self.settings["character"] = current

        character_dir = self.characters.get(current)
        self.character = load_character(character_dir) if character_dir else {}

        state_data = self.storage.load_state()
        attrs_data = state_data.get("attributes", {})
        self.attrs = AttributeSystem(attrs_data)

        ai_cfg = self.settings.get("ai", {})
        self.ai_client = AIClient(ai_cfg.get("base_url", ""), ai_cfg.get("api_key", ""), ai_cfg.get("model", ""))

        self.state_machine = StateMachine()
        self.decider = BehaviorDecider(self.settings.get("behavior", {}))

        self.anim_mgr = AnimationManager(character_dir, self.character) if character_dir else None
        self.pet = None
        self.chat = None
        self.settings_win = None
        self.tray = None
        self.visible = True
        self._pending_quit = False

    def run(self):
        self.pet = PetWindow(
            self.state_machine, self.attrs, self.decider, self.anim_mgr, self.settings, on_chat=self.open_chat
        )
        self.pet.move(100, 200)
        self.pet.show()

        self._setup_timers()
        self.tray = TrayIcon(f"{APP_NAME} v{APP_VERSION}", self._tray_callbacks())
        self.tray.show()

    def _setup_timers(self):
        self._attr_timer = QTimer()
        self._attr_timer.timeout.connect(self._on_attr_tick)
        self._attr_timer.start(1000)
        self._save_timer = QTimer()
        self._save_timer.timeout.connect(self._save_state)
        self._save_timer.start(60000)

    def _on_attr_tick(self):
        self.attrs.tick()

    def _tray_callbacks(self) -> dict:
        return {
            "toggle_visible": self._toggle_visible,
            "switch_character": self._open_character_menu,
            "open_settings": self._open_settings,
            "quit": self.quit,
        }

    def _toggle_visible(self):
        self.visible = not self.visible
        self.pet.setVisible(self.visible)

    def _open_character_menu(self):
        from PySide6.QtGui import QAction, QCursor
        from PySide6.QtWidgets import QMenu

        menu = QMenu()
        for cid in self.characters:
            action = QAction(cid, menu)
            action.setCheckable(True)
            action.setChecked(cid == self.settings["character"])
            action.triggered.connect(lambda _=False, cc=cid: self.switch_character(cc))
            menu.addAction(action)
        menu.exec(QCursor.pos())

    def switch_character(self, cid: str):
        if cid not in self.characters:
            return
        self.settings["character"] = cid
        self.storage.save_settings(self.settings)
        character_dir = self.characters[cid]
        self.character = load_character(character_dir)
        self.anim_mgr = AnimationManager(character_dir, self.character)
        self.pet.anim_mgr = self.anim_mgr
        self.pet.play(self.state_machine.state)

    def _open_settings(self):
        if self.settings_win is not None and self.settings_win.isVisible():
            self.settings_win.raise_()
            return
        available = [(cid, load_character(d).get("label", cid)) for cid, d in self.characters.items()]
        self.settings_win = SettingsWindow(self.settings, available, self._on_settings_saved)
        self.settings_win.show()

    def _on_settings_saved(self, settings: dict):
        self.storage.save_settings(settings)
        ai = settings.get("ai", {})
        self.ai_client.base_url = ai.get("base_url", "")
        self.ai_client.api_key = ai.get("api_key", "")
        self.ai_client.model = ai.get("model", "")
        self.decider.idle_trigger_seconds = settings["behavior"].get("idle_trigger_seconds", 15)
        cid = settings.get("character")
        if cid in self.characters and cid != self.settings["character"]:
            self.switch_character(cid)

    def _save_state(self):
        self.storage.save_state({"attributes": self.attrs.to_dict()})

    def open_chat(self):
        if self.chat is not None and self.chat.isVisible():
            self.chat.raise_()
            self.chat.activateWindow()
            return
        self.chat = ChatWindow(self.character, self.attrs, self.ai_client, on_reply=self._on_chat_reply)
        self.chat.show()

    def _on_chat_reply(self, reply: str):
        self.pet.play(self.state_machine.state, 2.0)

    def quit(self):
        self._pending_quit = True
        self._save_state()
        if self.chat is not None:
            self.chat.close()
        QApplication.instance().quit()


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    pet_app = DesktopPetApp()
    pet_app.run()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
