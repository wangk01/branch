"""数据路径管理"""
from config import data_dir, resource_path

CHARACTERS_DIR_NAME = "base"


def characters_dir() -> str:
    return str(resource_path("base"))


def data_file(name: str) -> str:
    return str(data_dir() / name)


def user_characters_dir() -> str:
    """用户导入的自定义角色目录，持久化到数据目录。"""
    d = data_dir() / "characters"
    d.mkdir(parents=True, exist_ok=True)
    return str(d)
