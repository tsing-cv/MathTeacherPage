#!/usr/bin/env python3
"""高中常见函数图象全集 v3 — 深度美学优化版
31函数(19常见+6大名模+6小名模), 4列x8行, 精致卡片网格
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import os

plt.rcParams['font.sans-serif'] = ['PingFang SC', 'STHeiti', 'Hiragino Sans GB']
plt.rcParams['axes.unicode_minus'] = False

# ══════════════════════════════════════════
# 精致色板 (Refined Palette)
# ══════════════════════════════════════════
BG       = '#0B1929'       # 更深邃的蓝黑底
CARD_BG  = '#0F2035'       # 卡片微亮于底
BORDER   = '#1E3A52'       # 柔和的卡片边框
GRID_C   = '#152840'       # 极淡网格（不抢视线）
AXIS_C   = '#2A4560'       # 坐标轴
TICK_C   = '#506878'       # 刻度数字
CURVE    = '#48C8E0'       # 曲线主色（清透青）
CURVE_G  = '#48C8E0'       # 曲线辉光（同色半透）
EXTREMA  = '#E8734A'       # 极值点（暖珊瑚，不刺眼）
GOLD     = '#C8A84E'       # 六大名模标签
GREEN    = '#5DB88A'       # 六小名模标签
DIM      = '#4A6070'       # 常见函数标签
NAME_C   = '#D0DCE6'       # 函数名（亮灰白）
NOTE_C   = '#8899A6'       # 注释文字（柔灰蓝）
PI_C     = '#607888'       # π 刻度色

# ══════════════════════════════════════════
# 31 个函数定义
# ══════════════════════════════════════════
funcs = [
    # ── 19 类常见函数 ──
    {'label': 'f(x) = c  (常数)', 'grp': 0,
     'fn': lambda x: x*0+2, 'xlim': (-3,3), 'ylim': (-1,4),
     'ext': [],
     'note': ['定义域 R · 值域 {c}', 'f′(x) = 0', '水平直线 · 既奇又偶(c=0)']},
    {'label': 'f(x) = kx+b  (一次)', 'grp': 0,
     'fn': lambda x: 0.8*x+1, 'xlim': (-3,3), 'ylim': (-2,4),
     'ext': [],
     'note': ['定义域 R · 值域 R', 'f′(x) = k（常数）', 'k>0 递增 · k<0 递减']},
    {'label': 'f(x) = ax²+bx+c  (二次)', 'grp': 0,
     'fn': lambda x: x**2-1, 'xlim': (-3,3), 'ylim': (-2,5),
     'ext': [(0,-1,'极小 −1')],
     'note': ['定义域 R · 抛物线', '对称轴 x = −b/2a', 'a>0 开口向上']},
    {'label': 'f(x) = k/x  (反比例)', 'grp': 0,
     'fn': lambda x: 1.0/x, 'xlim': (-3,3), 'ylim': (-3,3),
     'ext': [],
     'note': ['定义域 x≠0 · 奇函数', 'f′(x) = −k/x²', 'x/y 轴为渐近线']},
    {'label': 'f(x) = x²  (幂)', 'grp': 0,
     'fn': lambda x: x**2, 'xlim': (-2,2), 'ylim': (-0.5,4),
     'ext': [(0,0,'极小 0')],
     'note': ['定义域 R · 偶函数', 'f′(x) = 2x', '开口向上抛物线']},
    {'label': 'f(x) = x³  (幂)', 'grp': 0,
     'fn': lambda x: x**3, 'xlim': (-2,2), 'ylim': (-4,4),
     'ext': [],
     'note': ['定义域 R · 奇函数', 'f′(x) = 3x² ≥ 0', '全 R 递增 · 对称中心(0,0)']},
    {'label': 'f(x) = √x  (幂)', 'grp': 0,
     'fn': lambda x: np.sqrt(np.maximum(x,0)), 'xlim': (-0.2,4), 'ylim': (-0.3,2.2),
     'ext': [],
     'note': ['定义域 x≥0 · 非奇非偶', 'f′(x) = 1/(2√x)', '单调递增 · 过(0,0)(1,1)']},
    {'label': 'f(x) = |x|  (绝对值)', 'grp': 0,
     'fn': lambda x: np.abs(x), 'xlim': (-3,3), 'ylim': (-0.5,3.5),
     'ext': [(0,0,'极小 0')],
     'note': ['定义域 R · 偶函数', 'f(x)=x(x≥0), −x(x<0)', 'V 字形 · 极小 0(x=0)']},
    {'label': 'f(x) = sgn(x)  (符号)', 'grp': 0,
     'fn': lambda x: np.sign(x), 'xlim': (-2,2), 'ylim': (-1.5,1.5),
     'ext': [],
     'note': ['定义域 R · 奇函数', 'x>0→1, x=0→0, x<0→−1', '分段常数 · x=0 跳跃']},
    {'label': 'f(x) = x⌋  (取整)', 'grp': 0,
     'fn': lambda x: np.floor(x), 'xlim': (-2.5,3.5), 'ylim': (-3,4),
     'ext': [],
     'note': ['定义域 R · 非奇非偶', '阶梯函数 · 每整数跳跃', '⌊2.7⌋=2 · ⌊−1.3⌋=−2']},
    {'label': 'f(x) = a  (指数)', 'grp': 0,
     'fn': lambda x: 2**x, 'xlim': (-3,3), 'ylim': (-0.3,5),
     'ext': [],
     'note': ['定义域 R · 值域 (0,+∞)', '恒过 (0,1) · a>1 递增', 'x 轴为渐近线']},
    {'label': 'f(x) = eˣ  (衰减)', 'grp': 0,
     'fn': lambda x: np.exp(-x), 'xlim': (-2,4), 'ylim': (-0.1,4),
     'ext': [],
     'note': ['定义域 R · 值域 (0,+∞)', '恒过 (0,1) · 单调递减', 'x 轴为渐近线 · 衰减模型']},
    {'label': 'f(x) = log_a(x)  (对数)', 'grp': 0,
     'fn': lambda x: np.log2(np.maximum(x,1e-10)), 'xlim': (0.01,5), 'ylim': (-3,3),
     'ext': [],
     'note': ['定义域 x>0 · 值域 R', '恒过 (1,0) · a>1 递增', 'y 轴为渐近线']},
    {'label': 'f(x) = sin x', 'grp': 0,
     'fn': lambda x: np.sin(x), 'xlim': (-2*np.pi, 2*np.pi), 'ylim': (-1.5,1.5),
     'ext': [(np.pi/2,1,'极大 1'),(-np.pi/2,-1,'极小 −1')],
     'note': ['定义域 R · 奇函数 · 周期 2π', 'f′(x) = cos x', '值域 [−1,1] · 对称中心(kπ,0)']},
    {'label': 'f(x) = cos x', 'grp': 0,
     'fn': lambda x: np.cos(x), 'xlim': (-2*np.pi, 2*np.pi), 'ylim': (-1.5,1.5),
     'ext': [(0,1,'极大 1'),(np.pi,-1,'极小 −1')],
     'note': ['定义域 R · 偶函数 · 周期 2π', 'f′(x) = −sin x', '值域 [−1,1] · sin 左移 π/2']},
    {'label': 'f(x) = tan x', 'grp': 0,
     'fn': lambda x: np.tan(x), 'xlim': (-1.9,1.9), 'ylim': (-4,4),
     'ext': [],
     'note': ['定义域 x≠π/2+kπ · 奇函数', 'f′(x) = 1/cos²x > 0', '周期 π · 每段单调递增']},
    {'label': 'f(x) = arcsin x', 'grp': 0,
     'fn': lambda x: np.arcsin(np.clip(x,-1,1)), 'xlim': (-1.2,1.2), 'ylim': (-2,2),
     'ext': [],
     'note': ['定义域 [−1,1] · 值域 [−π/2,π/2]', '奇函数 · 单调递增', 'f′(x) = 1/√(1−x²)']},
    {'label': 'f(x) = arctan x', 'grp': 0,
     'fn': lambda x: np.arctan(x), 'xlim': (-4,4), 'ylim': (-2,2),
     'ext': [],
     'note': ['定义域 R · 值域 (−π/2,π/2)', '奇函数 · 单调递增', 'y = ±π/2 渐近线']},
    {'label': 'f(x) = x+1/x  (对勾)', 'grp': 0,
     'fn': lambda x: x+1.0/x, 'xlim': (-3,3), 'ylim': (-4,4),
     'ext': [(1,2,'极小 2'),(-1,-2,'极大 −2')],
     'note': ['定义域 x≠0 · 奇函数', 'f′(x) = 1−1/x²', 'x>0 极小 2(x=1) · x<0 极大 −2']},

    # ── 六大名模 ──
    {'label': 'f(x) = xeˣ', 'grp': 1,
     'fn': lambda x: x*np.exp(x), 'xlim': (-3,1.5), 'ylim': (-0.6,1.5),
     'ext': [(-1,-1/np.e,'极小 −1/e')],
     'note': ['定义域 R · x→−∞, f→0', 'f′(x) = (x+1)eˣ', '递减(−∞,−1) · 递增(−1,+∞)']},
    {'label': 'f(x) = x/eˣ', 'grp': 1,
     'fn': lambda x: x/np.exp(x), 'xlim': (-0.5,5), 'ylim': (-0.1,0.5),
     'ext': [(1,1/np.e,'极大 1/e')],
     'note': ['定义域 R · x→+∞, f→0', 'f′(x) = (1−x)/eˣ', '递增(0,1) · 递减(1,+∞)']},
    {'label': 'f(x) = eˣ/x', 'grp': 1,
     'fn': lambda x: np.exp(x)/x, 'xlim': (-2,4), 'ylim': (-3,5),
     'ext': [(1,np.e,'极小 e')],
     'note': ['定义域 x≠0', 'f′(x) = (x−1)eˣ/x²', 'x=0 渐近线 · x>0 极小 e(x=1)']},
    {'label': 'f(x) = x ln x', 'grp': 1,
     'fn': lambda x: x*np.log(x), 'xlim': (0.01,3), 'ylim': (-0.5,2),
     'ext': [(1/np.e,-1/np.e,'极小 −1/e')],
     'note': ['定义域 x>0 · f(1)=0', 'f′(x) = ln x+1', 'x→0⁺ 时 f→0 · 极小 −1/e']},
    {'label': 'f(x) = ln x / x', 'grp': 1,
     'fn': lambda x: np.log(x)/x, 'xlim': (0.1,6), 'ylim': (-0.3,0.5),
     'ext': [(np.e,1/np.e,'极大 1/e')],
     'note': ['定义域 x>0 · f(1)=0', 'f′(x) = (1−ln x)/x²', 'x→+∞, f→0 · 极大 1/e(x=e)']},
    {'label': 'f(x) = x / ln x', 'grp': 1,
     'fn': lambda x: x/np.log(x), 'xlim': (0.1,5), 'ylim': (-3,5),
     'ext': [(np.e,np.e,'极小 e')],
     'note': ['定义域 x>0, x≠1', 'f′(x) = (ln x−1)/(ln x)²', 'x=1 渐近线 · 极小 e(x=e)']},

    # ── 六小名模 ──
    {'label': 'f(x) = x + ln x', 'grp': 2,
     'fn': lambda x: x+np.log(x), 'xlim': (0.01,4), 'ylim': (-3,4),
     'ext': [],
     'note': ['定义域 x>0 · 单调递增', 'f′(x) = 1+1/x > 0', 'f(1)=1 · 无驻点']},
    {'label': 'f(x) = x − ln x', 'grp': 2,
     'fn': lambda x: x-np.log(x), 'xlim': (0.01,5), 'ylim': (-0.5,5),
     'ext': [(1,1,'极小 1')],
     'note': ['定义域 x>0', 'f′(x) = 1−1/x', '恒有 x−ln x ≥ 1 · 极小 1(x=1)']},
    {'label': 'f(x) = ln x − x', 'grp': 2,
     'fn': lambda x: np.log(x)-x, 'xlim': (0.01,5), 'ylim': (-5,0.5),
     'ext': [(1,-1,'极大 −1')],
     'note': ['定义域 x>0', 'f′(x) = 1/x−1', '恒有 ln x−x ≤ −1 · 极大 −1(x=1)']},
    {'label': 'f(x) = eˣ − x', 'grp': 2,
     'fn': lambda x: np.exp(x)-x, 'xlim': (-3,2), 'ylim': (0.5,5),
     'ext': [(0,1,'极小 1')],
     'note': ['定义域 R', 'f′(x) = eˣ−1', '恒有 eˣ−x ≥ 1 · 极小 1(x=0)']},
    {'label': 'f(x) = eˣ + x', 'grp': 2,
     'fn': lambda x: np.exp(x)+x, 'xlim': (-3,2), 'ylim': (-3,8),
     'ext': [],
     'note': ['定义域 R · 单调递增', 'f′(x) = e+1 > 0', 'f(0)=1 · 无驻点']},
    {'label': 'f(x) = ln x + x', 'grp': 2,
     'fn': lambda x: np.log(x)+x, 'xlim': (0.01,4), 'ylim': (-4,5),
     'ext': [],
     'note': ['定义域 x>0 · 单调递增', 'f′(x) = 1/x+1 > 0', 'f(1)=1 · x→0⁺ 时 f→−∞']},
]

# ══════════════════════════════════════════
# 布局: 4 列 × 8 行 = 32 格 (末格空)
# 每格 = 1 图行 + 1 文行
# ═════════════════════════════════════════
PH = 10    # 图行高度比
TH = 3     # 文行高度比
N  = len(funcs)           # 31
COLS = 4
ROWS = (N + COLS - 1) // COLS   # 8

hr = []
for _ in range(ROWS):
    hr.extend([PH, TH])

fig = plt.figure(figsize=(18, 26), facecolor=BG, dpi=130)
gs = gridspec.GridSpec(len(hr), COLS, figure=fig,
                       height_ratios=hr,
                       hspace=0.05, wspace=0.06,
                       left=0.02, right=0.98,
                       top=0.995, bottom=0.005)

GRP_NAMES  = ['常见函数', '六大名模', '六小名模']
GRP_COLORS = [DIM, GOLD, GREEN]

# π 刻度格式化
def pi_fmt(val, _pos=None):
    if abs(val) < 1e-9: return '0'
    r = val / np.pi
    for d, s in [(2,'π/2'),(1,'π'),(1.5,'3π/2'),(2,'2π')]:
        if abs(abs(r)-d) < 0.05:
            return (('-'+s) if r<0 else s)
    return f'{val:.1f}'

for idx, f in enumerate(funcs):
    r  = (idx // COLS) * 2
    c  = idx % COLS
    tr = r + 1
    xlo, xhi = f['xlim']
    ylo, yhi = f['ylim']
    is_trig  = f['label'] in ('f(x) = sin x','f(x) = cos x')
    is_tan   = f['label'] == 'f(x) = tan x'
    is_arcsin= f['label'] == 'f(x) = arcsin x'

    # ────────────────── 绘图区 ──────────────────
    ax = fig.add_subplot(gs[r, c])
    ax.set_facecolor(CARD_BG)

    # 四周边框 — 细而柔和
    for s in ['top','bottom','left','right']:
        sp = ax.spines[s]
        sp.set_color(BORDER)
        sp.set_linewidth(0.8)

    ax.tick_params(colors=TICK_C, labelsize=9, length=4, pad=3)
    ax.grid(True, color=GRID_C, linewidth=0.35, alpha=0.7)
    ax.set_xlim(xlo, xhi)
    ax.set_ylim(ylo, yhi)
    ax.axhline(0, color=AXIS_C, lw=0.5, zorder=0)
    ax.axvline(0, color=AXIS_C, lw=0.5, zorder=0)

    # 三角函数 π 刻度
    if is_trig:
        ax.set_xticks([-2*np.pi,-1.5*np.pi,-np.pi,-np.pi/2,0,
                        np.pi/2,np.pi,1.5*np.pi,2*np.pi])
        ax.xaxis.set_major_formatter(plt.FuncFormatter(pi_fmt))
        ax.tick_params(axis='x', labelsize=8, colors=PI_C)
    elif is_tan:
        ax.set_xticks([-np.pi/2, 0, np.pi/2])
        ax.xaxis.set_major_formatter(plt.FuncFormatter(pi_fmt))
        ax.tick_params(axis='x', labelsize=8, colors=PI_C)
    if is_arcsin:
        ax.set_yticks([-np.pi/2, 0, np.pi/2])
        ax.yaxis.set_major_formatter(plt.FuncFormatter(pi_fmt))
        ax.tick_params(axis='y', labelsize=8, colors=PI_C)

    # ── 曲线绘制 (含辉光) ──
    def draw_curve(xxs):
        """画曲线: 先画粗半透明辉光, 再画细主线"""
        for xx in xxs:
            yy = f['fn'](xx)
            m = np.abs(yy) < 50
            if m.sum() < 2: continue
            xp, yp = xx[m], yy[m]
            # 辉光层
            ax.plot(xp, yp, color=CURVE_G, lw=4.5, alpha=0.10, zorder=1, solid_capstyle='round')
            # 主线
            ax.plot(xp, yp, color=CURVE, lw=1.6, alpha=0.92, zorder=2, solid_capstyle='round')

    if f['label'] == 'f(x) = k/x  (反比例)':
        draw_curve([np.linspace(xlo,-0.02,300), np.linspace(0.02,xhi,300)])
    elif f['label'] == 'f(x) = eˣ/x':
        draw_curve([np.linspace(xlo,-0.01,200), np.linspace(0.01,xhi,300)])
    elif f['label'] == 'f(x) = x / ln x':
        draw_curve([np.linspace(max(xlo,0.01),0.98,200), np.linspace(1.02,xhi,300)])
    elif is_tan:
        segs = []
        for k in range(-1,2):
            xa = max(-np.pi/2+k*np.pi+0.03, xlo)
            xb = min( np.pi/2+k*np.pi-0.03, xhi)
            if xb > xa + 0.01:
                segs.append(np.linspace(xa, xb, 200))
        draw_curve(segs)
    elif f['label'] == 'f(x) = x+1/x  (对勾)':
        draw_curve([np.linspace(xlo,-0.02,300), np.linspace(0.02,xhi,300)])
    elif f['label'] == 'f(x) = sgn(x)  (符号)':
        # 三段水平线 + 跳跃虚线
        ax.plot([-2,0],[-1,-1], color=CURVE, lw=1.6, alpha=0.9, zorder=2)
        ax.plot([0,2],[1,1],   color=CURVE, lw=1.6, alpha=0.9, zorder=2)
        ax.plot([0,0],[-1,1],  color=CURVE, lw=0.8, alpha=0.3, linestyle=':', zorder=1)
        ax.scatter([0],[0], color=CURVE, s=28, zorder=3, edgecolors=CARD_BG, linewidths=1.2)
        ax.scatter([-1],[-1], color=CURVE, s=28, zorder=3, edgecolors=CARD_BG, linewidths=1.2)
        ax.scatter([1],[1],   color=CURVE, s=28, zorder=3, edgecolors=CARD_BG, linewidths=1.2)
    elif f['label'] == 'f(x) = ⌊x⌋  (取整)':
        for n in range(-3,4):
            ax.plot([n,n+1],[n,n], color=CURVE, lw=1.6, alpha=0.9, zorder=2)
            ax.scatter([n],[n],   color=CURVE, s=22, zorder=3)
            ax.scatter([n+1],[n], color=CARD_BG, s=22, zorder=3,
                       edgecolors=CURVE, linewidths=1.0)
    else:
        x_start = max(xlo, 0.001) if any(k in f['label'] for k in ['ln','log','√','arcsin']) else xlo
        x = np.linspace(x_start, xhi, 600)
        draw_curve([x])

    # ── 极值点 (精致双层圆点) ──
    for ex, ey, elabel in f['ext']:
        # 外圈光晕
        ax.scatter([ex],[ey], s=80, color=EXTREMA, alpha=0.15, zorder=3)
        # 内点
        ax.scatter([ex],[ey], s=22, color=EXTREMA, zorder=4,
                   edgecolors='#FFFFFF', linewidths=0.5)
        # 标签偏移
        mid_y = (ylo + yhi) / 2
        oy = 7 if ey < mid_y else -11
        ax.annotate(elabel, (ex,ey), textcoords='offset points',
                    xytext=(6, oy), fontsize=9, color=EXTREMA,
                    fontweight='bold', fontfamily='sans-serif')

    # ── 分组标签 (右上角, 极简) ──
    gc = GRP_COLORS[f['grp']]
    ax.text(0.97, 0.97, GRP_NAMES[f['grp']], transform=ax.transAxes,
            fontsize=8, color=gc, ha='right', va='top',
            fontweight='normal', fontfamily='sans-serif', alpha=0.7)

    # ────────────────── 文字区 ──────────────────
    tax = fig.add_subplot(gs[tr, c])
    tax.set_facecolor(CARD_BG)
    tax.axis('off')
    for s in ['top','bottom','left','right']:
        sp = tax.spines[s]
        sp.set_color(BORDER)
        sp.set_linewidth(0.8)

    # 动态计算行高 — 绝不溢出
    fig_h_px = fig.get_figheight() * fig.dpi
    total_ratio = sum(hr)
    cell_h_px = TH / total_ratio * fig_h_px
    n_lines = len(f['note'])
    padding_px = 14
    avail_px = cell_h_px - padding_px
    line_gap_px = avail_px / (n_lines + 1)
    title_gap = line_gap_px * 1.1

    # 函数名 — 亮色粗体
    y_title = 1.0 - padding_px / cell_h_px
    tax.text(0.05, y_title, f['label'], transform=tax.transAxes,
             fontsize=14, fontweight='bold', color=NAME_C,
             fontfamily='sans-serif', va='top')

    # 注释行 — 柔灰
    y_note_start = y_title - title_gap / cell_h_px
    gap_frac = line_gap_px / cell_h_px
    for j, note in enumerate(f['note']):
        y = y_note_start - j * gap_frac
        if y < 0.02: break  # 防止溢出
        tax.text(0.05, y, note, transform=tax.transAxes,
                 fontsize=10.5, color=NOTE_C, fontfamily='sans-serif', va='top')

# ═════════════════════════════════════════
# 保存
# ══════════════════════════════════════════
out = 'assets/function-graphs-handbook.png'
fig.savefig(out, dpi=120, facecolor=BG, edgecolor='none',
            bbox_inches='tight', pad_inches=0.08)
plt.close()
sz = os.path.getsize(out)
from PIL import Image
im = Image.open(out)
print(f'OK {out}  {im.size}  {sz/1024/1024:.1f}MB')
print(f'   {N} 函数: 常见{19} + 名模{6} + 小名模{6}')
