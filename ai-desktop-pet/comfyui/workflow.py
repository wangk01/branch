"""ComfyUI 工作流模板

默认工作流：加载参考图 -> 图生视频（如需生成视频则需安装对应节点）-> 保存图片帧。
此模板为占位工作流，用户可按本地 ComfyUI 节点实际安装情况替换。
"""
from pathlib import Path


def load_workflow(name: str = "image_to_frames.json") -> dict:
    wf_path = Path(__file__).resolve().parent / "workflows" / name
    if wf_path.exists():
        import json

        return json.loads(wf_path.read_text(encoding="utf-8"))
    return {"__placeholder__": {"class_type": "EmptyLatentImage", "inputs": {"width": 512, "height": 512, "batch_size": 1}}}
