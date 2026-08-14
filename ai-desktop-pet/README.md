# AI Desktop Pet（AI 桌宠）

一个 AI 驱动的 Windows 桌面宠物。宠物以透明置顶窗口常驻桌面，可吸附侧边栏；无人操作时自主产生行为（散步、打瞌睡、玩耍、讨食等）；支持右键交互、AI 对话、角色定制，可打包为 exe 安装程序。

## 功能特性

- **桌面宠物窗口**：无边框、透明背景、置顶；可拖拽移动，拖到屏幕边缘自动吸附侧边栏
- **自主行为**：闲置自动触发散步/打瞌睡/玩耍等，由行为决策器根据属性状态与随机权重驱动
- **属性系统**：能量、饥饿、清洁、心情四项属性随时间变化，过低会触发对应行为（困倦入睡、讨食、求洗澡）
- **交互方式**：单击抚摸、双击兴奋、拖拽抱起、右键菜单（喂食/洗澡/玩耍/聊天）
- **AI 对话**：接入 OpenAI 兼容 API（支持 DeepSeek、OpenAI、本地 ollama 等），宠物会结合当前心情与属性回复；未配置时自动降级为预设回复
- **角色定制**：内置史莱姆酱与小狗两个程序绘制角色，支持导入自定义素材角色包，支持 ComfyUI 从参考图生成动作动画
- **系统托盘**：显示/隐藏、切换角色、设置、退出
- **打包安装**：PyInstaller 打包 exe + NSIS 生成安装程序，GitHub Actions 自动构建

## 快速开始

### 环境要求

- Windows 10/11 或 Python 3.10+（源码运行）
- Linux/macOS 仅支持源码运行调试，打包 exe 需在 Windows 环境执行

### 源码运行

```bash
pip install -r requirements.txt
python main.py
```

### AI 配置

运行后在系统托盘或右键菜单打开「设置」，填入：

- **API 地址**：OpenAI 兼容接口，如 `https://api.deepseek.com/v1`
- **API Key**：你的模型服务密钥
- **模型名称**：如 `deepseek-chat`

未配置时宠物仍可运行，AI 对话自动使用内置模板回复。

## 打包为 exe

### 方式一：本地打包（Windows）

```bat
pip install -r requirements.txt pyinstaller
build\build.bat
```

产物在 `dist\AIDesktopPet\`，运行 `AIDesktopPet.exe`。

### 方式二：生成安装程序

安装 [NSIS](https://nsis.sourceforge.io/) 后：

```bat
build\make_installer.bat
```

生成 `dist\AIDesktopPet-Setup.exe`，双击即可安装。

### 方式三：GitHub Actions 自动打包

推送 `v*` 标签或在 Actions 手动触发 `build-windows` 工作流，自动在 Windows 环境打包并上传产物，`v*` 标签自动发布 Release。

## 添加自定义角色

### 方式一：导入现成素材

准备素材目录（GIF 或 PNG 序列帧）：

```
my_character/
  idle.gif          # 待机（必需）
  walk.gif          # 行走
  sleep.gif         # 睡觉
  stroke.gif        # 抚摸
  play.gif          # 玩耍
  eat.gif           # 喂食
  ...
```

运行导入脚本：

```bash
python scripts/import_character.py --source-dir D:\my_character --asset-id my_char --label "我的角色" --set-current
```

### 方式二：ComfyUI 生成动作

1. 准备角色全身参考图
2. 启动本地 ComfyUI（`127.0.0.1:8188`）
3. 逐个生成动作：

```bash
python scripts/generate_motion.py --asset-id my_char --slot idle --reference reference.png
python scripts/generate_motion.py --asset-id my_char --slot walk --reference reference.png
```

ComfyUI 工作流模板在 `comfyui/workflows/`，可按本地节点安装情况替换。

## 角色包结构

```
assets/base/<角色ID>/
  character.json    # 角色配置（id/label/personality/species/colors/animations）
  idle/             # 序列帧目录（可选，无则用程序绘制）
  ...
```

`character.json` 的 `animations` 字段示例：

```json
{
  "id": "my_char",
  "label": "我的角色",
  "personality": "傲娇、毒舌",
  "species": "slime",
  "colors": {"body": "#ff6b9d", "belly": "#ffd6e0", "accent": "#ff3b6b"},
  "animations": {
    "idle": {"type": "sequence", "frames_dir": "idle", "fps": 10},
    "walk": {"type": "sequence", "frames_dir": "walk", "fps": 12}
  }
}
```

动作槽位：`idle`（必需）、`walk`、`sleep`、`carried`、`stroke`、`play`、`eat`、`bath`、`double_click`、`drowsy`、`hungry`、`dirty`、`sad`。缺少的槽位自动回退程序绘制或禁用对应功能。

## 项目结构

```
├── main.py                 # 主程序入口
├── config.py               # 配置参数
├── core/                   # 状态机、行为决策、属性系统、事件总线、角色加载
├── ai/                     # OpenAI 兼容客户端、性格提示词、降级回复
├── animation/              # 程序绘制渲染器、序列帧播放器、动画管理器
├── ui/                     # 宠物窗口、聊天窗口、设置窗口、系统托盘
├── data/                   # JSON 存储与路径管理
├── comfyui/                # ComfyUI 客户端与工作流模板
├── scripts/                # 角色导入、动画生成、图标生成工具
├── assets/                 # 内置角色包与图标
├── build/                  # PyInstaller spec、build.bat、NSIS 脚本
└── tests/                  # 单元测试
```

## 开发

```bash
pip install -r requirements.txt pytest
python -m pytest
```

Linux 无头环境冒烟测试：

```bash
QT_QPA_PLATFORM=offscreen timeout 10 python -c "import sys; sys.path.insert(0,'.'); from PySide6.QtWidgets import QApplication; from main import DesktopPetApp; app=QApplication([]); app.setQuitOnLastWindowClosed(False); p=DesktopPetApp(); p.run(); app.processEvents(); print('smoke ok')"
```

## 测试策略

- `core`：状态迁移、属性衰减与持久化、行为决策触发
- `ai`：提示词构建、降级回复、客户端配置
- `animation`：各状态渲染有效性

## 许可证

MIT
