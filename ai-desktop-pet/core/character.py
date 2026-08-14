"""角色包加载与管理"""
import json
from pathlib import Path

from config import resource_path
from data.paths import user_characters_dir


def discover_characters() -> dict[str, Path]:
    """返回 {character_id: character_dir}，内置角色优先。"""
    found: dict[str, Path] = {}
    dirs = [Path(resource_path("base")), Path(user_characters_dir())]
    for base in dirs:
        if not base.exists():
            continue
        for entry in sorted(base.iterdir()):
            if not entry.is_dir():
                continue
            if (entry / "character.json").exists():
                found[entry.name] = entry
    return found


def load_character(character_dir: Path) -> dict:
    cfg = {}
    cfg_path = character_dir / "character.json"
    if cfg_path.exists():
        try:
            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            cfg = {}
    cfg.setdefault("id", character_dir.name)
    cfg.setdefault("label", character_dir.name)
    cfg.setdefault("personality", "可爱、友善")
    cfg.setdefault("species", "slime")
    cfg.setdefault("colors", {"body": "#ff6b9d", "belly": "#ffd6e0", "accent": "#ff3b6b"})
    return cfg
