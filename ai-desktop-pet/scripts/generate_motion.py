"""通过 ComfyUI 从参考图生成角色动作帧

用法：
    python scripts/generate_motion.py --asset-id my_char --slot idle \
        --reference assets/base/my_char/reference.png
"""
import argparse
import json
import shutil
import tempfile
from pathlib import Path

import requests

from comfyui.client import ComfyClient
from comfyui.workflow import load_workflow
from data.paths import user_characters_dir


def generate_motion(asset_id: str, slot: str, reference: Path, workflow: dict, fps: int = 10) -> Path:
    client = ComfyClient()
    if not client.is_available():
        raise RuntimeError("ComfyUI 未运行，请先启动本地 ComfyUI (127.0.0.1:8188)")

    wf = dict(workflow)
    for node in wf.values():
        if node.get("class_type") in ("LoadImage", "ImageLoader"):
            node["inputs"]["image"] = str(reference)
        if node.get("class_type") == "SaveImage":
            node["inputs"].setdefault("filename_prefix", f"{asset_id}_{slot}")

    images = client.submit(wf)
    if not images:
        raise RuntimeError("ComfyUI 未返回图片")

    frame_dir = Path(user_characters_dir()) / asset_id / slot
    frame_dir.mkdir(parents=True, exist_ok=True)

    save_dir = None
    with tempfile.TemporaryDirectory() as tmp:
        for i, url in enumerate(images):
            data = requests.get(url, timeout=60).content
            tmp_path = Path(tmp) / f"{i:04d}.png"
            tmp_path.write_bytes(data)
        save_dir = frame_dir
        for i in range(len(images)):
            shutil.copy2(Path(tmp) / f"{i:04d}.png", save_dir / f"{i:04d}.png")

    _update_character_json(asset_id, slot, fps)
    return frame_dir


def _update_character_json(asset_id: str, slot: str, fps: int):
    char_dir = Path(user_characters_dir()) / asset_id
    cfg_path = char_dir / "character.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8")) if cfg_path.exists() else {"id": asset_id}
    cfg.setdefault("animations", {})
    cfg["animations"][slot] = {"type": "sequence", "frames_dir": slot, "fps": fps}
    cfg_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="用 ComfyUI 从参考图生成动作")
    parser.add_argument("--asset-id", required=True, help="角色 ID")
    parser.add_argument("--slot", required=True, help="动作槽位: idle/walk/sleep/etc.")
    parser.add_argument("--reference", required=True, help="参考图路径")
    parser.add_argument("--workflow", default="image_to_frames.json", help="工作流文件")
    parser.add_argument("--fps", type=int, default=10)
    args = parser.parse_args()

    wf = load_workflow(args.workflow)
    frame_dir = generate_motion(args.asset_id, args.slot, Path(args.reference), wf, args.fps)
    print(f"已生成 {args.slot} 动作: {frame_dir}")


if __name__ == "__main__":
    main()
