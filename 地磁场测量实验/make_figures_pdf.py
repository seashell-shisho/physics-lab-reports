# -*- coding: utf-8 -*-
"""
把实验报告的图排成 A4 打印版 PDF（每页两张，图下带图注）。

用法：
    python make_figures_pdf.py            # 生成 地磁场测量实验_图集.pdf
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
    ('图1_磁阻传感器_磁电转换特性_线性拟合.png',
     '图 1  磁阻传感器磁电转换特性：输出电压 U 随磁感应强度 B 的变化及线性拟合'),
    ('图2_磁阻传感器_方向特性_余弦拟合.png',
     '图 2  磁阻传感器方向特性：输出电压 U 随夹角 α 的变化及余弦拟合'),
    ('图3_亥姆霍兹线圈_轴向磁场分布.png',
     '图 3  亥姆霍兹线圈轴向磁场分布：实测曲线与理论曲线'),
    ('图4_亥姆霍兹线圈_空间磁场分布.png',
     '图 4  亥姆霍兹线圈空间磁场分布：中平面三维曲面图'),
]

OUT_PDF = '地磁场测量实验_图集.pdf'
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
