import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest  # noqa: E402
from ai.client import AIClient  # noqa: E402
from ai.fallback import FallbackResponder  # noqa: E402
from ai.personality import build_system_prompt  # noqa: E402
from animation.procedural_renderer import ProceduralRenderer  # noqa: E402
from core.attributes import AttributeSystem  # noqa: E402
from core.state_machine import PetState  # noqa: E402


class TestPersonality:
    def test_system_prompt_contains_label_and_attrs(self):
        attrs = AttributeSystem()
        prompt = build_system_prompt({"label": "史莱姆酱", "personality": "可爱"}, attrs)
        assert "史莱姆酱" in prompt
        assert "能量" in prompt
        assert "心情" in prompt

    def test_prompt_without_attrs(self):
        prompt = build_system_prompt({"label": "小汪"})
        assert "能量" not in prompt


class TestFallback:
    def test_keyword_match(self):
        fb = FallbackResponder()
        hello_pool = ["你好呀主人！(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧", "嗨嗨！今天也要开心哦~"]
        assert fb.respond("你好呀") in hello_pool
        assert fb.respond("我肚子好饿") in ["我也觉得肚子空空的，快喂我吃点东西吧~", "呜……好想吃好吃的 (｡•́︿•̀｡)"]
        assert fb.respond("拜拜") in ["拜拜主人，我会想你的！", "下次再来找我玩呀 (´▽`)"]

    def test_always_returns_text(self):
        fb = FallbackResponder()
        for _ in range(20):
            assert fb.respond("random stuff")
            assert len(fb.respond("")) > 0


class TestAIClient:
    def test_not_configured(self):
        client = AIClient()
        assert not client.is_configured()
        with pytest.raises(RuntimeError):
            client.chat([{"role": "user", "content": "hi"}])

    def test_is_configured(self):
        client = AIClient(base_url="https://example.com/v1", api_key="k", model="m")
        assert client.is_configured()


class TestProceduralRenderer:
    def test_render_all_states(self, qapp):
        renderer = ProceduralRenderer(colors={"body": "#ff6b9d", "belly": "#ffd6e0", "accent": "#ff3b6b"})
        for state in PetState:
            pm = renderer.render(state, 0.3)
            assert not pm.isNull()

    def test_dog_render(self, qapp):
        renderer = ProceduralRenderer(species="dog")
        pm = renderer.render(PetState.WALK, 0.5)
        assert not pm.isNull()
