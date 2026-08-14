"""设置窗口"""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class SettingsWindow(QWidget):
    def __init__(self, settings: dict, available_characters: list[tuple[str, str]], on_save=None):
        super().__init__(None)
        self.setWindowTitle("桌宠设置")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self.resize(360, 320)
        self._settings = settings
        self._on_save = on_save

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.character_combo = QComboBox()
        for cid, label in available_characters:
            self.character_combo.addItem(label, cid)
        idx = self.character_combo.findData(settings.get("character"))
        if idx >= 0:
            self.character_combo.setCurrentIndex(idx)
        form.addRow("角色", self.character_combo)

        ai = settings.get("ai", {})
        self.base_url = QLineEdit(ai.get("base_url", ""))
        self.base_url.setPlaceholderText("https://api.deepseek.com/v1")
        self.api_key = QLineEdit(ai.get("api_key", ""))
        self.api_key.setEchoMode(QLineEdit.Password)
        self.model = QLineEdit(ai.get("model", "deepseek-chat"))
        form.addRow("API 地址", self.base_url)
        form.addRow("API Key", self.api_key)
        form.addRow("模型名称", self.model)

        self.idle_spin = QSpinBox()
        self.idle_spin.setRange(5, 300)
        self.idle_spin.setValue(settings.get("behavior", {}).get("idle_trigger_seconds", 15))
        form.addRow("空闲触发行为(秒)", self.idle_spin)

        layout.addLayout(form)

        tip = QLabel("API 地址需为 OpenAI 兼容接口，例如 https://api.deepseek.com/v1")
        tip.setWordWrap(True)
        tip.setStyleSheet("color: gray; font-size: 11px;")
        layout.addWidget(tip)

        btns = QHBoxLayout()
        self.save_btn = QPushButton("保存")
        self.save_btn.clicked.connect(self._save)
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self.close)
        btns.addWidget(self.save_btn)
        btns.addWidget(self.cancel_btn)
        layout.addLayout(btns)

    def _save(self):
        self._settings["character"] = self.character_combo.currentData()
        self._settings["ai"] = {
            "base_url": self.base_url.text().strip(),
            "api_key": self.api_key.text().strip(),
            "model": self.model.text().strip(),
        }
        self._settings["behavior"]["idle_trigger_seconds"] = self.idle_spin.value()
        if self._on_save:
            self._on_save(self._settings)
        self.close()
