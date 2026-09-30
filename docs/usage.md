# 详细使用文档

## 目录

1. [命令行参数详解](#命令行参数详解)
2. [离线模式使用](#离线模式使用)
3. [函数调用演示](#函数调用演示)
4. [常见问题 FAQ](#常见问题-faq)
5. [性能调优](#性能调优)
6. [自定义开发](#自定义开发)

---

## 命令行参数详解

```bash
python scripts/sias_map_agent.py [OPTIONS]
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--model` | string | `gemma4:e4b` | Ollama 模型名称。可选：gemma4:e2b, gemma4:e4b, gemma4:26b, gemma4:31b |
| `--base-url` | string | `http://localhost:11434` | Ollama API 地址。如果 Ollama 运行在其他端口或远程服务器，修改此参数 |
| `--locations` | int | `8` | 生成地点数量。建议 5-20 个，过多可能导致模型输出截断 |
| `--output` | string | `Student_C4D_map.html` | 输出 HTML 文件名 |
| `--offline` | flag | False | 离线模式：使用内置数据，不调用 LLM |
| `--skip-validation` | flag | False | 跳过数据验证步骤 |
| `--demo-function-call` | flag | False | 演示函数调用能力 |

### 示例

```bash
# 使用 E2B 模型生成 5 个地点
python scripts/sias_map_agent.py --model gemma4:e2b --locations 5

# 输出到指定文件
python scripts/sias_map_agent.py --output ~/Desktop/my_map.html

# 连接远程 Ollama 服务器
python scripts/sias_map_agent.py --base-url http://192.168.1.100:11434

# 跳过验证（不推荐）
python scripts/sias_map_agent.py --skip-validation
```

---

## 离线模式使用

离线模式不调用本地 LLM，直接使用内置的 SIAS 大学 12 个地点数据生成地图。

### 适用场景

- 还没安装 Ollama 或下载模型
- 想快速查看地图效果
- 网络不稳定，无法保证 Ollama 服务运行
- 只需要 SIAS 大学的地图，不需要其他地点

### 使用方法

```bash
python scripts/sias_map_agent.py --offline
```

### 离线模式输出

```
============================================================
  C4D 本地大模型 Agent - SIAS 大学交互式地图生成器
============================================================
  时间: 2026-09-29 10:22:54
  模式: 离线（内置数据）
============================================================

[Mode] 使用内置 SIAS 大学地点数据（离线模式）

[Validator] 地点数据质量验证：
--------------------------------------------------
  ✅ 地点 1: 郑州西亚斯学院正门 (34.4014, 113.7650)
  ✅ 地点 2: 莫斯科红场 (34.4008, 113.7662)
  ...
  ✅ 地点 12: 轩辕湖公园 (34.3950, 113.7750)
--------------------------------------------------
[Validator] 验证完成：12/12 个地点通过验证

[Map] 交互式地图已生成：Student_C4D_map.html
[Map] 共标记 12 个地点
```

---

## 函数调用演示

Gemma 4 支持原生 function calling。本项目提供了演示功能。

### 使用方法

```bash
python scripts/sias_map_agent.py --demo-function-call
```

### 工作原理

1. 定义 `get_campus_info` 工具函数，参数为 `info_type`（address/phone/website/all）
2. 通过 Ollama API 发送用户问题："西亚斯学院的地址是什么？请调用工具获取。"
3. 模型决定是否调用工具，并返回调用参数
4. 系统打印模型的决策结果

### 预期输出

```
[Agent] 演示函数调用能力...
[Agent] 模型决定调用工具：get_campus_info
[Agent] 调用参数：{"info_type": "address"}
```

> 注意：函数调用功能需要 Gemma 4 模型支持。如果模型不支持 function calling，可能会直接回答而不调用工具。

---

## 常见问题 FAQ

### Q1：运行时提示"无法连接 Ollama 服务"

**原因**：Ollama 没有启动。

**解决**：
- Windows：检查任务栏右下角有没有羊驼图标，没有的话从开始菜单打开 Ollama
- Mac：从启动台打开 Ollama
- Linux：终端输入 `ollama serve`，保持窗口开着

然后重新运行脚本，或使用 `--offline` 离线模式。

### Q2：提示"model 'gemma4:e4b' not found"

**原因**：模型还没下载，或模型名不对。

**解决**：
1. 输入 `ollama list` 查看已安装的模型
2. 如果没有 gemma4，输入 `ollama pull gemma4:e4b` 下载
3. 如果模型名不同，运行时指定：`python scripts/sias_map_agent.py --model gemma4:26b`

### Q3：模型下载太慢

**解决**：
- 换更小的模型 `gemma4:e2b`（下载快，占用小）
- 使用手机热点试试
- 搜索"Ollama 国内镜像"找加速方法

### Q4：生成的地图打开是空白的

**原因**：地图底图（OpenStreetMap）需要联网加载。

**解决**：
- 确保电脑联网
- 等几秒钟，底图加载需要时间
- 换个浏览器（Chrome/Edge/Firefox）

### Q5：LLM 生成的地点坐标不对

**原因**：大模型可能产生"坐标幻觉"。

**解决**：
- 脚本内置了数据验证器，会标记异常坐标
- 可以用 `--offline` 模式使用经过人工核实的内置数据
- 生成后手动调整 HTML 中的坐标

### Q6：怎么生成其他地点的地图？

修改 `scripts/sias_map_agent.py` 中的两处：
1. `generate_locations()` 中的 `user_prompt`：把 "SIAS University" 改成目标地点
2. `generate_map()` 中的 `center_lat` 和 `center_lon`：改成目标地点的坐标

### Q7：怎么打包为 .skill 文件？

```bash
cd C5_GitHub_Repo
tar -czf ../local-llm-map-agent.skill .
```

然后在 Claude 中安装使用。

---

## 性能调优

### 提升生成速度

| 方法 | 效果 | 说明 |
|------|------|------|
| 使用更小的模型 | 显著 | E2B 比 E4B 快约 30-50% |
| 减少地点数量 | 线性 | `--locations 5` 比 `--locations 12` 快约一倍 |
| 使用 GPU | 显著 | 有 NVIDIA GPU 的话 Ollama 会自动使用 |
| 增加内存 | 中等 | 16GB 比 8GB 流畅，减少 swap |
| 使用 Q4 量化 | 显著 | Ollama 默认就是 Q4，质量/速度平衡好 |

### 提升输出质量

| 方法 | 效果 | 说明 |
|------|------|------|
| 使用更大的模型 | 显著 | 26B/31B 比 E4B 质量高 |
| 使用 Q8 量化 | 轻微 | 比 Q4 质量好，但慢一些 |
| 优化 System Prompt | 中等 | 修改 `generate_locations()` 中的 system_prompt，增加更详细的要求 |
| 降低 temperature | 轻微 | 在 payload 中设置 `"temperature": 0.3`，输出更稳定 |

### 查看推理速度

Ollama 运行时会显示 tok/s 速度。也可以用：
```bash
ollama ps
```
查看当前加载的模型和内存占用。

---

## 自定义开发

### 添加新的地点分类

编辑 `scripts/sias_map_agent.py` 中的 `category_colors`：

```python
category_colors = {
    "校门": "red",
    "地标建筑": "blue",
    "你的新分类": "pink",  # 添加这行
}
```

Folium 支持的颜色：red, blue, green, purple, orange, darkred, lightblue, cadetblue, darkgreen, pink, gray, black 等。

### 修改 System Prompt

编辑 `LocalLLMAgent.generate_locations()` 中的 `system_prompt`：

```python
system_prompt = """You are a geography assistant.
You ALWAYS respond with valid JSON only.
...（你的自定义要求）..."""
```

可以添加：
- 更严格的坐标范围限制
- 描述的字数要求
- 特定的分类列表
- 输出语言要求

### 添加新的验证规则

编辑 `validate_locations()` 函数，添加新的检查项：

```python
# 示例：检查描述长度
if len(loc.get("description", "")) < 10:
    loc_issues.append(f"描述过短: {loc.get('description', '')}")
```

### 切换地图底图

编辑 `generate_map()` 中的 `tiles` 参数：

```python
m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=15,
    tiles="CartoDB positron",  # 简洁白底风格
    # tiles="Stamen Terrain",  # 地形风格
    # tiles="OpenStreetMap",   # 默认
)
```
