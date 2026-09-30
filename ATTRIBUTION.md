# 借鉴来源与数据说明 — local-llm-map-agent

> 本项目遵循"拿来主义"原则：站在巨人的肩膀上，明确标注所有借鉴来源。

---

## 一、使用的开源库与工具

| 库/工具 | 版本 | 用途 | 许可证 | 官网 |
|---------|------|------|--------|------|
| Python | 3.8+ | 编程语言 | PSF | https://www.python.org |
| Ollama | 最新版 | 本地大模型运行器 | MIT | https://ollama.com |
| requests | 最新版 | HTTP 客户端（调用 Ollama API） | Apache 2.0 | https://docs.python-requests.org |
| Folium | 最新版 | 交互式地图生成 | MIT | https://python-visualization.github.io/folium/ |
| Leaflet.js | 1.x（Folium 内置） | 前端交互式地图库 | BSD-2 | https://leafletjs.com |
| OpenStreetMap | — | 地图底图数据 | ODbL | https://www.openstreetmap.org |

### 大模型

| 模型 | 参数量 | 许可证 | 来源 |
|------|--------|--------|------|
| Gemma 4 E2B | ~2B effective | Apache 2.0 | Google DeepMind |
| Gemma 4 E4B | ~4.5B effective | Apache 2.0 | Google DeepMind |
| Gemma 4 26B MoE | 26B total / 3.8B active | Apache 2.0 | Google DeepMind |
| Gemma 4 31B Dense | 31B | Apache 2.0 | Google DeepMind |

> Gemma 4 由 Google DeepMind 开发，2025 年发布，Apache 2.0 协议，可自由使用、修改和分发。
> 参考：https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/

---

## 二、参考资料

### 官方文档

| 资料 | 用途 | 链接 |
|------|------|------|
| Ollama 官方文档 | Ollama API 使用方法、模型管理 | https://github.com/ollama/ollama |
| Ollama OpenAI 兼容 API | /v1/chat/completions 接口规范 | https://ollama.com/blog/openai-compatibility |
| Folium 官方文档 | 地图生成、标记、弹窗用法 | https://python-visualization.github.io/folium/ |
| Gemma 4 技术报告 | 模型架构、能力、硬件需求 | https://ai.google.dev/gemma |
| Leaflet.js 文档 | 前端地图交互原理 | https://leafletjs.com/reference.html |

### 挑战材料

| 文件 | 来源 | 用途 |
|------|------|------|
| C4.pdf | Elite20 挑战 C4 主任务说明 | 技能四条件、提交规范、评分标准 |
| C4D.pdf | Elite20 挑战 C4D 任务说明 | 本地大模型 Agent 具体要求、四级任务、交付物清单 |
| C5.pdf | Elite20 挑战 C5 任务说明 | GitHub repo 标准、README 模板、检查清单 |

### 参考技能（来自 C4 主任务示例）

| 技能 | 参考点 |
|------|--------|
| wechat-doc-mapper.skill | .skill 包结构、SKILL.md 写法、scripts/ + references/ 组织 |
| skill-explainer.skill | 纯指令型技能写法、四维评审矩阵设计 |

---

## 三、数据来源

### SIAS 大学地点数据

| 数据项 | 来源 | 获取方式 |
|--------|------|----------|
| 学校正门坐标 (34.401422, 113.765004) | 高德地图 POI | 联网搜索"郑州西亚斯学院 经纬度" |
| 综合体育馆坐标 (34.399654, 113.766787) | 高德地图 POI | 联网搜索 |
| 堪萨斯国际学院坐标 (34.395225, 113.769275) | 高德地图 POI | 联网搜索 |
| 学校地址（人民路东段168号） | 西亚斯学院官网 | sias.edu.cn 联系我们页面 |
| 校园建筑信息（莫斯科红场、欧洲街、伦敦街、法国园等） | 抖音校园介绍视频 + 携程酒店周边信息 | 联网搜索"西亚斯学院 校园 地标" |
| 渔夫子亭历史背景 | 抖音文化介绍 + 新郑地方史料 | 联网搜索"渔夫子亭 西亚斯" |
| 周边景点（郑风苑、轩辕湖） | 携程旅行攻略 + 高德地图 | 联网搜索"新郑 景点" |

### 数据核实方法

所有内置地点数据均经过以下核实流程：
1. **坐标核实**：在高德地图中搜索对应地点，确认经纬度
2. **名称核实**：中英文名称对照官方信息
3. **描述核实**：描述内容基于多个公开来源交叉验证
4. **分类核实**：地点分类基于实际功能判断
5. **范围验证**：脚本内置验证器检查所有坐标在合理范围内（34.30-34.50, 113.65-113.85）

---

## 四、代码借鉴声明

本项目代码为原创编写，参考了以下公开资源的设计思路（非直接复制）：

1. **Ollama API 调用方式**：参考 Ollama 官方文档中的 OpenAI 兼容 API 示例
2. **Folium 标记和弹窗用法**：参考 Folium 官方文档中的 Quickstart 示例
3. **.skill 包结构**：参考 Elite20 C4 主任务提供的 wechat-doc-mapper.skill 和 skill-explainer.skill 的目录组织方式
4. **SKILL.md 格式**：参考 Claude Skill 官方规范（YAML frontmatter + Markdown body）
5. **README 模板**：参考 C5.pdf 中提供的 README 标准模板

---

## 五、AI 使用声明

本项目在开发过程中使用了豆包（Doubao）大语言模型辅助：
- 代码框架设计和生成
- 文档撰写和润色
- 错误排查和修复
- 架构设计讨论

所有 AI 生成的代码均经过人工审查和测试验证。AI 使用的详细记录见 [AI_LOG.md](AI_LOG.md)。

---

## 六、许可证

本项目代码采用 MIT 许可证。使用的第三方库和工具均遵循其各自的开源许可证。

地图底图数据（OpenStreetMap）遵循 ODbL 许可证，使用时需注明来源。
