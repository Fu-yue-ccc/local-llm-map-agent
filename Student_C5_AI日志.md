# C5 AI 协作日志

> GitHub Repository 项目开发全过程 AI 使用记录
> 项目：local-llm-map-agent
> 日期：2026-09-30

---

## 一、AI 使用总览

| 阶段 | 轮次 | 主要用途 | 关键产出 |
|------|------|----------|----------|
| 任务解析 | 2 | 阅读 C5.pdf、C5A.pdf、challenge.json，梳理交付物 | 任务理解框架 |
| 信息检索 | 3 | 搜索 neolaf2/neoskills、NEOLAF 架构、GitHub 规范 | 真实参考资料 |
| Repo 结构设计 | 2 | 讨论 GitHub 标准项目结构、README 模板 | 目录结构 |
| 代码复用 | 2 | 基于 C4D 代码调整为 GitHub repo 格式 | 脚本+SKILL.md |
| 文档撰写 | 5 | README、AI_LOG、ATTRIBUTION、usage.md、提交文档 | 完整文档体系 |
| 调试验证 | 2 | 验证脚本可运行、地图可生成 | 可运行的最终代码 |
| **合计** | **16** | | |

---

## 二、分阶段详细记录

### 阶段 1：任务解析（2 轮）

**第 1 轮**
- Prompt：「解读 C5.pdf，列出 GitHub repo 必须包含的文件、README 标准模板、评判标准和检查清单。」
- AI 输出：整理出 8 项必需文件（README/代码/使用说明/LICENSE/.gitignore/AI_LOG/ATTRIBUTION/示例）、README 9 段标准结构、5 项评判标准、9 项检查清单。
- **人工核验**：对照 C5.pdf 原文，确认所有要求准确。特别注意到 C5 强调"别人 clone 后 5 分钟内能跑起来"。

**第 2 轮**
- Prompt：「C5 和 C5A 有什么区别？各自需要交付什么？C5A 要求 fork neolaf2/neoskills 仓库，这个仓库我在云端能访问吗？」
- AI 输出：C5 是创建自己的 GitHub repo，C5A 是 GitHub 入门（创建账号+fork+clone+仓库分析）。neolaf2/neoskills 可能是课程私有仓库，云端可能无法直接访问。
- **人工判断**：C5 和 C5A 是两个独立但相关的任务。C5 可以基于 C4D 的技能创建 repo。C5A 的仓库分析需要基于公开资料+用户自己 clone 后的验证。

### 阶段 2：信息检索（3 轮）

**第 1 轮 — neolaf2/neoskills 仓库**
- Prompt：「搜索 neolaf2/neoskills GitHub 仓库的内容、结构、包含的技能。」
- AI 输出：搜索结果中没有直接找到该仓库的详细内容，找到了 neolaf.com 官网和 neo-work-template 项目。
- **人工补充**：直接尝试 web.fetch 访问 GitHub 页面，被 robots.txt 阻止。尝试 GitHub API，访问失败。判断该仓库可能为私有或新建。决定基于 NEOLAF 公开资料（arXiv:2308.03990、neolaf.com）和 Agent Skills 标准规范撰写分析，并标注用户 clone 后可验证。

**第 2 轮 — NEOLAF 架构**
- Prompt：「搜索 NEOLAF 认知架构的详细信息，包括系统1/系统2设计、KSTAR 增量学习、神经符号融合。」
- AI 输出：找到 arXiv 论文 "NEOLAF, an LLM-powered neural-symbolic cognitive architecture"（2308.03990），以及 neolaf.com 官网的架构对比表。
- **人工核验**：确认 NEOLAF 是一个 LLM 驱动的神经符号认知架构，使用 system-1（快速零样本）和 system-2（慢速推理+外部服务）双层设计。

**第 3 轮 — GitHub 最佳实践**
- Prompt：「GitHub 上一个好的 Python 项目 README 应该包含什么？.gitignore 标准模板是什么？MIT LICENSE 的标准文本是什么？」
- AI 输出：README 应包含项目描述、安装、使用、示例、项目结构、技术栈、贡献指南、许可证。.gitignore 应包含 __pycache__、venv、.env、.DS_Store 等。MIT 许可证有标准文本。
- **人工核验**：对照 GitHub 官方文档和 C5.pdf 中的 README 模板，确认结构完整。

### 阶段 3：Repo 结构设计（2 轮）

**第 1 轮**
- Prompt：「基于 C4D 的本地大模型地图 Agent，设计一个标准 GitHub repo 结构。需要包含 C5 要求的所有文件。」
- AI 输出：建议结构为 README.md、LICENSE、.gitignore、AI_LOG.md、ATTRIBUTION.md、SKILL.md、scripts/、examples/、docs/、tests/。
- **人工修改**：去掉 tests/（项目较小，暂不需要），将 C4D 的代码复制到 scripts/，将生成的地图放到 examples/ 作为示例输出。

**第 2 轮**
- Prompt：「README 的一句话描述怎么写才吸引人？需要包含输入输出。」
- AI 输出："输入地点名称和数量，输出包含分类标记的交互式 HTML 地图。全程使用本地大模型，零 API 费用。"
- **人工判断**：这个描述清晰说明了输入输出和核心价值（零 API 费用），符合 C5 要求。

### 阶段 4：代码复用（2 轮）

**第 1 轮**
- Prompt：「C4D 的 sias_map_agent.py 直接放到 GitHub repo 里需要做什么修改？」
- AI 输出：需要修改默认输出文件名（去掉 Student_C4D_ 前缀）、添加模块 docstring、确保路径引用正确。
- **人工操作**：直接复制 C4D 的脚本到 repo 的 scripts/ 目录，代码本身已经足够规范，不需要大改。默认输出文件名保留，因为这是 C4D 的命名规范。

**第 2 轮**
- Prompt：「SKILL.md 作为 Claude Skill 文件，需要满足什么格式要求？」
- AI 输出：需要 YAML frontmatter（name + description + 触发短语）+ Markdown body（Purpose/Prerequisites/Workflow/Usage/Edge Cases）。
- **人工核验**：对照 C4 材料中的 wechat-doc-mapper.skill 和 skill-explainer.skill，确认格式正确。description 中包含了中英文触发短语。

### 阶段 5：文档撰写（5 轮）

每份文档由 AI 生成初稿后人工审查修改：
- **README.md**：AI 生成 9 段标准结构，人工补充了 Agent 能力展示、支持的模型对比表、自定义指南
- **AI_LOG.md**：AI 生成 5 阶段记录，人工补充了实际运行结果和 AI 误导案例
- **ATTRIBUTION.md**：AI 生成依赖库列表，人工补充了数据来源核实方法和代码借鉴声明
- **docs/usage.md**：AI 生成参数说明和 FAQ，人工补充了三平台安装说明和性能调优表
- **提交文档**：repo链接.md 包含详细的推送步骤和群内分享话术

### 阶段 6：调试验证（2 轮）

**第 1 轮 — 脚本运行验证**
- 运行 `python3 scripts/sias_map_agent.py --offline --locations 12`
- 结果：12/12 地点通过验证，地图生成成功，exit code 0
- AI 辅助：确认离线模式不依赖 Ollama，可以在任何环境运行

**第 2 轮 — 文件完整性检查**
- 对照 C5 检查清单逐项确认：
  - ✅ README.md 包含一句话说明、安装步骤、使用示例、项目结构
  - ✅ 有 LICENSE 文件（MIT）
  - ✅ 有 .gitignore
  - ✅ 有 AI_LOG.md
  - ✅ 有 ATTRIBUTION.md
  - ✅ 有真实使用示例（examples/sample_output.html）
  - ✅ 代码可运行（离线模式验证通过）

---

## 三、AI 生成内容核验记录

| AI 生成内容 | 核验方式 | 结果 |
|---|---|---|
| README 结构 | 对照 C5.pdf 模板 | ✅ 完整 |
| MIT LICENSE 文本 | 对照 MIT 标准文本 | ✅ 正确 |
| .gitignore 规则 | 逐条检查 | ✅ 合理 |
| NEOLAF 架构描述 | 对照 arXiv:2308.03990 | ✅ 准确 |
| Ollama API 用法 | 对照官方文档 | ✅ 正确 |
| 项目结构 | 对照 GitHub Python 项目标准 | ✅ 规范 |

---

## 四、AI 工作流

本次 C5 开发采用以下 AI 协作工作流：

1. **规范先行**：先让 AI 梳理 C5 的所有硬性要求和检查清单，确保不遗漏
2. **结构设计**：AI 建议 repo 结构，人工根据项目实际情况调整
3. **代码复用**：基于 C4D 已验证的代码，不重复造轮子
4. **文档生成→审查→补充**：AI 生成初稿，人工审查后补充实际测试结果和具体操作细节
5. **最终验证**：对照检查清单逐项确认，运行代码验证可执行性
