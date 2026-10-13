#!/usr/bin/env python3
"""
函数知识图谱 v8 — 左→右水平布局，全面美化
根(左) → 11章(中列) → 子题(右)
对称分布，平滑连线，清晰层次
"""
from PIL import Image, ImageDraw, ImageFont
import os

# ══════════════════════════════════════════
# 数据
# ══════════════════════════════════════════
DATA = [
    ('函数的基本概念', ['判断函数关系','列不等式(组)求函数定义域','求复合函数的定义域',
        '运用待定系数法求函数解析式','运用配凑法求函数解析式','运用换元法求函数解析式',
        '构造方程组求函数解析式','运用赋值法求函数解析式','运用反函数法求函数值域',
        '运用分离常数法求函数值域','运用判别式法求函数值域','运用换元法求函数值域',
        '运用均值不等式求函数值域','已知函数定义域或值域求参数取值范围','分段函数分段看']),
    ('函数的单调性', ['利用函数图像判断绝对值函数的单调性','利用定义证明函数的单调性',
        '对勾函数的单调性','利用函数的单调性求函数的值域','复合函数单调性的判断',
        '已知含参函数的单调性求参数的取值范围','分段函数的单调性',
        '抽象函数的单调性','新定义——倍值区间']),
    ('函数的奇偶性', ['函数奇偶性的判断','分段函数奇偶性的判断','抽象函数的奇偶性',
        '已知一半求另一半','利用函数的奇偶性求参数值','利用函数的奇偶性求函数值',
        '利用函数的奇偶性求最值','函数单调性与奇偶性','函数奇偶性与对称性']),
    ('函数的周期性', ['函数周期性的定义及其应用','周期性与对称性',
        '综合应用函数性质解决抽象函数问题']),
    ('函数的最值', ['求二次函数在闭区间上的最值','利用基本不等式求函数的最值',
        '利用函数单调性求函数最值','利用对勾函数单调性求对勾函数最值',
        '利用分离常数法求形如f(x)=(cx+d)/(ax+b)的函数最值',
        '利用整式分离法求函数的最值','利用配凑法求函数的最值',
        '利用换元法求函数的最值','条件最值问题']),
    ('幂函数', ['幂函数的概念','幂函数的图像','幂函数的奇偶性',
        '幂函数的单调性','幂函数图像的应用']),
    ('指数函数', ['根式、指数式的求值','根式的化简','利用乘法公式化简指数式',
        '幂的证明问题','指数型函数的定义域','函数图像的识别',
        '根据函数图像判断参数取值范围','函数图像的应用',
        '函数单调性与奇偶性的判断与证明','复合函数单调性同增异减',
        '利用指数函数单调性比较大小','利用指数函数单调性解不等式',
        '换元法求指数型函数的值域','已知指数型函数的最值求参数的值',
        '指数函数与分段函数','构造函数','任意性与存在性问题']),
    ('对数函数', ['对数式的计算问题','换底公式的应用',
        '用已知对数表示未知对数问题','对数方程的求解',
        '对数式与指数式的关系转化','对数的应用',
        '求对数型函数的定义域','求对数型函数的值域',
        '求对数型函数值域为R的参数取值范围问题','对数型函数的单调性',
        '复合函数单调性的逆向问题','新定义——闭函数','对数型函数的最值',
        '利用对数函数单调性估算','解对数不等式','对数型函数的奇偶性',
        'f(x)=log(1+x)/(1-x)的图像与性质','函数图像的识别问题',
        '对数的大小比较','通过构造函数比较大小','利用中间值比较大小',
        '利用函数性质比较大小','数形结合比较大小','函数图像的应用',
        '几类函数模型的增长差异','对数函数与分段函数',
        '互为反函数的两函数图像的公共点问题','恒成立问题']),
    ('函数的零点', ['零点概念和零点存在定理','判断函数零点所在区间',
        '判断方程根所在区间','转化为两个图像的交点来处理函数零点问题',
        '已知零点个数或所在区间求参数的取值范围','二次函数的零点分布问题',
        '两函数图像交点转化为二次方程实根分布','判断分段函数的零点个数',
        '根据分段函数零点个数求参数的取值范围',
        '已知函数f(x)解析式求方程a[f(x)]²+f(x)+c=0的实根个数',
        '函数y=f(x)的零点问题','函数y=f(g(x))-a的零点问题',
        '运用导数解决函数零点问题']),
    ('函数的综合应用', ['开放题','劣构试题',
        '数学问题背景下运动变化过程中的函数关系','抽象函数','绝对值函数',
        '分段函数','新定义创新题——高等数学思想方法的渗透',
        '新定义创新题——高斯函数及其相近的几类函数',
        '新定义创新题——最值函数','最值嵌套问题',
        '新定义创新题——课本概念性质的拓展','有效回避分类讨论',
        '分离参数','变更主元','必要性策略','形的直观与数的分析',
        '换元法和消元法','函数最值与任意和存在性问题',
        '函数值域倍增(减)问题','通过构造函数求(最)值']),
    ('函数的实际应用', ['分析散点图推断函数模型','分析变化过程判断函数图像',
        '读取图像信息判断结论正误','应用二次函数模型解决实际问题',
        '应用分段函数模型解决实际问题','指数对数的运算在实际问题中的应用',
        '构造对勾函数模型解决最值问题',
        '构造指数函数对数函数模型解决增长率问题',
        '理解给定函数模型判断结论正误','数学建模']),
]

# ══════════════════════════════════════════
# 配色
# ══════════════════════════════════════════
BG = (11, 25, 41)
GRID = (18, 35, 55)
GOLD = (210, 175, 100)
GOLD_HI = (240, 215, 155)
SNOW = (238, 240, 245)
TEXT_DIM = (160, 178, 195)

# 11 章色 — 青蓝渐变
CH_COLORS = [
    (70, 170, 190), (85, 185, 200), (55, 150, 170), (100, 200, 215),
    (45, 130, 150), (115, 210, 225), (75, 165, 180), (50, 138, 155),
    (130, 218, 232), (40, 118, 135), (90, 190, 205),
]

# ══════════════════════════════════════════
# 字体
# ═════════════════════════════════════════
def load_font(size):
    for p in [
        '/System/Library/Fonts/PingFang.ttc',
        '/System/Library/Fonts/STHeiti Light.ttc',
        '/System/Library/Fonts/Hiragino Sans GB.ttc',
    ]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

f_title = load_font(52)
f_sub = load_font(24)
f_root = load_font(72)
f_root_s = load_font(26)
f_ch = load_font(34)
f_ch_num = load_font(18)
f_item = load_font(24)

# ══════════════════════════════════════════
# 画布 & 布局
# ══════════════════════════════════════════
W = 2200
H = 5400
img = Image.new('RGB', (W, H), BG)
D = ImageDraw.Draw(img)

ROOT_X, ROOT_Y = 200, None   # ROOT_Y 在计算 ch_cy 后设定
ROOT_R = 90

CH_X = 520                      # 章节节点列
ITEM_X = 820                    # 子题文字起始

ROW_H = 32                      # 子题行高
CH_GAP = 48                     # 章节间距
CH_R = 38                       # 章节节点半径
START_Y = 120                   # 第一页起始 Y

# ══════════════════════════════════════════
# 背景网格
# ═════════════════════════════════════════
for x in range(0, W, 50):
    D.line([(x, 0), (x, H)], fill=GRID, width=1)
for y in range(0, H, 50):
    D.line([(0, y), (W, y)], fill=GRID, width=1)

# ══════════════════════════════════════════
# 按内容量比例分配垂直空间
# ══════════════════════════════════════════
ch_sizes = [len(s) for _, s in DATA]
total_items = sum(ch_sizes)
total_gap = CH_GAP * (len(DATA) - 1)
avail_h = H - START_Y - 80 - total_gap

# 先按行数算原始高度，再等比缩放到可用空间
ch_h_raw = [max(s * ROW_H, ROW_H * 4) for s in ch_sizes]
scale = avail_h / sum(ch_h_raw)
ch_h = [max(int(h * scale), ROW_H * 4) for h in ch_h_raw]

# 每章中心 y
ch_cy = []
cur_y = START_Y
for i in range(len(DATA)):
    ch_cy.append(cur_y + ch_h[i] // 2)
    cur_y += ch_h[i] + CH_GAP

# 根节点 Y = 章节垂直中心
ROOT_Y = (ch_cy[0] + ch_cy[-1]) // 2

# ══════════════════════════════════════════
# 根节点
# ══════════════════════════════════════════
# 外圈光晕
for ring in range(8):
    r_o = ROOT_R + 60 - ring * 8
    a = 30 - ring * 4
    if a > 0:
        D.ellipse([ROOT_X-r_o, ROOT_Y-r_o, ROOT_X+r_o, ROOT_Y+r_o],
                  fill=(GOLD[0], GOLD[1], GOLD[2], a))

# 主圆
D.ellipse([ROOT_X-ROOT_R, ROOT_Y-ROOT_R, ROOT_X+ROOT_R, ROOT_Y+ROOT_R],
          fill=(16, 34, 62), outline=GOLD, width=6)

# 内圈装饰
D.ellipse([ROOT_X-ROOT_R+14, ROOT_Y-ROOT_R+14, ROOT_X+ROOT_R-14, ROOT_Y+ROOT_R-14],
          outline=(GOLD[0]//2, GOLD[1]//2, GOLD[2]//2), width=2)

# "函数"
bb3 = D.textbbox((0, 0), '函数', font=f_root)
tw3 = bb3[2]-bb3[0]; th3 = bb3[3]-bb3[1]
D.text((ROOT_X - tw3//2, ROOT_Y - th3//2), '函数', fill=GOLD_HI, font=f_root)

# ══════════════════════════════════════════
# 绘制：11 章 + 子题
# ══════════════════════════════════════════
for ci in range(len(DATA)):
    ch_name, items = DATA[ci]
    col = CH_COLORS[ci]
    cy = ch_cy[ci]
    cnt = len(items)

    # ─ 根 → 章 连线（smoothstep 曲线）──
    steps = 80
    prev = None
    for si in range(steps + 1):
        t = si / steps
        et = t * t * (3 - 2 * t)  # smoothstep
        x = (ROOT_X + ROOT_R) + (CH_X - 20 - 14 - ROOT_X - ROOT_R) * t
        y = ROOT_Y + (cy - ROOT_Y) * et
        pt = (int(x), int(y))
        if prev:
            D.line([prev, pt], fill=col, width=2)
        prev = pt

    # ─ 章名称（椭圆框，无圆节点）──
    lx = CH_X - 20
    bb5 = D.textbbox((0, 0), ch_name, font=f_ch)
    chh = bb5[3]-bb5[1]
    chw = bb5[2]-bb5[0]
    # 椭圆框
    pad_x, pad_y = 14, 10
    D.ellipse([lx-pad_x, cy-chh//2-2-pad_y, lx+chw+pad_x, cy+chh//2-2+pad_y],
              fill=(col[0]//8, col[1]//8, col[2]//8), outline=col, width=2)
    D.text((lx, cy - chh // 2 - 2), ch_name, fill=SNOW, font=f_ch)
    ellipse_right = lx + chw + pad_x

    # ── 条目数徽章（已隐藏）──
    # num_t = f'{cnt} 题'
    # bb6 = D.textbbox((0, 0), num_t, font=f_ch_num)
    # nw = bb6[2]-bb6[0]; nh = bb6[3]-bb6[1]
    # bx, by = lx, cy + chh // 2 + 8
    # D.rounded_rectangle([bx, by, bx+nw+12, by+nh+8], radius=5,
    #                     fill=(col[0]//6, col[1]//6, col[2]//6), outline=col, width=1)
    # D.text((bx + 5, by + 3), num_t, fill=col, font=f_ch_num)

    # ── 子题 ──
    block_h = ch_h[ci]
    item_start_y = cy - block_h // 2

    for j, item in enumerate(items):
        if cnt == 1:
            iy = cy
        else:
            iy = item_start_y + (j + 0.5) * (block_h / cnt)

        # 章 → 子题 连线（细线）
        D.line([(ellipse_right, cy), (ITEM_X - 16, iy)], fill=col, width=1)

        # 小圆点
        dr = 4
        D.ellipse([ITEM_X-dr-1, iy-dr-1, ITEM_X+dr+1, iy+dr+1],
                  fill=col, outline=col, width=1)

        # 子题文字
        D.text((ITEM_X + dr + 10, iy - 11), item, fill=SNOW, font=f_item)

# ══════════════════════════════════════════
# 保存
# ══════════════════════════════════════════
out = 'assets/mindmap-tree.png'
img.save(out, 'PNG')
print(f'✅ {out}  {W}×{H}')
print(f'   总条目: {total_items}, 章节数: {len(DATA)}')
for i, (n, items) in enumerate(DATA):
    print(f'   [{i+1}] {n}: {len(items)} 项, h={ch_h[i]}px, cy={ch_cy[i]}')
