"""ComfyUI API 客户端"""
import time
import uuid

import requests

DEFAULT_COMFY_URL = "http://127.0.0.1:8188"


class ComfyClient:
    """提交工作流到本地 ComfyUI 并轮询生成结果。"""

    def __init__(self, base_url: str = DEFAULT_COMFY_URL):
        self.base_url = base_url.rstrip("/")

    def is_available(self, timeout: float = 2.0) -> bool:
        try:
            requests.get(f"{self.base_url}/system_stats", timeout=timeout)
            return True
        except requests.RequestException:
            return False

    def submit(self, workflow: dict, timeout: float = 600.0) -> list[str]:
        """提交工作流，返回生成的图片 URL 列表。"""
        prompt_id = str(uuid.uuid4())
        payload = {"prompt": workflow, "client_id": "desktop_pet"}
        resp = requests.post(f"{self.base_url}/prompt", json=payload, timeout=timeout)
        resp.raise_for_status()

        node_ids = self._output_node_ids(workflow)
        deadline = time.time() + timeout
        while time.time() < deadline:
            history = requests.get(f"{self.base_url}/history/{prompt_id}", timeout=timeout).json()
            if prompt_id in history:
                entry = history[prompt_id]
                if entry.get("status", {}).get("completed"):
                    return self._collect_images(entry, node_ids)
                if entry.get("status", {}).get("status_str") == "error":
                    raise RuntimeError("ComfyUI 工作流执行出错")
            time.sleep(1)
        raise TimeoutError("ComfyUI 生成超时")

    def _output_node_ids(self, workflow: dict) -> list[str]:
        ids = []
        for nid, node in workflow.items():
            if node.get("class_type") in ("SaveImage",):
                ids.append(nid)
        return ids

    def _collect_images(self, history_entry: dict, node_ids: list[str]) -> list[str]:
        urls = []
        outputs = history_entry.get("outputs", {})
        for nid in node_ids:
            for img in outputs.get(nid, {}).get("images", []):
                urls.append(f"{self.base_url}/view?filename={img['filename']}&subfolder={img.get('subfolder', '')}&type={img.get('type', 'output')}")
        return urls
