# AI 辅助开发日志 — local-llm-map-agent

> 本项目使用豆包（Doubao）大语言模型辅助开发。
> 所有 AI 生成内容均经过人工审查和测试验证。

---

## 一、AI 使用总览

| 阶段 | AI 用途 | 轮次 | 关键产出 |
|------|---------|------|----------|
| 项目初始化 | 生成 repo 骨架、README 模板、.gitignore | 2 | 标准项目结构 |
| 代码编写 | 生成 Agent 类、验证器、地图生成器、argparse | 4 | 430 行 Python 代码 |
| 文档撰写 | README、使用文档、拿来说明 | 3 | 完整文档体系 |
| 调试修复 | folium 安装、脚本运行错误修复 | 2 | 可运行的最终代码 |
| 代码审查 | AI review 安全问题和性能瓶颈 | 1 | 审查意见清单 |
| **合计** | | **12** | |

---

## 二、分阶段记录

### 阶段 1：项目初始化（2 轮）

**第 1 轮**
- Prompt：「帮我创建一个 Python 项目的标准 GitHub repo 结构，包含 README、LICENSE、.gitignore、src、examples、docs、tests。」
- AI 输出：标准目录结构和各文件的初始内容。
- 人工修改：根据项目实际情况调整目录结构（使用 scripts/ 而非 src/，因为是单脚本项目），补充 AI 相关文件（AI_LOG.md、ATTRIBUTION.md）。

**第 2 轮**
- Prompt：「生成一个 Python 项目的 .gitignore，包含 Python 虚拟环境、IDE 文件、OS 文件、输出 HTML 文件、Ollama 数据目录。」
- AI 输出：完整的 .gitignore 文件。
- 人工核验：确认所有规则合理，添加了 `*_map.html` 规则防止生成的地图文件被提交。

### 阶段 2：代码编写（4 轮）

**第 1 轮 — 核心框架**
- Prompt：「生成 sias_map_agent.py 的核心框架，包括 LocalLLMAgent 类（check_connection, generate_locations, function_call_demo）、validate_locations 函数、generate_map 函数、main 函数和 argparse 参数解析。」
- AI 输出：约 300 行代码框架。
- 人工审查：确认类设计合理，参数完整，补充了分类着色和图例功能。

**第 2 轮 — 内置数据**
- Prompt：「根据搜索到的 SIAS 大学真实信息，生成 BUILTIN_LOCATIONS 列表，包含至少 10 个地点，每个地点有 name、name_zh、latitude、longitude、description、category 字段。」
- AI 输出：12 个地点的数据。
- 人工核验：正门、体育馆、堪萨斯国际学院使用高德地图精确坐标；其他建筑坐标基于校园布局合理估算；描述内容基于公开搜索信息。

**第 3 轮 — 地图样式增强**
- Prompt：「增强 generate_map 函数，添加分类着色标记点（10种分类10种颜色）、固定图例、顶部标题栏、丰富的弹窗 HTML。」
- AI 输出：补充了 category_colors 字典、legend_html、title_html、popup_html。
- 人工测试：运行脚本验证所有样式正常显示。

**第 4 轮 — 错误处理**
- Prompt：「完善错误处理：LLM 输出非 JSON 时的清理逻辑、连接失败提示、JSON 解析失败时切换内置数据、所有异常的捕获。」
- AI 输出：补充了 content 清理、ConnectionError 捕获、JSONDecodeError 捕获、通用 Exception 捕获。
- 人工审查：确认异常处理覆盖所有失败点，失败时有明确用户提示和回退方案。

### 阶段 3：文档撰写（3 轮）

**第 1 轮 — README**
- Prompt：「根据项目代码写一个完整的 README.md，包含：项目名称、一句话描述、解决什么问题、快速开始（安装+使用）、示例（输入输出）、项目结构、技术栈、AI 生成说明、借鉴来源、License。」
- AI 输出：完整的 README 初稿。
- 人工修改：补充了 Agent 能力展示、支持的模型对比表、自定义指南，修正了安装命令中的路径。

**第 2 轮 — 使用文档**
- Prompt：「写一份详细的使用文档 docs/usage.md，包含：所有命令行参数说明、离线模式使用方法、函数调用演示、常见问题 FAQ、性能调优建议。」
- AI 输出：详细使用文档。
- 人工补充：添加了 Windows/Mac/Linux 三平台的 Ollama 安装说明。

**第 3 轮 — 拿来说明**
- Prompt：「写 ATTRIBUTION.md，列出所有使用的开源库、工具、参考资料、数据来源，包含许可证信息。」
- AI 输出：依赖库列表和参考资料。
- 人工补充：添加了数据来源的详细核实方法（高德地图 POI、西亚斯官网、公开旅游信息）。

### 阶段 4：调试修复（2 轮）

**第 1 轮 — folium 安装**
- 问题：运行脚本提示 ModuleNotFoundError: No module named 'folium'
- AI 辅助：确认依赖名称正确，folium 会自动安装 jinja2、branca 等依赖。
- 解决：`pip install folium requests`

**第 2 轮 — 脚本运行验证**
- 问题：首次运行时需要确认 argparse 参数定义正确。
- AI 辅助：检查 --offline 参数为 store_true 类型，默认 False。
- 解决：运行 `python3 sias_map_agent.py --offline --locations 12` 成功，12/12 地点通过验证，地图生成成功。

### 阶段 5：代码审查（1 轮）

- Prompt：「审查这个 Python 脚本的安全问题和性能瓶颈，重点检查：用户输入处理、文件写入、网络请求、异常处理、资源泄漏。」
- AI 输出：审查意见清单。
- 人工处理：
  - ✅ 网络请求有超时控制（timeout=120）
  - ✅ 文件写入使用 folium 库，无路径遍历风险
  - ✅ 异常处理覆盖主要失败点
  - ⚠️ 建议添加日志记录（已通过 print 输出实现，对于 CLI 工具足够）
  - ⚠️ 建议添加类型注解（后续改进项）

---

## 三、AI 生成内容的人工核验记录

| AI 生成内容 | 核验方式 | 结果 |
|---|---|---|
| 项目结构 | 对照 GitHub 标准 Python 项目规范 | ✅ 合理 |
| .gitignore 规则 | 逐条检查是否会误删必要文件 | ✅ 正确 |
| Ollama API 调用格式 | 对照 Ollama 官方文档 | ✅ 正确 |
| folium 标记颜色名称 | 对照 Folium 官方文档颜色列表 | ✅ 有效 |
| 12 个地点坐标 | 高德地图 POI + 范围验证器 | ✅ 全部通过 |
| README 安装命令 | 实际运行验证 | ✅ 可执行 |
| argparse 参数定义 | 实际运行 --help 验证 | ✅ 正确 |

---

## 四、手动编写的内容（非 AI 生成）

以下内容为人工手动编写，未使用 AI 生成：
- BUILTIN_LOCATIONS 中 3 个精确坐标（正门、体育馆、堪萨斯国际学院）来自高德地图人工查询
- 离线模式测试的实际运行结果
- 代码审查后的修改决策

---

## 五、AI 误导案例

### 案例：SIAS 大学坐标偏差
- AI 初始给出的坐标为 34.40°N, 113.73°E
- 实际高德地图精确坐标为 34.401422°N, 113.765004°E
- 偏差：经度约 3.5 公里
- 发现方式：人工在高德地图搜索验证
- 对策：所有精确坐标必须通过地图服务查询验证，代码中内置坐标范围验证器
