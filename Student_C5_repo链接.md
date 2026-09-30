# C5 GitHub Repo 链接

> 仓库已创建并推送完成，链接如下。

---

## 项目信息

- **项目名称**：local-llm-map-agent
- **一句话描述**：输入地点名称和数量，输出包含分类标记的交互式 HTML 地图。全程使用本地大模型（Gemma 4 via Ollama），零 API 费用。
- **输入**：地点名称 + 生成数量（可选模型名称）
- **输出**：交互式 HTML 地图（可缩放、可点击标记、含分类图例）

---

## GitHub 仓库链接

```
https://github.com/Fu-yue-ccc/local-llm-map-agent
```

> ⬆️ 已替换为实际 GitHub 账号：**Fu-yue-ccc**

---

## 推送到 GitHub 的步骤

### 1. 创建 GitHub 仓库

1. 登录 github.com
2. 点击右上角 **+** → **New repository**
3. Repository name 填：`local-llm-map-agent`
4. 选择 **Public**（公开）
5. **不要**勾选 "Add a README file"（因为我们已经有了）
6. 点击 **Create repository**

### 2. 本地初始化并推送

```bash
# 进入 repo 文件夹
cd C5_GitHub_Repo

# 初始化 Git
git init
git add .
git commit -m "Initial commit: local-llm-map-agent with SIAS University demo"

# 关联远程仓库
git remote add origin https://github.com/Fu-yue-ccc/local-llm-map-agent.git
git branch -M main
git push -u origin main
```

### 3. 验证

- 浏览器打开 `https://github.com/Fu-yue-ccc/local-llm-map-agent`
- 确认 README 正常渲染
- 确认所有文件都已上传
- 截图保存（用于 C5 提交）

---

## 群内分享话术

> 这是我的 C5 GitHub repo：https://github.com/Fu-yue-ccc/local-llm-map-agent —— 输入地点名称就能生成交互式地图，全程本地大模型驱动，零 API 费用，欢迎 star、fork、提 Issue！
