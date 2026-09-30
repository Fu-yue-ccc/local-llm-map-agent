# C5 拿来说明

> local-llm-map-agent GitHub 项目的借鉴来源与数据说明

---

## 一、使用的开源库与工具

| 库/工具 | 用途 | 许可证 |
|---------|------|--------|
| Python 3.8+ | 编程语言 | PSF |
| Ollama | 本地大模型运行器 | MIT |
| requests | HTTP 客户端 | Apache 2.0 |
| Folium | 交互式地图生成 | MIT |
| Leaflet.js | 前端地图库（Folium 内置） | BSD-2 |
| OpenStreetMap | 地图底图数据 | ODbL |
| Gemma 4 | 本地大模型 | Apache 2.0 |

## 二、参考资料

| 资料 | 来源 | 用途 |
|------|------|------|
| C5.pdf | Elite20 挑战材料 | GitHub repo 标准、README 模板、检查清单 |
| C4D.pdf | Elite20 挑战材料 | 本地大模型 Agent 任务要求 |
| Ollama 官方文档 | ollama.com | API 调用方法 |
| Folium 官方文档 | python-visualization.github.io | 地图生成用法 |
| NEOLAF 论文 | arXiv:2308.03990 | Agent 架构参考 |
| wechat-doc-mapper.skill | Elite20 C4 示例 | .skill 包结构参考 |
| skill-explainer.skill | Elite20 C4 示例 | SKILL.md 格式参考 |

## 三、代码来源

- **核心脚本** `scripts/sias_map_agent.py`：基于 C4D 任务开发的代码，为原创编写，参考了 Ollama API 文档和 Folium Quickstart 示例
- **SKILL.md**：参考 Elite20 C4 示例技能的格式，内容为原创
- **README.md**：参考 C5.pdf 提供的标准模板，内容为原创
- **.gitignore**：参考 GitHub Python 项目标准模板

## 四、数据来源

SIAS 大学地点数据来自：
- 高德地图 POI（正门、体育馆、堪萨斯国际学院的精确坐标）
- 西亚斯学院官网（地址、联系方式）
- 公开旅游信息（校园建筑介绍、周边景点）

所有坐标数据经过脚本内置验证器检查范围合理性。

## 五、AI 使用声明

本项目使用豆包（Doubao）大语言模型辅助开发，包括代码生成、文档撰写、架构设计。所有 AI 生成内容均经过人工审查和测试验证。详细记录见 repo 内的 AI_LOG.md。
