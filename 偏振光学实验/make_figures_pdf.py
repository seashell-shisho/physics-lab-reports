# -*- coding: utf-8 -*-
"""
把实验报告的图排成 A4 打印版 PDF（每页两张，图下带图注）。

用法：
    python make_figures_pdf.py            # 生成 偏振光学实验_图集.pdf
    python make_figures_pdf.py --preview  # 同时输出每页的 PNG 预览

想增删图或改图注，只改下面的 FIGURES 列表即可。
注意：图注里不要用 $...$ 数学模式，否则 matplotlib 会丢掉中文。
"""

import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.font_manager as fm
from PIL import Image

# ---------- 图与图注（顺序即打印顺序） ----------
FIGURES = [
    ('图1_散点+线性拟合.png',            '图 1  马吕斯定律：I/I₀–cos²α 线性拟合'),
    ('图2_折线图.png',                   '图 2  马吕斯定律：I/I₀–cos²α 折线图'),
    ('图1_半波片_线性拟合.png',           '图 3  1/2 波片：检偏器转角 β 与波片转角 θ'),
    ('图1_四分之一波片_极坐标.png',        '图 4  1/4 波片（初始态）极坐标图'),
    ('图2_四分之一波片_45度_极坐标.png',   '图 5  1/4 波片（45°）极坐标图'),
    ('图3_四分之一波片_20度_极坐标.png',   '图 6  1/4 波片（20°）极坐标图'),
    ('图4_初始态_角度-功率_拟合.png',      '图 7  初始态 A–φ 线性拟合'),
    ('图5_45度_角度-功率_拟合.png',        '图 8  45° A–φ 线性拟合'),
]

OUT_PDF = '偏振光学实验_图集.pdf'
A4_IN = (8.27, 11.69)        # A4 / 英寸
SLOT_H = 0.455               # 每张图占页高的比例
CAP_GAP = 0.03               # 图与图注之间的空隙（页高比例）

# ---------- 中文字体 ----------
_installed = {f.name for f in fm.fontManager.ttflist}
_cjk = next((f for f in ['SimSun', 'STSong', 'Noto Serif SC', 'SimHei',
                         'Microsoft YaHei'] if f in _installed), 'DejaVu Sans')
rcParams['font.family'] = ['Times New Roman', _cjk, 'DejaVu Sans']
rcParams['mathtext.fontset'] = 'stix'
rcParams['axes.unicode_minus'] = False


def make_page(items):
    """把 1~2 张图排到一页 A4 上：图片在上、图注在下。"""
    fig = plt.figure(figsize=A4_IN)
    for k, (path, caption) in enumerate(items):
        img = Image.open(path).convert('RGB')
        ratio = img.height / img.width                # 高/宽

        slot_bottom = 0.03 if k == 1 else 0.515
        avail_h = (SLOT_H - CAP_GAP - 0.01) * A4_IN[1]
        max_w = 0.86 * A4_IN[0]
        w_in = min(max_w, avail_h / ratio)
        h_in = w_in * ratio

        W = w_in / A4_IN[0]
        H = h_in / A4_IN[1]

        block_h = H + CAP_GAP
        y_block = slot_bottom + (SLOT_H - block_h) / 2

        ax = fig.add_axes([(1 - W) / 2, y_block + CAP_GAP, W, H])
        ax.imshow(img, interpolation='lanczos')
        ax.set_axis_off()

        fig.text(0.5, y_block + CAP_GAP * 0.35, caption,
                 ha='center', va='center', fontsize=10.5)
    return fig


def main():
    preview = '--preview' in sys.argv
    missing = [p for p, _ in FIGURES if not os.path.exists(p)]
    if missing:
        print('缺少图片：', missing)
        return 1

    pages = [FIGURES[i:i + 2] for i in range(0, len(FIGURES), 2)]
    with PdfPages(OUT_PDF) as pdf:
        for n, page in enumerate(pages, 1):
            fig = make_page(page)
            pdf.savefig(fig, dpi=300)          # 位图以 300 dpi 嵌入
            if preview:
                fig.savefig(f'preview_page{n}.png', dpi=110)
            plt.close(fig)

    print(f'已生成 {OUT_PDF}（{len(pages)} 页，共 {len(FIGURES)} 张图）')
    return 0


if __name__ == '__main__':
    sys.exit(main())
