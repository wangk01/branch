# Requirements Document

## Introduction

开发一款 Windows 桌面宠物应用。宠物以透明无边框窗口形式常驻桌面，可吸附到屏幕侧边栏；在无人操作时自主产生行为（散步、打瞌睡、玩耍、讨食等）；支持用户定制宠物外观；支持接入 AI 大模型进行自然语言对话；可打包为 Windows exe 安装程序分发。

## Glossary

- **系统 (System)**: Windows 桌面宠物应用，以下统称"桌宠系统"
- **宠物 (Pet)**: 桌面上的动画角色实体
- **行为 (Behavior)**: 宠物执行的动画动作，如散步、打瞌睡、玩耍、睡觉、讨食
- **属性 (Attribute)**: 宠物的状态参数，如能量、饥饿、清洁、心情
- **状态机 (State Machine)**: 管理宠物行为切换的核心逻辑模块
- **侧边栏模式 (Sidebar Mode)**: 宠物吸附在屏幕边缘时的展示形态
- **AI 会话 (AI Session)**: 用户与宠物之间的多轮对话
- **角色包 (Character Pack)**: 一套完整的宠物外观素材与配置，包含动画与元数据

## Requirements

### Requirement 1: 桌面宠物窗口

**User Story:** AS 用户, I want 宠物以悬浮窗口常驻桌面, so that 宠物随时可见且不干扰其他应用

#### Acceptance Criteria

1. WHEN 系统启动, 桌宠系统 SHALL 显示一个无边框、透明背景、置顶的宠物窗口
2. WHEN 宠物窗口显示, 桌宠系统 SHALL 允许用户拖拽移动宠物到屏幕任意位置
3. WHEN 宠物被拖拽到屏幕边缘, 桌宠系统 SHALL 自动吸附到侧边栏并以侧边栏模式展示
4. WHEN 宠物处于侧边栏模式, 桌宠系统 SHALL 收起非必要内容, 仅保留紧凑的宠物形象

### Requirement 2: 自主行为

**User Story:** AS 用户, I want 宠物在无人操作时自主产生行为, so that 宠物看起来有生命力

#### Acceptance Criteria

1. WHEN 宠物闲置超过一定时长, 桌宠系统 SHALL 触发自主行为决策
2. WHEN 宠物进入散步行为, 桌宠系统 SHALL 在屏幕上沿水平方向移动宠物并播放散步动画
3. WHEN 宠物进入打瞌睡行为, 桌宠系统 SHALL 播放打瞌睡动画并保持原地
4. WHEN 宠物进入玩耍行为, 桌宠系统 SHALL 播放玩耍动画
5. WHEN 宠物属性达到阈值, 桌宠系统 SHALL 触发对应行为 (WHEN 能量过低 THEN 强制入睡, WHEN 饥饿过高 THEN 讨食)
6. WHILE 用户正在操作宠物, 桌宠系统 SHALL 暂停自主行为决策

### Requirement 3: 属性系统

**User Story:** AS 用户, I want 宠物拥有成长属性, so that 互动更有反馈感

#### Acceptance Criteria

1. 桌宠系统 SHALL 维护能量、饥饿、清洁、心情四项属性
2. WHEN 时间流逝, 桌宠系统 SHALL 按配置速率消耗能量并增加饥饿
3. WHEN 用户喂食, 桌宠系统 SHALL 降低宠物饥饿值
4. WHEN 用户为宠物洗澡, 桌宠系统 SHALL 提升清洁值
5. WHEN 用户与宠物互动, 桌宠系统 SHALL 提升心情值
6. 桌宠系统 SHALL 在退出时将宠物属性持久化保存, 下次启动恢复

### Requirement 4: 交互方式

**User Story:** AS 用户, I want 通过多种方式与宠物互动, so that 体验直观有趣

#### Acceptance Criteria

1. WHEN 用户单击宠物, 桌宠系统 SHALL 播放抚摸动画并提升心情
2. WHEN 用户双击宠物, 桌宠系统 SHALL 播放兴奋反应动画
3. WHEN 用户拖拽宠物, 桌宠系统 SHALL 模拟抱起状态
4. WHEN 用户右键点击宠物, 桌宠系统 SHALL 弹出操作菜单 (喂食、洗澡、玩耍、聊天、设置、切换角色、退出)

### Requirement 5: AI 对话

**User Story:** AS 用户, I want 与宠物进行自然语言对话, so that 宠物能智能回复

#### Acceptance Criteria

1. WHEN 用户点击聊天入口, 桌宠系统 SHALL 打开对话窗口
2. WHEN 对话窗口打开, 桌宠系统 SHALL 展示与宠物的多轮对话记录
3. WHEN 用户发送消息, 桌宠系统 SHALL 将消息连同宠物性格设定与当前状态发送给 AI 模型
4. WHEN AI 模型返回回复, 桌宠系统 SHALL 将回复展示在对话窗口中并可选播放回应动画
5. WHEN 未配置 AI 模型, 桌宠系统 SHALL 使用本地预设的回复模板降级响应
6. 桌宠系统 SHALL 在设置中支持配置 AI 模型的 API 地址、密钥与模型名称

### Requirement 6: 宠物定制

**User Story:** AS 用户, I want 定制自己的宠物外观, so that 宠物具有个性化

#### Acceptance Criteria

1. 桌宠系统 SHALL 内置至少两个角色包 (默认角色 + 备用角色)
2. 桌宠系统 SHALL 支持从指定目录导入自定义角色包
3. 每个角色包 SHALL 包含待机、行走、睡觉、抚摸等动作动画素材与角色配置
4. WHEN 用户切换角色, 桌宠系统 SHALL 卸载当前角色并加载新角色的动画资源

### Requirement 7: 系统托盘

**User Story:** AS 用户, I want 从系统托盘快速管理宠物, so that 不占用任务栏空间

#### Acceptance Criteria

1. 桌宠系统 SHALL 在系统托盘显示宠物图标
2. WHEN 用户点击托盘图标, 桌宠系统 SHALL 显示托盘菜单 (显示/隐藏宠物、切换角色、设置、退出)
3. WHEN 用户从托盘选择退出, 桌宠系统 SHALL 保存属性数据并退出程序

### Requirement 8: 打包与安装

**User Story:** AS 用户, I want 将桌宠打包为 exe 安装程序, so that 可直接安装使用

#### Acceptance Criteria

1. 桌宠系统 SHALL 提供将应用打包为 Windows 可执行文件的构建脚本
2. 打包产物 SHALL 包含所有内置角色素材与依赖
3. 桌宠系统 SHALL 提供可选的安装程序生成方式 (NSIS/Inno Setup)
4. 打包后的应用 SHALL 在无 Python 环境的 Windows 10/11 上正常运行

### Requirement 9: 数据持久化

**User Story:** AS 用户, I want 宠物记住我的设定与状态, so that 重启后不丢失

#### Acceptance Criteria

1. 桌宠系统 SHALL 将用户配置 (当前角色、AI 设置、行为参数) 保存到本地配置文件
2. 桌宠系统 SHALL 将宠物属性与对话历史保存到本地数据目录
3. 桌宠系统 SHALL 在应用目录或用户目录创建数据存储位置
