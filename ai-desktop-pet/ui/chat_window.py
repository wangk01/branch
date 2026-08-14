"""对话窗口"""
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ai.client import AIClient
from ai.fallback import FallbackResponder
from ai.personality import build_system_prompt
from core.attributes import AttributeSystem


class ChatWorker(QThread):
    """后台执行 AI 对话请求，避免阻塞 UI。"""

    finished = Signal(str)
    failed = Signal(str)

    def __init__(self, client: AIClient, messages: list[dict]):
        super().__init__()
        self._client = client
        self._messages = messages

    def run(self):
        try:
            reply = self._client.chat(self._messages)
            self.finished.emit(reply)
        except Exception as exc:  # noqa: BLE001
            self.failed.emit(str(exc))


class ChatWindow(QWidget):
    def __init__(self, character: dict, attrs: AttributeSystem, client: AIClient, on_reply=None):
        super().__init__(None)
        self.setWindowTitle("和桌宠聊天")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self.resize(380, 480)
        self._character = character or {}
        self._attrs = attrs
        self._client = client
        self._fallback = FallbackResponder()
        self._on_reply = on_reply
        self._messages: list[dict] = []
        self._worker: ChatWorker | None = None

        layout = QVBoxLayout(self)
        self.label = QLabel(self._character.get("label", "桌宠"))
        layout.addWidget(self.label)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        bottom = QHBoxLayout()
        self.input = QLineEdit()
        self.input.returnPressed.connect(self._send)
        self.send_btn = QPushButton("发送")
        self.send_btn.clicked.connect(self._send)
        bottom.addWidget(self.input)
        bottom.addWidget(self.send_btn)
        layout.addLayout(bottom)

    def _send(self):
        text = self.input.text().strip()
        if not text or self._worker is not None:
            return
        self.input.clear()
        self._append("user", text)
        self._messages.append({"role": "user", "content": text})

        if self._client.is_configured():
            system = build_system_prompt(self._character, self._attrs)
            messages = [{"role": "system", "content": system}] + self._messages[-20:]
            self._worker = ChatWorker(self._client, messages)
            self._worker.finished.connect(self._on_reply_ok)
            self._worker.failed.connect(self._on_reply_fail)
            self._worker.start()
        else:
            self._on_reply_ok(self._fallback.respond(text))

    def _on_reply_ok(self, reply: str):
        self._worker = None
        self._append("assistant", reply)
        self._messages.append({"role": "assistant", "content": reply})
        if self._on_reply:
            self._on_reply(reply)

    def _on_reply_fail(self, error: str):
        self._worker = None
        self._append("assistant", "(AI 调用失败：" + error + "，已用预设回复代替)")
        self._on_reply_ok(self._fallback.respond(""))

    def _append(self, role: str, text: str):
        who = "我" if role == "user" else self._character.get("label", "桌宠")
        item = QListWidgetItem(f"{who}: {text}")
        self.list_widget.addItem(item)
        self.list_widget.scrollToBottom()

    def closeEvent(self, event):
        if self._worker is not None:
            self._worker.wait(100)
        super().closeEvent(event)
