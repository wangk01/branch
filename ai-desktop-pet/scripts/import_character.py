"""角色包导入工具

用法：
    python scripts/import_character.py --source-dir D:\\my_character --asset-id my_char --label "我的角色" [--set-current]

素材目录结构（GIF 或 PNG 序列帧目录均可）：
    my_character/
        reference.png       # 全身参考图（可选）
        idle.gif            # 或 idle/  目录下 0001.png...
        walk.gif
        sleep.gif
        ...
"""
import argparse
import json
import shutil
from pathlib import Path

from data.paths import user_characters_dir

SUPPORTED_VIDEO = (".gif", ".mp4", ".webm", ".mov", ".avi")

SLOTS = [
    "idle",
    "walk",
    "sleep",
    "carried",
    "stroke",
    "play",
    "eat",
    "bath",
    "double_click",
    "drowsy",
    "hungry",
    "dirty",
    "sad",
]


def _is_video(p: Path) -> bool:
    return p.suffix.lower() in SUPPORTED_VIDEO


def import_character(source_dir: Path, asset_id: str, label: str, species: str = "slime"):
    src = Path(source_dir)
    if not src.exists():
        raise FileNotFoundError(f"素材目录不存在: {src}")
    dest = Path(user_characters_dir()) / asset_id
    dest.mkdir(parents=True, exist_ok=True)

    animations = {}
    for slot in SLOTS:
        slot_path = src / slot
        gif_path = src / f"{slot}.gif"
        if slot_path.is_dir():
            frames = sorted(slot_path.glob("*.png"))
            if frames:
                frame_dir = dest / slot
                frame_dir.mkdir(exist_ok=True)
                for f in frames:
                    shutil.copy2(f, frame_dir / f.name)
                animations[slot] = {"type": "sequence", "frames_dir": slot, "fps": 10}
        elif gif_path.exists():
            import PIL.Image

            frame_dir = dest / slot
            frame_dir.mkdir(exist_ok=True)
            img = PIL.Image.open(gif_path)
            n = 0
            while True:
                img.seek(n)
                img.convert("RGBA").save(frame_dir / f"{n:04d}.png")
                n += 1
                try:
                    img.seek(n)
                except EOFError:
                    break
            animations[slot] = {"type": "sequence", "frames_dir": slot, "fps": img.info.get("duration", 100) // 10}

    ref = src / "reference.png"
    if ref.exists():
        shutil.copy2(ref, dest / "reference.png")

    cfg = {
        "id": asset_id,
        "label": label,
        "personality": "可爱、友善",
        "species": species,
        "colors": {"body": "#ff6b9d", "belly": "#ffd6e0", "accent": "#ff3b6b"},
        "animations": animations,
    }
    (dest / "character.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    return dest


def main():
    parser = argparse.ArgumentParser(description="导入自定义桌宠角色包")
    parser.add_argument("--source-dir", required=True, help="素材目录")
    parser.add_argument("--asset-id", required=True, help="角色 ID（目录名）")
    parser.add_argument("--label", required=True, help="角色显示名")
    parser.add_argument("--species", default="slime", choices=["slime", "dog"])
    parser.add_argument("--set-current", action="store_true", help="导入后设为当前角色")
    args = parser.parse_args()

    dest = import_character(args.source_dir, args.asset_id, args.label, args.species)
    print(f"已导入角色包: {dest}")

    if args.set_current:
        from data.storage import Storage

        storage = Storage()
        settings = storage.load_settings()
        settings["character"] = args.asset_id
        storage.save_settings(settings)
        print(f"已切换当前角色为: {args.asset_id}")


if __name__ == "__main__":
    main()
