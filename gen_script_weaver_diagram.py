#!/usr/bin/env python3
"""Generate script-weaver Excalidraw diagram."""
import json, random, string, os

def rid(): return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

elements = []

# ── Helpers ──
def text(x, y, w, h, txt, fs=14, align="left", color="#1e1e1e", bold=False, containerId=None):
    el = {"type":"text","version":1,"id":rid(),"x":x,"y":y,"width":w,"height":h,
          "text":txt,"fontSize":fs,"fontFamily":1,"textAlign":align,"verticalAlign":"middle",
          "containerId":containerId,"originalText":txt,"autoResize":True,"lineHeight":1.25}
    elements.append(el); return el

def rect(x, y, w, h, stroke, bg, boundTexts=None, roundness=2):
    el = {"type":"rectangle","version":1,"id":rid(),"x":x,"y":y,"width":w,"height":h,
          "strokeColor":stroke,"backgroundColor":bg,"fillStyle":"solid","strokeWidth":2,
          "strokeStyle":"solid","roughness":2,"opacity":100,"roundness":{"type":roundness}}
    if boundTexts:
        el["boundElements"] = [{"id":t,"type":"text"} for t in boundTexts]
    elements.append(el); return el

def arrow(x, y, pts, sw=1.5, color="#495057"):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    w = max(xs)-min(xs); h = max(ys)-min(ys)
    el = {"type":"arrow","version":1,"id":rid(),"x":x,"y":y,"width":max(w,1),"height":max(h,1),
          "strokeColor":color,"backgroundColor":"transparent","fillStyle":"solid",
          "strokeWidth":sw,"strokeStyle":"solid","roughness":2,"opacity":100,
          "points":pts,"startArrowhead":None,"endArrowhead":"arrow"}
    elements.append(el); return el

def box(x, y, w, h, stroke, bg, txt, fs=13, tc="#1e1e1e", align="center"):
    """Create a rect with centered text bound to it."""
    tid = rid()
    # Text slightly inset
    text(x+6, y+(h-fs-2)/2, w-12, fs+4, txt, fs, align, tc, containerId=tid)
    rect(x, y, w, h, stroke, bg, [tid])

def group_frame(x, y, w, h, stroke, bg, title, title_fs=14):
    """Create a group frame with title as first text line inside."""
    rect(x, y, w, h, stroke, bg, roundness=2)
    text(x+12, y+10, w-24, title_fs+4, title, title_fs, "left", stroke)

def hline(x, y, w, color="#dee2e6"):
    arrow(x, y, [[0,0],[w,0]], sw=0.8, color=color)

# ── Color Scheme ──
C_CORE   = ("#f08c00","#ffec99")  # orange - core principle
C_FENG   = ("#1971c2","#d0ebff")  # blue - xiaofeng
C_AN     = ("#9c36b5","#e599f7")  # purple - an xiansheng
C_MIX    = ("#2f9e44","#d3f9d8")  # green - mixed
C_CASE   = ("#e8590c","#ffe8cc")  # red-orange - case study
C_TOOL   = ("#868e96","#f8f9fa")  # gray - toolboxes

# ── Layout Constants ──
PAGE_LEFT = 40
PAGE_W = 880
CENTER = 480
GAP = 20
PAD = 16
COL_W = 420
LEFT_X = 40
RIGHT_X = 500

curY = 30

# ═══════════════════════════════════════
# SECTION 1: 核心原理
# ═══════════════════════════════════════
box(PAGE_LEFT, curY, PAGE_W, 44, *C_CORE, "脚本织造师 · 核心原理", fs=20, tc=C_CORE[0])
curY += 44 + 10

box(PAGE_LEFT, curY, PAGE_W, 48, "#f08c00", "#fff4e6",
    "完播率 = 信息类型切换频率 × 认知刷新强度", fs=16)
curY += 48 + 10

text(PAGE_LEFT+10, curY, PAGE_W-20, 22,
     "人脑对同类型刺激 15-30s 习惯化 → 必须持续切换信息类型，否则观众划走",
     fs=14, color="#868e96", align="center")
curY += 22 + GAP

# ═══════════════════════════════════════
# SECTION 2: 两种体系对比
# ═══════════════════════════════════════
text(PAGE_LEFT, curY, 200, 20, "两种口播体系", fs=15, color="#868e96")
curY += 22 + 6

LEFT_H = 410
RIGHT_H = 410

# -- Left: 小冯型 --
fx, fy = LEFT_X, curY
group_frame(fx, fy, COL_W, LEFT_H, *C_FENG, "小冯型 · 经验论证", title_fs=16)

iy = fy + 44  # below header
items_left = [
    "回答： 「XX 怎么做？」",
    "选题： 方法论 / 操作指南 / 项目拆解",
    "结构： A 阶梯递进  |  B 三步操作",
    "切换频率： 中频 30-45s / 段",
    "过渡方式： 有承接词缓冲（比如说/所以）",
]
for item in items_left:
    text(fx+16, iy, COL_W-32, 20, item, fs=12, color="#1e1e1e")
    iy += 22

iy += 8
hline(fx+16, iy, COL_W-32, "#1971c2")
iy += 10
text(fx+16, iy, COL_W-32, 18, "信息要素链", fs=12, color="#1971c2", bold=True)
iy += 22

# Pipeline boxes - left
pipe_w = 68; pipe_h = 24; pipe_gap = 8
pipe_left = [
    ("知识晶体\n≤12字", C_FENG),
    ("反常识\n观点", C_FENG),
    ("故事\n验证", C_FENG),
    ("金句\n收尾", C_FENG),
    ("推力\n过渡", C_FENG),
]
px = fx + 16
for i, (label, colors) in enumerate(pipe_left):
    box(px, iy, pipe_w, pipe_h+16, *colors, label, fs=9, tc=colors[0])
    if i < len(pipe_left)-1:
        ax = px + pipe_w
        arrow(ax, iy+pipe_h/2+8, [[0,0],[pipe_gap,0]], sw=1.0, color=colors[0])
    px += pipe_w + pipe_gap

iy += pipe_h + 16 + 12
text(fx+16, iy, COL_W-32, 44,
     "特点：框架显性、编号分段\n每 1.5-2 分钟一次框架回扣\n故事 30-40s/个，亲身经历必用",
     fs=11, color="#495057")
iy += 50

# -- Right: 安先生型 --
ax, ay = RIGHT_X, curY
group_frame(ax, ay, COL_W, RIGHT_H, *C_AN, "安先生型 · 认知颠覆", title_fs=16)

iy2 = ay + 44
items_right = [
    "回答： 「XX 到底是什么？」",
    "选题： 概念重定义 / 认知颠覆",
    "结构： C 单线概念展开",
    "切换频率： 高频 4-5s / 次",
    "过渡方式： 无过渡词，直接跳",
]
for item in items_right:
    text(ax+16, iy2, COL_W-32, 20, item, fs=12, color="#1e1e1e")
    iy2 += 22

iy2 += 8
hline(ax+16, iy2, COL_W-32, "#9c36b5")
iy2 += 10
text(ax+16, iy2, COL_W-32, 18, "信息要素链", fs=12, color="#9c36b5", bold=True)
iy2 += 22

pipe_right = [
    ("概念\n对撞", C_AN),
    ("硬细节\n锚定", C_AN),
    ("尺度\n跳跃", C_AN),
    ("无信号\n直接跳", C_AN),
    ("故意不\n给答案", C_AN),
]
px2 = ax + 16
for i, (label, colors) in enumerate(pipe_right):
    box(px2, iy2, pipe_w, pipe_h+16, *colors, label, fs=9, tc=colors[0])
    if i < len(pipe_right)-1:
        arrow(px2+pipe_w, iy2+pipe_h/2+8, [[0,0],[pipe_gap,0]], sw=1.0, color=colors[0])
    px2 += pipe_w + pipe_gap

iy2 += pipe_h + 16 + 12
text(ax+16, iy2, COL_W-32, 44,
     "特点：无编号分段、概念自然展开\n硬细节锚定 3-5s/个 替代故事\n结尾故意不给答案，引爆评论区",
     fs=11, color="#495057")

curY += LEFT_H + GAP

# ═══════════════════════════════════════
# SECTION 3: 混合型（汇聚节点）
# ═══════════════════════════════════════
# Arrows from both columns converging to center
conv_y = curY
arrow(LEFT_X+COL_W/2, curY-20, [[0,0],[0,GAP+20]], sw=1.2, color="#2f9e44")
arrow(RIGHT_X+COL_W/2, curY-20, [[0,0],[0,GAP+20]], sw=1.2, color="#2f9e44")

box(LEFT_X+60, curY, PAGE_W-200, 40, *C_MIX,
    "混合型 = 小冯骨架 + 安先生血肉 → 方法论结构 + 认知颠覆技法", fs=14, tc=C_MIX[0])
curY += 40 + GAP + 4

# ═══════════════════════════════════════
# SECTION 4: 实战案例 — 三棱镜定位法
# ═══════════════════════════════════════
case_h = 200
cx, cy = PAGE_LEFT, curY
group_frame(cx, cy, PAGE_W, case_h, *C_CASE, "实战案例：三棱镜定位法口播稿", title_fs=16)

ciy = cy + 44

# Three big step boxes
step_w = 130; step_h = 70; step_gap = 60
total_step_w = 3*step_w + 2*step_gap
step_start_x = cx + (PAGE_W - total_step_w)/2

steps = [
    ("做", "三个追问\n时间花哪了\n别人找你帮什么\n你知道什么\n同龄人不知道"),
    ("看", "认知翻转\n「这不都是\n很普通的事吗」\n概念对撞\n普通 vs 稀缺"),
    ("配", "匹配 AI 形式\n能讲明白→口播\n带情绪→短剧\n擅拆步骤→教程"),
]
for i, (title, desc) in enumerate(steps):
    sx = step_start_x + i*(step_w + step_gap)
    box(sx, ciy, step_w, step_h, *C_CASE, title, fs=22, tc=C_CASE[0])
    text(sx+4, ciy+30, step_w-8, step_h-34, desc, fs=9, color="#495057", align="center")
    if i < 2:
        arrow(sx+step_w, ciy+step_h/2, [[0,0],[step_gap,0]], sw=1.5, color=C_CASE[0])

ciy += step_h + 14

# Switching path summary
text(cx+16, ciy, PAGE_W-32, 16, "信息切换路径", fs=12, color=C_CASE[0], bold=True)
ciy += 18
path_text = (
    "段1: 反常识 → 三追问 → 金句 → 推力过渡  |  "
    "段2: 概念对撞 → 无信号跳 → 硬细节「孩子哭了怎么哄」 → 反问 → 翻转  |  "
    "段3: 匹配逻辑 → 案例讲透 → 金句闭环"
)
text(cx+16, ciy, PAGE_W-32, 36, path_text, fs=11, color="#495057")

curY += case_h + GAP

# ═══════════════════════════════════════
# SECTION 5: 素材工具箱（双列）
# ═══════════════════════════════════════
tool_h = 340
tx, ty = PAGE_LEFT, curY

# Left: 9 故事类型
group_frame(tx, ty, COL_W, tool_h, *C_TOOL, "9 种故事类型（按频率排序）", title_fs=14)

story_types = [
    "1. 亲身经历 — 每条稿子必用，最自然的信任",
    "2. 生活比喻 — 每个抽象概念配一个",
    "3. 行业现象 — 观察到的行业趋势/现象",
    "4. 假设性场景 — 「假设你...」让观众代入",
    "5. 社会新闻/公众人物 — 名人案例/新闻",
    "6. 数据/调研结果 — 具体数字锚定观点",
    "7. 历史典故 — 需主题本身有历史维度",
    "8. 亲属案例 — 有真实素材才用，禁止编造",
    "9. 真实用户案例 — 需真实用户，禁止编造",
]
tiy = ty + 44
for s in story_types:
    text(tx+16, tiy, COL_W-32, 18, s, fs=10.5, color="#1e1e1e")
    tiy += 20

# Right: 13 嵌入技法
rx, ry = RIGHT_X, curY
group_frame(rx, ry, COL_W, tool_h, *C_TOOL, "13 种嵌入技法", title_fs=14)

tech_types = [
    ("每条必用", [
        "· 「比如说」嵌入 — 抽象→具象",
        "· 金句段尾 — 故事→总结",
        "· 框架回扣 — 段落→主线",
    ]),
    ("按需选用", [
        "· 个人记忆链 · 代理人总结 · 正反翻转",
        "· 历史纵深 · 比喻嵌入 · 痛点反问",
        "· 首尾闭环 · 自问自答 · 误解除法",
        "· 认知反差 · 选择题参与",
    ]),
]
tiy2 = ry + 44
for section_title, items in tech_types:
    text(rx+16, tiy2, COL_W-32, 18, section_title, fs=11, color="#868e96", bold=True)
    tiy2 += 18
    for item in items:
        text(rx+16, tiy2, COL_W-32, 17, item, fs=10, color="#1e1e1e")
        tiy2 += 17
    tiy2 += 4

curY += tool_h + GAP

# ═══════════════════════════════════════
# SECTION 6: Footer
# ═══════════════════════════════════════
text(PAGE_LEFT, curY, PAGE_W, 18,
     "ah-script-weaver  |  脚本织造师  |  小冯 4 篇交叉验证 + 安先生 1 篇（待验证）",
     fs=11, color="#adb5bd", align="center")

# ── AppState ──
appState = {
    "viewBackgroundColor": "#ffffff",
    "gridSize": None,
    "theme": "light",
}

# ── Write file ──
output = {
    "type": "excalidraw",
    "version": 2,
    "source": "https://excalidraw.com",
    "elements": elements,
    "appState": appState,
    "files": {}
}

outdir = os.environ.get("SCRIPT_WEAVER_OUTDIR", ".")
path = os.path.join(outdir, "07-脚本织造师方法手绘图.excalidraw")
with open(path, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Written {len(elements)} elements to {path}")
print(f"Estimated total height: {curY + 30}px")
