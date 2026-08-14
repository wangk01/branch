"""宠物性格设定与系统提示词生成"""
from core.attributes import AttributeSystem


def build_system_prompt(character: dict, attrs: AttributeSystem | None = None) -> str:
    label = (character or {}).get("label", "桌宠")
    personality = (character or {}).get("personality", "可爱、友善")
    attrs_line = ""
    if attrs is not None:
        attrs_line = (
            "\n你当前的宠物状态："
            f"能量{int(attrs.values['energy'])}/100、"
            f"饥饿{int(attrs.values['hunger'])}/100、"
            f"清洁{int(attrs.values['clean'])}/100、"
            f"心情{int(attrs.values['mood'])}/100。"
            "回复时可自然带上当前状态（如困了就打个哈欠说想睡觉）。"
        )
    return (
        f"你是一只名叫「{label}」的 Windows 桌面宠物。"
        f"你的性格：{personality}。"
        f"请用简短、可爱、口语化的中文回复，每条回复不超过 60 字，"
        f"可以适度使用颜文字，但不要用 markdown 格式。"
        f"{attrs_line}"
    )
