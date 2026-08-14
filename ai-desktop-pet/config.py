"""默认配置参数"""
from pathlib import Path

APP_NAME = "AI Desktop Pet"
APP_VERSION = "1.0.0"
ORG_NAME = "AIDesktopPet"

DEFAULT_WINDOW_SIZE = (120, 120)
SIDEBAR_DOCK_DISTANCE = 40
SIDEBAR_MARGIN = 8
WALK_SPEED = 1.2
TICK_INTERVAL_MS = 1000
IDLE_TRIGGER_SECONDS = 15
AI_REQUEST_TIMEOUT = 30

DEFAULT_ATTRIBUTES = {"energy": 80, "hunger": 20, "clean": 90, "mood": 70}

ATTRIBUTE_DECAY = {
    "energy": 0.4,
    "hunger": 0.6,
    "clean": 0.1,
    "mood": 0.05,
}

DEFAULT_SETTINGS = {
    "character": "slime_chan",
    "ai": {"base_url": "", "api_key": "", "model": ""},
    "behavior": {
        "idle_trigger_seconds": IDLE_TRIGGER_SECONDS,
        "walk_range": 120,
        "behavior_probabilities": {
            "walk": 0.4,
            "sleep": 0.15,
            "play": 0.2,
            "drowsy": 0.05,
            "sad": 0.1,
            "hungry": 0.05,
            "dirty": 0.05,
        },
    },
}

RESOURCE_DIR = Path(__file__).resolve().parent / "assets"


def data_dir() -> Path:
    """返回数据存储目录：打包后使用 %APPDATA%，源码运行使用 ./data。"""
    import sys

    if getattr(sys, "frozen", False):
        base = Path.home() / "AppData" / "Roaming" / ORG_NAME
    else:
        base = Path(__file__).resolve().parent / "data"
    base.mkdir(parents=True, exist_ok=True)
    return base


def resource_path(rel: str) -> Path:
    """定位资源文件：打包后使用 sys._MEIPASS。"""
    import sys

    if getattr(sys, "frozen", False):
        base = Path(getattr(sys, "_MEIPASS", "."))
    else:
        base = RESOURCE_DIR
    return base / rel
