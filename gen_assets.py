# -*- coding: utf-8 -*-
"""
占位素材生成器 —— 数学老师招生单页
生成页面所需的全部占位图片（导师照片 / 二维码 / 分享封面 / 教案笔记截图等）。
所有图片均为本地程序化生成，无任何版权风险；上线前请用真实素材替换 assets/ 下同名文件。

用法：python3 gen_assets.py
依赖：Pillow（pip install Pillow）
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

# ---------- 全局色板（与页面 CSS token 一致） ----------
NAVY_DEEP = (14, 33, 64)      # #0E2140 深空蓝
NAVY_CARD = (22, 48, 92)      # #16305C 层叠蓝
PAPER = (244, 247, 250)       # #F4F7FA 冷纸白
GOLD = (194, 160, 95)         # #C2A05F 主金（冷纸黄铜）
GOLD_HI = (227, 200, 138)     # #E3C88A 亮金
GOLD_DEEP = (122, 94, 47)     # #7A5E2F 暗金（冷纸黄铜）
SNOW = (232, 237, 245)        # #E8EDF5 雾白
GRAY_D = (143, 160, 188)      # #8FA0BC 灰蓝
KRAFT = (216, 201, 163)       # 牛皮纸色（证据链档案卡）
INK = (27, 42, 68)            # #1B2A44 墨蓝

FONT_SANS = "/System/Library/Fonts/Hiragino Sans GB.ttc"        # 无衬线（正文/说明）
FONT_SERIF = "/System/Library/Fonts/Supplemental/Songti.ttc"    # 宋体衬线（标题，学术气质）
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")


def font(size, index=0):
    """加载系统字体（macOS 自带，随 OS 授权，无版权问题）。index: 0=无衬线 1=宋体衬线"""
    path = FONT_SERIF if index == 1 else FONT_SANS
    return ImageFont.truetype(path, size=size, index=0)


def ensure_dir():
    os.makedirs(OUT_DIR, exist_ok=True)


def canvas_bg(draw, w, h, base, grid_color, cell=32, heavy_every=4, heavy_alpha_boost=1.6):
    """绘制坐标纸网格背景（与页面 CSS 纹理呼应）"""
    for x in range(0, w, cell):
        heavy = (x // cell) % heavy_every == 0
        c = tuple(min(255, int(v * heavy_alpha_boost)) for v in grid_color) if heavy else grid_color
        draw.line([(x, 0), (x, h)], fill=c, width=1)
    for y in range(0, h, cell):
        heavy = (y // cell) % heavy_every == 0
        c = tuple(min(255, int(v * heavy_alpha_boost)) for v in grid_color) if heavy else grid_color
        draw.line([(0, y), (w, y)], fill=c, width=1)


def text_center(draw, xy, text, fnt, fill):
    """按中心对齐绘制文字"""
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x, y = xy
    draw.text((x - tw / 2 - bbox[0], y - th / 2 - bbox[1]), text, font=fnt, fill=fill)


def curve(draw, w, h, color, width=3, phase=0.0):
    """绘制 Hero 同款正弦叠加曲线，营造页面一致性"""
    pts = []
    for px in range(0, w, 4):
        t = px / w * math.pi * 4
        y = h * 0.55 - (math.sin(t + phase) * h * 0.16 + math.sin(t * 2.7 + phase * 1.5) * h * 0.07)
        pts.append((px, y))
    draw.line(pts, fill=color, width=width, joint="curve")


def gen_og_cover():
    """微信分享卡封面 1200x630（微信好友卡会裁切为近似方形，主体内容居中）"""
    w, h = 1200, 630
    img = Image.new("RGB", (w, h), NAVY_DEEP)
    d = ImageDraw.Draw(img)
    canvas_bg(d, w, h, NAVY_DEEP, tuple(int(c * 1.45) for c in NAVY_DEEP))
    curve(d, w, h, tuple(int(c * 0.55) for c in GOLD), width=2, phase=0.8)
    # 金色细边框（学术精装书装订线隐喻）
    d.rectangle([24, 24, w - 24, h - 24], outline=GOLD, width=2)
    text_center(d, (w / 2, h * 0.36), "18,000 道题", font(92, 1), SNOW)
    text_center(d, (w / 2, h * 0.52), "串成 300 串", font(92, 1), SNOW)
    text_center(d, (w / 2, h * 0.66), "学一道，会一串", font(40, 1), GOLD_HI)
    text_center(d, (w / 2, h * 0.78), "高考真题 · 主流模拟 · 竞赛题，逐题拆过建档", font(26), GRAY_D)
    d.line([(w / 2 - 90, h * 0.83), (w / 2 + 90, h * 0.83)], fill=GOLD, width=2)
    text_center(d, (w / 2, h * 0.90), "陈老师 · 高一至考研 · 3-5 人小班直播", font(30, 1), GOLD_HI)
    img.save(os.path.join(OUT_DIR, "og-cover.png"), optimize=True)


def gen_portrait():
    """导师照片占位 800x1000（替换为真人形象照，浅色墙面正面半身照最佳）"""
    w, h = 800, 1000
    img = Image.new("RGB", (w, h), NAVY_CARD)
    d = ImageDraw.Draw(img)
    canvas_bg(d, w, h, NAVY_CARD, tuple(int(c * 1.35) for c in NAVY_CARD))
    # 简约人形剪影（示意）
    cx = w / 2
    d.ellipse([cx - 110, 250, cx + 110, 470], fill=NAVY_DEEP)          # 头
    d.pieslice([cx - 230, 500, cx + 230, 950], 180, 360, fill=NAVY_DEEP)  # 肩
    d.rectangle([20, 20, w - 20, h - 20], outline=GOLD, width=3)         # 金框
    text_center(d, (w / 2, 130), "老师照片占位", font(44, 1), GOLD_HI)
    text_center(d, (w / 2, 890), "请替换 assets/portrait.png", font(26), GRAY_D)
    img.save(os.path.join(OUT_DIR, "portrait.png"), optimize=True)


def gen_qr():
    """二维码占位 480x560（必须保留 PNG 位图格式：微信长按识别仅支持 img 位图）"""
    w, h = 480, 560
    img = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(img)
    # 伪二维码点阵（不可扫描，仅示意）
    random.seed(2026)
    n, cell = 25, 16
    ox, oy = (w - n * cell) / 2, 40
    dark = INK
    for r in range(n):
        for c in range(n):
            if random.random() < 0.45:
                d.rectangle([ox + c * cell, oy + r * cell,
                             ox + (c + 1) * cell - 2, oy + (r + 1) * cell - 2], fill=dark)
    # 三个定位角
    for (px, py) in [(ox, oy), (ox + (n - 7) * cell, oy), (ox, oy + (n - 7) * cell)]:
        d.rectangle([px, py, px + 7 * cell - 2, py + 7 * cell - 2], outline=dark, width=cell)
        d.rectangle([px + 2 * cell, py + 2 * cell, px + 5 * cell - 2, py + 5 * cell - 2], fill=dark)
    # "数学" 大字（定位角下方、居中）
    text_center(d, (w / 2, 486), "数学", font(52, 1), NAVY_DEEP)
    text_center(d, (w / 2, 530), "请替换 assets/qr-wechat.png", font(22), (120, 128, 144))
    img.save(os.path.join(OUT_DIR, "qr-wechat.png"), optimize=True)


def gen_evidence():
    """证据链占位图：手写教案 / 真题批注 / 统计手稿（牛皮纸档案卡质感）+ 直播板书"""
    specs = [
        ("notes-lesson.png", KRAFT, "手写教案占位", "请替换为真实备课手稿扫描件", "assets/notes-lesson.png", (800, 620)),
        ("notes-annotate.png", (232, 226, 208), "真题批注占位", "请替换为真题册多轮批注页照片", "assets/notes-annotate.png", (800, 620)),
        ("notes-stats.png", PAPER, "统计手稿占位", "请替换为考点台账/手绘统计表", "assets/notes-stats.png", (800, 620)),
        ("board-live.png", NAVY_DEEP, "直播板书占位", "请替换为带弹幕的板书截图", "assets/board-live.png", (800, 620)),
    ]
    for name, bg, t1, t2, path, (w, h) in specs:
        img = Image.new("RGB", (w, h), bg)
        d = ImageDraw.Draw(img)
        fg = INK if sum(bg) > 400 else SNOW
        sub = (120, 128, 144) if sum(bg) > 400 else GRAY_D
        # 模拟手写横线/方格纸
        line_c = tuple(min(255, c + 18) for c in bg) if sum(bg) > 400 else tuple(max(0, c + 18) for c in NAVY_CARD)
        for y in range(90, h - 60, 42):
            d.line([(50, y), (w - 50, y)], fill=line_c, width=1)
        if name == "notes-stats.png":
            # 简易台账表格
            for x in range(90, w - 60, 140):
                d.line([(x, 120), (x, h - 90)], fill=line_c, width=1)
            d.line([(70, 120), (w - 70, 120)], fill=GOLD_DEEP, width=2)
        if name == "board-live.png":
            curve(d, w, h, tuple(int(c * 0.9) for c in GOLD), width=3)
        # 胶带贴角（档案桌隐喻）
        tape = (230, 222, 195, 200)
        d.polygon([(30, 24), (130, 8), (150, 40), (50, 56)], fill=(226, 216, 186))
        d.polygon([(w - 130, h - 56), (w - 30, h - 40), (w - 50, h - 8), (w - 150, h - 24)], fill=(226, 216, 186))
        text_center(d, (w / 2, 60), t1, font(38, 1), fg)
        text_center(d, (w / 2, h - 36), f"{t2}（{path}）", font(22), sub)
        img.save(os.path.join(OUT_DIR, name), optimize=True)


def gen_report_sample():
    """听课报告样例占位 1200x620（横幅通栏；教研现场区第 5 张图）
    模拟一份打码后的单讲报告：头部信息条 + 两列表格 + 底部替换提示。
    走神 FAQ、「问题不过夜」卖点、四关制「对关归档」都以它为证据。"""
    w, h = 1200, 620
    img = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(img)
    # 报告头（冷纸白条 + 金色分隔线）
    d.rectangle([0, 0, w, 104], fill=PAPER)
    d.rectangle([0, 104, w, 107], fill=GOLD)
    text_center(d, (w / 2, 52), "学习反馈（样例 · 按周汇总）", font(40, 1), INK)
    # 报告体：两列表格，斑马行；学员名以灰色打码条示意
    rows = [
        ("学员", None),  # 特殊行：打码条 + 班级
        ("日期 / 讲次", "2026-09-19 · 第 5 讲"),
        ("本讲一串", "圆锥曲线 · 三道核心串之二：设而不求"),
        ("限时演练", "1 道同构变式 · 12 / 14 分 · 用时 9 分钟（限时 12）"),
        ("课中答题", "弹幕作答 6 / 7 · 连麦讲题 1 次 · 走神提醒 0 次"),
        ("对关记录", "收尾三查：漏「答案代回」1 次，已归档"),
        ("给家长的话", "本讲一串已过「会」关；下周进「对」关变式训练。"),
    ]
    y0, row_h, lx, rx = 148, 54, 90, 1110
    for i, (k, v) in enumerate(rows):
        y = y0 + i * row_h
        if i % 2 == 0:
            d.rectangle([lx - 20, y - 8, rx + 20, y + row_h - 16], fill=(247, 249, 252))
        d.text((lx, y), k, font=font(26), fill=GOLD_DEEP)
        if v is None:
            d.rectangle([lx + 250, y + 2, lx + 390, y + 28], fill=(198, 205, 216))  # 姓名打码条
            d.text((lx + 406, y), "· 高二 · 周六班", font=font(26), fill=INK)
        else:
            d.text((lx + 250, y), v, font=font(26), fill=INK)
    d.line([(lx - 20, y0 - 16), (rx + 20, y0 - 16)], fill=(180, 188, 200), width=1)
    # 底部替换提示
    text_center(d, (w / 2, h - 32), "占位示意图 —— 请替换 assets/report-sample.png（真实报告截图，学生信息打码）", font(22), (120, 128, 144))
    img.save(os.path.join(OUT_DIR, "report-sample.png"), optimize=True)


def gen_correction_sample():
    """批改痕迹占位 800x620（教研现场区：红笔逐题批注的学生作业）
    白底作业纸 + 红笔勾叉与旁批，示意「不是打勾叉，是告诉你为什么错」。"""
    w, h = 800, 620
    img = Image.new("RGB", (w, h), (255, 253, 248))
    d = ImageDraw.Draw(img)
    RED = (186, 64, 56)
    # 作业纸横线
    for y in range(110, h - 60, 44):
        d.line([(60, y), (w - 60, y)], fill=(214, 220, 228), width=1)
    text_center(d, (w / 2, 60), "学生作业批改占位", font(36, 1), INK)
    # 三道题的「学生解答」灰笔示意（等宽色块）+ 红笔批注
    rows = [
        (150, "✓", "步骤完整，这一道过得硬"),
        (260, "✗", "第二步符号搬家：− 抄成了 +，答案差一个负号——收尾三查第②查"),
        (380, "△", "方法对了没写完：考场时间不够，限时演练每周练的就是这个"),
    ]
    for y, mark, note in rows:
        d.rectangle([70, y, 480, y + 60], fill=(238, 240, 244))          # 学生作答区
        d.text((500, y + 8), mark, font=font(40, 1), fill=RED)            # 红笔判定
        d.text((70, y + 66), note, font=font(22), fill=RED)               # 红笔旁批
    text_center(d, (w / 2, h - 30), "请替换 assets/correction-sample.png（真实作业照片）", font(22), (120, 128, 144))
    img.save(os.path.join(OUT_DIR, "correction-sample.png"), optimize=True)


def gen_student_notes():
    """学生笔记占位 800x620（教研现场区：孩子自己按串归类）
    方格纸 + 串根→变式的归类树示意——方法长在孩子手上才算学会。"""
    w, h = 800, 620
    img = Image.new("RGB", (w, h), PAPER)
    d = ImageDraw.Draw(img)
    # 方格纸
    for x in range(0, w, 28):
        d.line([(x, 0), (x, h)], fill=(222, 228, 236), width=1)
    for y in range(0, h, 28):
        d.line([(0, y), (w, y)], fill=(222, 228, 236), width=1)
    text_center(d, (w / 2, 54), "学生按串归类笔记占位", font(36, 1), INK)
    # 归类树：一道串根挂三个变式
    mx, my = w / 2, 150
    d.rectangle([mx - 150, my - 24, mx + 150, my + 24], outline=GOLD_DEEP, width=3)
    text_center(d, (mx, my), "串根 · 数列求和（错位相减）", font(24), INK)
    leaves = ["2023 新课标Ⅰ·17 题", "2021 全国甲·17 题", "期中卷·压轴变式"]
    for i, t in enumerate(leaves):
        lx = 130 + i * 270
        ly = 300
        d.line([(mx, my + 24), (lx, ly - 22)], fill=GOLD_DEEP, width=2)
        d.rectangle([lx - 118, ly - 22, lx + 118, ly + 22], outline=(90, 107, 133), width=2)
        text_center(d, (lx, ly), t, font(22), (90, 107, 133))
    d.text((90, 400), "自己的话写注：", font=font(24), fill=GOLD_DEEP)
    d.text((90, 440), "「先认结构再动笔——见到等差×等比，就是它。」", font=font(26), fill=INK)
    text_center(d, (w / 2, h - 30), "请替换 assets/student-notes.png（真实学生笔记照片）", font(22), (120, 128, 144))
    img.save(os.path.join(OUT_DIR, "student-notes.png"), optimize=True)


def main():
    ensure_dir()
    gen_og_cover()
    gen_portrait()
    gen_qr()
    gen_evidence()
    gen_report_sample()
    gen_correction_sample()
    gen_student_notes()
    names = sorted(os.listdir(OUT_DIR))
    print("生成完成：")
    for n in names:
        p = os.path.join(OUT_DIR, n)
        print(f"  {n}  {os.path.getsize(p) // 1024} KB")


if __name__ == "__main__":
    main()
