#!/usr/bin/env python3
"""
C4D Local LLM Agent - SIAS University Interactive Map Generator
=================================================================
使用本地 Gemma 4 模型（通过 Ollama API）驱动 Agent 生成地点数据，
并用 Folium 渲染交互式 HTML 地图。

用法:
    python sias_map_agent.py                          # 使用默认设置
    python sias_map_agent.py --model gemma4:e4b      # 指定模型
    python sias_map_agent.py --locations 10           # 生成10个地点
    python sias_map_agent.py --output my_map.html     # 指定输出文件名
    python sias_map_agent.py --offline                 # 离线模式（使用内置数据，不调用LLM）

依赖:
    pip install requests folium
"""

import argparse
import json
import sys
import os
from datetime import datetime

# ============================================================================
# 内置 SIAS 大学地点数据（离线模式 / LLM 输出验证参考）
# 数据来源：高德地图 POI + 西亚斯学院官网 + 公开旅游信息
# ============================================================================
BUILTIN_LOCATIONS = [
    {
        "name": "SIAS University Main Gate",
        "name_zh": "郑州西亚斯学院正门",
        "latitude": 34.401422,
        "longitude": 113.765004,
        "description": "西亚斯学院主入口，位于新郑市人民路东段168号，是学校的标志性入口。",
        "category": "校门"
    },
    {
        "name": "Moscow Red Square",
        "name_zh": "莫斯科红场",
        "latitude": 34.400800,
        "longitude": 113.766200,
        "description": "校园内标志性欧式建筑群，仿照莫斯科红场风格建造，是西亚斯最具辨识度的地标之一。",
        "category": "地标建筑"
    },
    {
        "name": "SIAS Library",
        "name_zh": "西亚斯图书馆",
        "latitude": 34.399500,
        "longitude": 113.767000,
        "description": "学校图书馆，内设咖啡厅，是学生学习和休闲的重要场所。",
        "category": "教学设施"
    },
    {
        "name": "Comprehensive Gymnasium",
        "name_zh": "综合体育馆",
        "latitude": 34.399654,
        "longitude": 113.766787,
        "description": "西亚斯综合体育馆，高德评分4.5，营业时间09:30-22:00，承办各类体育赛事和校园活动。",
        "category": "体育设施"
    },
    {
        "name": "Europe Street",
        "name_zh": "欧洲街",
        "latitude": 34.400200,
        "longitude": 113.767500,
        "description": "校园内商业步行街，汇聚必胜客、星巴克、泡泡玛特、霸王茶姬、DQ、小米之家等品牌，被称为'河南最贵气的学校'的核心区域。",
        "category": "商业街"
    },
    {
        "name": "London Street",
        "name_zh": "伦敦街",
        "latitude": 34.398800,
        "longitude": 113.768000,
        "description": "以欧式建筑风格著称的校园街道，拥有罗马柱等欧式元素，拍照出片率极高。",
        "category": "地标建筑"
    },
    {
        "name": "French Garden",
        "name_zh": "法国园",
        "latitude": 34.398200,
        "longitude": 113.766500,
        "description": "法式风格园林，内设咖啡厅，环境优雅，是学生休闲社交的热门地点。",
        "category": "园林景观"
    },
    {
        "name": "Spain Square",
        "name_zh": "西班牙广场",
        "latitude": 34.399000,
        "longitude": 113.765500,
        "description": "西班牙风格广场，旁设西班牙餐厅，是校园内约会聚餐的首选之地。",
        "category": "广场"
    },
    {
        "name": "Fisherman's Pavilion",
        "name_zh": "渔夫子亭",
        "latitude": 34.402500,
        "longitude": 113.768500,
        "description": "纪念春秋时期救助伍子胥的渔夫父子而建，位于校园东北方向高地，兼具历史传说与校园文化意义。",
        "category": "文化地标"
    },
    {
        "name": "Kansas International School",
        "name_zh": "堪萨斯国际学院",
        "latitude": 34.395225,
        "longitude": 113.769275,
        "description": "西亚斯学院与美国堪萨斯州富特海斯州立大学合作办学机构，位于校园南部。",
        "category": "教学设施"
    },
    {
        "name": "Zhengfengyuan Scenic Area",
        "name_zh": "郑风苑景区",
        "latitude": 34.403000,
        "longitude": 113.762000,
        "description": "校园南门附近的开放式景区，含水上世界、疯狂老鼠、海豚戏水等游乐设施，距校园仅约190-550米。",
        "category": "周边景点"
    },
    {
        "name": "Xuanyuan Lake Park",
        "name_zh": "轩辕湖公园",
        "latitude": 34.395000,
        "longitude": 113.775000,
        "description": "新郑市著名湿地公园，环境优美，是学生周末休闲散步的好去处。",
        "category": "周边景点"
    }
]


# ============================================================================
# LLM Agent 核心逻辑
# ============================================================================

class LocalLLMAgent:
    """本地大模型 Agent，通过 Ollama API 调用 Gemma 4 生成地点数据。"""

    def __init__(self, model="gemma4:e4b", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.api_endpoint = f"{base_url}/v1/chat/completions"

    def check_connection(self):
        """检查 Ollama 服务是否可用。"""
        import requests
        try:
            resp = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if resp.status_code == 200:
                models = [m["name"] for m in resp.json().get("models", [])]
                return True, models
            return False, []
        except Exception as e:
            return False, str(e)

    def generate_locations(self, count=8, location_name="SIAS University"):
        """
        调用本地 Gemma 4 生成地点数据。
        使用结构化 JSON 输出（Agent 能力展示）。
        """
        import requests

        system_prompt = """You are a geography and local knowledge assistant.
You ALWAYS respond with valid JSON only — no markdown, no explanation, no code blocks.
Output a JSON array of location objects. Each object MUST have exactly these fields:
- name (English name)
- name_zh (Chinese name)
- latitude (float, between 34.38 and 34.42)
- longitude (float, between 113.74 and 113.79)
- description (brief description in Chinese, 1-2 sentences)
- category (one of: 校门, 地标建筑, 教学设施, 体育设施, 商业街, 园林景观, 广场, 文化地标, 周边景点, 餐厅)
Ensure coordinates are realistic for the Xinzheng area near SIAS University."""

        user_prompt = f"""List {count} notable locations at or near {location_name} (西亚斯学院) 
in Xinzheng, Henan, China. Include campus landmarks, buildings, commercial areas, 
and nearby attractions. Return JSON array only."""

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2048
        }

        print(f"[Agent] 正在调用本地模型 {self.model} 生成地点数据...")
        print(f"[Agent] API: {self.api_endpoint}")

        try:
            resp = requests.post(self.api_endpoint, json=payload, timeout=120)
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"]

            # 清理可能的 markdown 代码块标记
            content = content.strip()
            if content.startswith("```"):
                content = content.split("\n", 1)[1] if "\n" in content else content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

            locations = json.loads(content)
            print(f"[Agent] 成功生成 {len(locations)} 个地点")
            return locations

        except requests.exceptions.ConnectionError:
            print("[Agent] 错误：无法连接 Ollama 服务。请确保 Ollama 已启动。")
            print("[Agent] 启动命令：ollama serve")
            return None
        except json.JSONDecodeError as e:
            print(f"[Agent] 错误：模型输出不是有效 JSON。{e}")
            print(f"[Agent] 原始输出前200字符：{content[:200] if 'content' in dir() else 'N/A'}")
            return None
        except Exception as e:
            print(f"[Agent] 错误：{e}")
            return None

    def function_call_demo(self):
        """
        演示函数调用（function calling）能力。
        定义一个工具函数，让模型决定何时调用。
        """
        import requests

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_campus_info",
                    "description": "获取西亚斯学院校园信息，包括地址、电话、官网等",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "info_type": {
                                "type": "string",
                                "enum": ["address", "phone", "website", "all"],
                                "description": "需要获取的信息类型"
                            }
                        },
                        "required": ["info_type"]
                    }
                }
            }
        ]

        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": "西亚斯学院的地址是什么？请调用工具获取。"}
            ],
            "tools": tools,
            "tool_choice": "auto"
        }

        print("[Agent] 演示函数调用能力...")
        try:
            resp = requests.post(self.api_endpoint, json=payload, timeout=60)
            result = resp.json()
            message = result["choices"][0]["message"]
            if "tool_calls" in message:
                print(f"[Agent] 模型决定调用工具：{message['tool_calls'][0]['function']['name']}")
                print(f"[Agent] 调用参数：{message['tool_calls'][0]['function']['arguments']}")
            else:
                print(f"[Agent] 模型直接回答：{message.get('content', 'N/A')[:100]}")
            return result
        except Exception as e:
            print(f"[Agent] 函数调用演示失败：{e}")
            return None


# ============================================================================
# 地图生成器
# ============================================================================

def generate_map(locations, output_file="sias_map.html", center_lat=34.401422, center_lon=113.765004):
    """用 Folium 生成交互式 HTML 地图。"""
    try:
        import folium
    except ImportError:
        print("错误：未安装 folium。请运行：pip install folium")
        return False

    # 创建地图，中心定位在 SIAS 正门
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=15,
        tiles="OpenStreetMap",
        width="100%",
        height="100%"
    )

    # 分类颜色
    category_colors = {
        "校门": "red",
        "地标建筑": "blue",
        "教学设施": "green",
        "体育设施": "orange",
        "商业街": "purple",
        "园林景观": "darkgreen",
        "广场": "cadetblue",
        "文化地标": "darkred",
        "周边景点": "lightblue",
        "餐厅": "pink"
    }

    # 添加标记点
    for loc in locations:
        color = category_colors.get(loc.get("category", ""), "blue")
        popup_html = f"""
        <div style="font-family: sans-serif; min-width: 200px;">
            <h4 style="margin: 0 0 8px 0; color: #333;">{loc.get('name_zh', loc.get('name', ''))}</h4>
            <p style="margin: 0 0 6px 0; font-size: 13px; color: #666;">
                <strong>英文名：</strong>{loc.get('name', '')}<br>
                <strong>类别：</strong>{loc.get('category', '未分类')}<br>
                <strong>坐标：</strong>{loc.get('latitude', 0):.6f}, {loc.get('longitude', 0):.6f}
            </p>
            <p style="margin: 0; font-size: 13px; color: #444; line-height: 1.5;">
                {loc.get('description', '')}
            </p>
        </div>
        """

        folium.Marker(
            location=[loc.get("latitude", center_lat), loc.get("longitude", center_lon)],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=loc.get("name_zh", loc.get("name", "")),
            icon=folium.Icon(color=color, icon="info-sign", prefix="glyphicon")
        ).add_to(m)

    # 添加中心点标记（SIAS 正门）
    folium.Marker(
        location=[center_lat, center_lon],
        popup=folium.Popup("<strong>郑州西亚斯学院正门</strong><br>人民路东段168号", max_width=200),
        tooltip="SIAS University 中心",
        icon=folium.Icon(color="red", icon="star", prefix="glyphicon")
    ).add_to(m)

    # 添加图例
    legend_html = """
    <div style="position: fixed; bottom: 20px; left: 20px; z-index: 1000; 
                background: white; padding: 12px 16px; border-radius: 8px; 
                box-shadow: 0 2px 10px rgba(0,0,0,0.2); font-family: sans-serif; font-size: 12px;">
        <strong style="display: block; margin-bottom: 8px;">📍 地点分类图例</strong>
    """
    for cat, color in category_colors.items():
        legend_html += f'<div style="margin: 3px 0;"><span style="display:inline-block;width:12px;height:12px;background:{color};border-radius:50%;margin-right:6px;"></span>{cat}</div>'
    legend_html += "</div>"

    m.get_root().html.add_child(folium.Element(legend_html))

    # 添加标题
    title_html = """
    <div style="position: fixed; top: 20px; left: 50%; transform: translateX(-50%); 
                z-index: 1000; background: rgba(255,255,255,0.95); padding: 10px 24px; 
                border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.15); 
                font-family: sans-serif; text-align: center;">
        <h2 style="margin: 0; font-size: 18px; color: #333;">🏛️ 郑州西亚斯学院交互式地图</h2>
        <p style="margin: 4px 0 0 0; font-size: 12px; color: #666;">
            由本地 Gemma 4 Agent 生成 | 点击标记查看详情 | 可缩放拖拽
        </p>
    </div>
    """
    m.get_root().html.add_child(folium.Element(title_html))

    # 保存
    m.save(output_file)
    print(f"[Map] 交互式地图已生成：{output_file}")
    print(f"[Map] 共标记 {len(locations)} 个地点")
    return True


# ============================================================================
# 数据验证器
# ============================================================================

def validate_locations(locations):
    """验证 LLM 生成的地点数据质量。"""
    print("\n[Validator] 地点数据质量验证：")
    print("-" * 50)

    issues = []
    valid_count = 0

    for i, loc in enumerate(locations):
        loc_issues = []

        # 检查必填字段
        required_fields = ["name", "name_zh", "latitude", "longitude", "description"]
        for field in required_fields:
            if field not in loc:
                loc_issues.append(f"缺少字段: {field}")

        # 检查坐标范围（新郑市附近）
        if "latitude" in loc:
            lat = loc["latitude"]
            if not (34.30 <= lat <= 34.50):
                loc_issues.append(f"纬度异常: {lat} (预期 34.30-34.50)")

        if "longitude" in loc:
            lon = loc["longitude"]
            if not (113.65 <= lon <= 113.85):
                loc_issues.append(f"经度异常: {lon} (预期 113.65-113.85)")

        if loc_issues:
            print(f"  ❌ 地点 {i+1} ({loc.get('name_zh', loc.get('name', '未知'))}): {'; '.join(loc_issues)}")
            issues.extend(loc_issues)
        else:
            print(f"  ✅ 地点 {i+1}: {loc.get('name_zh', '')} ({loc.get('latitude', 0):.4f}, {loc.get('longitude', 0):.4f})")
            valid_count += 1

    print("-" * 50)
    print(f"[Validator] 验证完成：{valid_count}/{len(locations)} 个地点通过验证")
    if issues:
        print(f"[Validator] 发现 {len(issues)} 个问题")
    else:
        print("[Validator] 所有地点数据质量良好")

    return valid_count, issues


# ============================================================================
# 主函数
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="C4D 本地大模型 Agent - SIAS 大学交互式地图生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python sias_map_agent.py                          # 默认模式（调用本地LLM）
  python sias_map_agent.py --offline                # 离线模式（使用内置数据）
  python sias_map_agent.py --model gemma4:e2b      # 使用 E2B 模型
  python sias_map_agent.py --locations 12 --output campus.html
        """
    )
    parser.add_argument("--model", default="gemma4:e4b", help="Ollama 模型名称 (默认: gemma4:e4b)")
    parser.add_argument("--base-url", default="http://localhost:11434", help="Ollama API 地址")
    parser.add_argument("--locations", type=int, default=8, help="生成地点数量 (默认: 8)")
    parser.add_argument("--output", default="Student_C4D_map.html", help="输出 HTML 文件名")
    parser.add_argument("--offline", action="store_true", help="离线模式：使用内置数据，不调用 LLM")
    parser.add_argument("--skip-validation", action="store_true", help="跳过数据验证")
    parser.add_argument("--demo-function-call", action="store_true", help="演示函数调用能力")

    args = parser.parse_args()

    print("=" * 60)
    print("  C4D 本地大模型 Agent - SIAS 大学交互式地图生成器")
    print("=" * 60)
    print(f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  模式: {'离线（内置数据）' if args.offline else '在线（本地LLM）'}")
    if not args.offline:
        print(f"  模型: {args.model}")
        print(f"  API:  {args.base_url}")
    print("=" * 60)
    print()

    locations = None

    if args.offline:
        print("[Mode] 使用内置 SIAS 大学地点数据（离线模式）")
        locations = BUILTIN_LOCATIONS[:args.locations]
    else:
        # 在线模式：调用本地 LLM
        agent = LocalLLMAgent(model=args.model, base_url=args.base_url)

        # 检查连接
        connected, info = agent.check_connection()
        if not connected:
            print(f"[Error] 无法连接 Ollama 服务: {info}")
            print("[Hint]  请先启动 Ollama：ollama serve")
            print("[Hint]  或使用 --offline 参数运行离线模式")
            sys.exit(1)

        print(f"[OK] Ollama 服务已连接，可用模型: {info}")

        # 演示函数调用
        if args.demo_function_call:
            agent.function_call_demo()
            print()

        # 生成地点数据
        locations = agent.generate_locations(count=args.locations)
        if locations is None:
            print("[Error] LLM 生成失败，切换到内置数据...")
            locations = BUILTIN_LOCATIONS[:args.locations]

    # 验证数据
    if not args.skip_validation and locations:
        valid_count, issues = validate_locations(locations)

    # 生成地图
    print()
    success = generate_map(locations, output_file=args.output)

    if success:
        print()
        print("=" * 60)
        print("  ✅ 任务完成！")
        print(f"  📍 地图文件: {args.output}")
        print(f"  📊 标记地点: {len(locations)} 个")
        print("  🖱️  在浏览器中打开 HTML 文件即可查看交互式地图")
        print("=" * 60)
    else:
        print("\n❌ 地图生成失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
