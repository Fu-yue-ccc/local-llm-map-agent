# local-llm-map-agent

> 输入地点名称和数量，输出包含分类标记的交互式 HTML 地图。全程使用本地大模型（Gemma 4 via Ollama），零 API 费用，数据不离开你的设备。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Ollama](https://img.shields.io/badge/Ollama-compatible-green.svg)](https://ollama.com/)

---

## 解决什么问题

需要生成某个地点（大学校园、城市景区、公司园区）的交互式地图时，传统做法是：
1. 手动搜索每个地点的坐标
2. 手动整理成 JSON
3. 用地图库逐个添加标记

这个过程繁琐、重复、容易出错。

**有了 local-llm-map-agent 之后**：
1. 告诉模型"生成 SIAS 大学周边 10 个地点"
2. 本地 Gemma 4 自动输出结构化 JSON（名称、坐标、描述、分类）
3. 脚本自动渲染成可交互的 HTML 地图
4. 双击打开，即可缩放、点击、查看详情

全程在本地完成，不需要 Google Maps API Key，不需要联网调用云端 LLM。

---

## 快速开始

### 安装

```bash
# 1. 克隆仓库
git clone https://github.com/Fu-yue-ccc/local-llm-map-agent.git
cd local-llm-map-agent

# 2. 安装 Python 依赖
pip install requests folium

# 3. 安装 Ollama（如果还没装）
# Linux/Mac:
curl -fsSL https://ollama.com/install.sh | sh
# Windows: 从 https://ollama.com/download 下载安装包

# 4. 下载 Gemma 4 模型（选一个适合你设备的）
ollama pull gemma4:e4b    # 推荐：普通笔记本，约5GB内存
ollama pull gemma4:e2b    # 低配设备：约5GB内存，更小更快
```

### 使用

```bash
# 默认：调用本地 gemma4:e4b 生成 8 个地点
python scripts/sias_map_agent.py

# 指定模型和地点数量
python scripts/sias_map_agent.py --model gemma4:e2b --locations 12

# 指定输出文件
python scripts/sias_map_agent.py --output my_campus_map.html

# 离线模式（不调用 LLM，使用内置的 SIAS 大学数据）
python scripts/sias_map_agent.py --offline

# 演示函数调用能力
python scripts/sias_map_agent.py --demo-function-call
```

运行成功后，在浏览器中打开生成的 HTML 文件即可查看交互式地图。

---

## 示例

### 输入

```bash
python scripts/sias_map_agent.py --offline --locations 12 --output examples/sample_output.html
```

### 输出

生成的 HTML 地图包含：
- 📍 12 个分类标记点（10 种颜色对应 10 种分类）
- 🖱️ 可缩放、可拖拽、点击标记显示详情弹窗
- 📋 左下角固定图例（分类颜色对照）
- 🏷️ 顶部标题栏
- 🌐 OpenStreetMap 底图

示例输出见 [`examples/sample_output.html`](examples/sample_output.html)（SIAS 大学 12 个地点地图）。

### LLM 输出示例（结构化 JSON）

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

完整示例数据见 [`examples/sample_locations.json`](examples/sample_locations.json)。

---

## 项目结构

```
local-llm-map-agent/
├── README.md                 # 本文件
├── LICENSE                   # MIT 开源协议
├── .gitignore                # Git 忽略规则
├── AI_LOG.md                 # AI 辅助开发日志
├── ATTRIBUTION.md            # 借鉴来源与数据说明
├── SKILL.md                  # Claude Skill 格式（可直接安装为 Agent Skill）
├── scripts/
│   └── sias_map_agent.py     # 主程序（Agent + 验证器 + 地图生成）
├── examples/
│   ├── sample_output.html    # 示例地图输出
│   └── sample_locations.json # 示例地点数据
└── docs/
    └── usage.md              # 详细使用文档
```

---

## 技术栈

| 层次 | 技术 | 说明 |
|------|------|------|
| 语言 | Python 3.8+ | 核心开发语言 |
| 模型运行 | Ollama | 本地大模型运行器，OpenAI 兼容 API |
| 大模型 | Gemma 4 (E2B/E4B/26B/31B) | Google 开源，Apache 2.0，原生支持 function calling |
| HTTP 客户端 | requests | 调用 Ollama API |
| 地图渲染 | Folium | Python 交互式地图库，基于 Leaflet.js |
| 底图 | OpenStreetMap | 免费开源地图数据 |
| 数据格式 | JSON | LLM 结构化输出 |

---

## Agent 能力展示

本项目展示了以下 Agent 能力：

1. **结构化输出（Structured Output）**：通过 System Prompt 强制 LLM 输出 valid JSON，每个地点包含 6 个预定义字段
2. **函数调用（Function Calling）**：定义 `get_campus_info` 工具函数，模型自主决定是否调用
3. **多步工作流（Multi-step Workflow）**：连接检查 → 生成 → 验证 → 渲染，四步流水线
4. **自验证（Self-validation）**：生成后自动检查字段完整性、坐标范围、数据类型
5. **错误回退（Error Handling & Fallback）**：LLM 不可用时自动切换到内置数据，保证 100% 可用

---

## 支持的模型

| 模型 | 内存需求 | 推荐设备 | 生成8地点耗时 |
|------|----------|----------|--------------|
| gemma4:e2b | ~5GB | 8GB 笔记本/手机 | ~10-20秒 |
| gemma4:e4b | ~5GB | 16GB 笔记本（推荐） | ~15-30秒 |
| gemma4:26b | ~18GB | 16GB+ 显存 GPU | ~30-60秒 |
| gemma4:31b | ~20GB | 24GB+ 显存 GPU | ~40-90秒 |

---

## 自定义

### 修改地点分类和颜色

编辑 `scripts/sias_map_agent.py` 中的 `category_colors` 字典：

```python
category_colors = {
    "校门": "red",
    "地标建筑": "blue",
    # 添加你的分类...
}
```

### 生成其他地点的地图

修改 `LocalLLMAgent.generate_locations()` 中的 `user_prompt`，将 "SIAS University" 改为目标地点名称，同时修改 `generate_map()` 中的 `center_lat` 和 `center_lon`。

### 修改地图样式

在 `generate_map()` 函数中：
- `tiles="OpenStreetMap"` → 改为 `"CartoDB positron"`（简洁白底）
- `zoom_start=15` → 调整初始缩放级别

---

## AI 生成说明

本项目使用 AI（豆包 Doubao）辅助开发，包括代码生成、文档撰写、架构设计和调试辅助。所有 AI 生成内容均经过人工审查和测试验证。

详细 AI 使用记录见 [`AI_LOG.md`](AI_LOG.md)。

---

## 借鉴来源

本项目参考了以下开源项目和公开资料，详见 [`ATTRIBUTION.md`](ATTRIBUTION.md)。

---

## License

[MIT](LICENSE) - 可自由使用、修改和分发。
