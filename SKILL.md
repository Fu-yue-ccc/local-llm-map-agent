---
name: c4d-local-llm-map-agent
description: >
  使用本地大模型（Gemma 4 via Ollama）驱动 Agent 生成指定地点的交互式 HTML 地图。
  支持函数调用、结构化 JSON 输出、多轮 Agent 工作流。输入地点名称和数量，
  输出包含标记点、弹窗详情、分类图例的可交互 Folium 地图。
  Use whenever the user says "generate map with local LLM", "本地模型生成地图",
  "Gemma 4 地图", "Ollama 地图 Agent", "interactive map agent", "SIAS 地图",
  or provides a location name and asks to generate an interactive map using a local model.
  Also trigger when the user mentions C4D challenge together with map or local LLM.
---

# C4D 本地大模型地图 Agent

## Purpose

在不依赖云端 API 的情况下，使用本地运行的 Gemma 4 大模型驱动 Agent 工作流，
自动生成指定地点（如大学校园、城市景区）的交互式 HTML 地图。

核心价值：
- **零 API 费用**：所有推理在本地完成，无限次调用
- **数据隐私**：地点数据不离开你的设备
- **Agent 能力**：展示函数调用、结构化输出、多步推理等 Agent 技能
- **即开即用**：生成的 HTML 地图直接在浏览器打开，无需服务器

## Prerequisites

### 软件依赖
- Python 3.8+
- Ollama（本地模型运行器）
- Python 包：`requests`, `folium`

### 模型依赖
- 任意 Gemma 4 模型（E2B / E4B / 26B / 31B），已通过 Ollama 下载

### 安装命令
```bash
# 1. 安装 Ollama（Linux/Mac）
curl -fsSL https://ollama.com/install.sh | sh
# Windows: 从 ollama.com 下载安装包

# 2. 下载 Gemma 4 模型（选一个适合你设备的）
ollama pull gemma4:e4b    # 推荐入门，普通笔记本
ollama pull gemma4:e2b    # 最小，手机/老电脑

# 3. 安装 Python 依赖
pip install requests folium
```

## Input / Output

### 输入
- **地点名称**（必填）：如 "SIAS University"、"郑州大学"、"北京故宫"
- **地点数量**（可选，默认 8）：生成多少个标记点
- **模型名称**（可选，默认 gemma4:e4b）：使用哪个本地模型
- **输出文件名**（可选，默认 map.html）

### 输出
- **交互式 HTML 地图**：可缩放、可拖拽、点击标记显示详情
- **地点数据 JSON**：LLM 生成的结构化地点列表
- **验证报告**：地点数据质量检查结果

## Workflow

### Step 1 — 连接检查
检查 Ollama 服务是否运行，列出可用模型。
```
GET http://localhost:11434/api/tags
```

### Step 2 — Agent 生成地点数据（核心 Agent 能力）
通过 Ollama OpenAI 兼容 API 调用本地 Gemma 4：
- **System Prompt**：强制输出 valid JSON，定义字段结构和坐标范围
- **User Prompt**：指定地点名称和数量
- **结构化输出**：模型返回 JSON 数组，每个对象包含 name、name_zh、latitude、longitude、description、category

```json
[
  {
    "name": "Moscow Red Square",
    "name_zh": "莫斯科红场",
    "latitude": 34.4008,
    "longitude": 113.7662,
    "description": "校园内标志性欧式建筑群...",
    "category": "地标建筑"
  }
]
```

### Step 3 —（可选）函数调用演示
定义 `get_campus_info` 工具函数，让模型自主决定是否调用，展示 function calling 能力。

### Step 4 — 数据验证
自动检查 LLM 输出的质量：
- 必填字段完整性
- 坐标范围合理性（防止模型生成远离目标的坐标）
- 数据类型正确性

### Step 5 — 地图渲染
使用 Folium 生成交互式 HTML：
- OpenStreetMap 底图
- 按分类着色的标记点（10 种分类，10 种颜色）
- 点击弹窗显示中英文名称、类别、坐标、描述
- 悬浮提示显示中文名
- 固定图例和标题

## Usage

### 基本用法
```bash
# 默认：调用本地 gemma4:e4b 生成 8 个地点
python scripts/sias_map_agent.py

# 指定模型和地点数量
python scripts/sias_map_agent.py --model gemma4:e2b --locations 12

# 指定输出文件
python scripts/sias_map_agent.py --output my_campus.html
```

### 离线模式（无需 LLM）
```bash
# 使用内置的 SIAS 大学数据，不调用本地模型
python scripts/sias_map_agent.py --offline
```

### 函数调用演示
```bash
python scripts/sias_map_agent.py --demo-function-call
```

### 完整参数
```
--model MODEL           Ollama 模型名称 (默认: gemma4:e4b)
--base-url URL          Ollama API 地址 (默认: http://localhost:11434)
--locations N           生成地点数量 (默认: 8)
--output FILE           输出 HTML 文件名
--offline               离线模式（使用内置数据）
--skip-validation       跳过数据验证
--demo-function-call    演示函数调用能力
```

## Architecture

```
用户输入（地点名称+数量）
        │
        ▼
┌─────────────────┐
│  Ollama 连接检查  │  ← 确认本地模型可用
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  LocalLLMAgent   │  ← 核心 Agent 类
│  ├──────────────┤│
│  │ System Prompt ││  ← 强制 JSON 输出格式
│  │ User Prompt   ││  ← 地点名称+数量
│  │ Structured Out││  ← JSON 地点数组
│  └──────────────┤│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  数据验证器       │  ← 字段/坐标/类型检查
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Folium 地图生成  │  ← 交互式 HTML
│  ├──────────────┤│
│  │ 分类着色标记   ││
│  │ 弹窗详情       ││
│  │ 图例+标题      ││
│  └──────────────┤│
└────────┬────────┘
         │
         ▼
    map.html（浏览器打开）
```

## Edge Cases

| 情况 | 处理方式 |
|------|----------|
| Ollama 未启动 | 报错并提示启动命令，建议使用 --offline |
| 模型未下载 | 连接检查时列出可用模型，提示 ollama pull |
| LLM 输出非 JSON | 捕获异常，打印原始输出前200字符，切换到内置数据 |
| 坐标超出范围 | 验证器标记为异常，报告具体问题 |
| 缺少必填字段 | 验证器报告缺失字段 |
| 网络不可用 | 离线模式完全不依赖网络（地图底图除外） |
| 中文编码问题 | 全程 UTF-8，Folium 原生支持中文 |
| 大数量地点（>50） | 正常工作，但建议分批生成避免模型输出截断 |

## Customization

### 修改地点分类和颜色
编辑 `sias_map_agent.py` 中的 `category_colors` 字典：
```python
category_colors = {
    "校门": "red",
    "地标建筑": "blue",
    # 添加你的分类...
}
```

### 修改 System Prompt
编辑 `LocalLLMAgent.generate_locations()` 中的 `system_prompt` 变量，
可以调整输出字段、坐标范围、描述语言等。

### 修改地图样式
编辑 `generate_map()` 函数：
- `tiles`：底图样式（OpenStreetMap / Stamen Terrain / CartoDB）
- `zoom_start`：初始缩放级别
- 标记图标：`folium.Icon(color=..., icon=...)`

## File Structure

```
c4d-local-llm-map-agent/
├── SKILL.md                          # 本文件（技能说明）
├── scripts/
│   └── sias_map_agent.py            # 主程序（Agent + 地图生成）
└── references/
    └── sias_locations_reference.json # 内置参考数据（可选）
```

## Performance Notes

| 模型 | 内存占用 | 生成8地点耗时 | 推荐设备 |
|------|----------|--------------|----------|
| gemma4:e2b | ~5GB | ~10-20秒 | 8GB内存笔记本 |
| gemma4:e4b | ~5GB | ~15-30秒 | 16GB内存笔记本（推荐） |
| gemma4:26b | ~18GB | ~30-60秒 | 16GB+显存GPU |
| gemma4:31b | ~20GB | ~40-90秒 | 24GB+显存GPU |

> 实际速度取决于 CPU/GPU、内存带宽和量化级别。使用 GPU offload 可显著加速。

## License

本技能为 C4D 挑战提交作品，可自由使用和修改。
