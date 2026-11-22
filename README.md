# 大学物理实验报告

大学物理实验课程的数据处理、作图与实验报告图集，使用 Python / Jupyter 完成。

## 实验目录

| 实验 | 内容 | 成品 |
| --- | --- | --- |
| [偏振光学实验](偏振光学实验/) | 马吕斯定律、1/2 波片、1/4 波片 | [偏振光学实验_图集.pdf](偏振光学实验/偏振光学实验_图集.pdf) |
| 地磁场测量实验 | 待补充 | — |

## 偏振光学实验

原始数据、处理代码、输出图和 A4 打印图集都在 [`偏振光学实验/`](偏振光学实验/) 下。

### 实验内容

1. **马吕斯定律**（[马吕斯定律_数据处理与作图.ipynb](偏振光学实验/马吕斯定律_数据处理与作图.ipynb)）
   - 验证 $I = I_0\cos^2\alpha$
   - 将 $I/I_0$ 对 $\cos^2\alpha$ 作线性拟合，检查斜率 $\approx 1$、截距 $\approx 0$、$R^2 \to 1$

2. **1/2 波片**（[半波片_数据处理与作图.ipynb](偏振光学实验/半波片_数据处理与作图.ipynb)）
   - 验证检偏器转角 $\beta$ 与波片转角 $\theta$ 满足 $\beta = 2\theta$

3. **1/4 波片**（[四分之一波片_极坐标作图.ipynb](偏振光学实验/四分之一波片_极坐标作图.ipynb)）
   - 用极坐标图判断偏振态：线偏振光经 1/4 波片后，45° 入射得到圆偏振光，20° 入射得到椭圆偏振光

### 输出文件

- `图*.png`：各实验的线性拟合图、折线图与极坐标图
- [偏振光学实验_图集.pdf](偏振光学实验/偏振光学实验_图集.pdf)：A4 打印版，每页两张图并附图注，可直接打印
- [make_figures_pdf.py](偏振光学实验/make_figures_pdf.py)：把 PNG 重新排版生成图集 PDF；增删图或修改图注只需编辑其中的 `FIGURES` 列表

## 地磁场测量实验

尚未开始，目录暂为空（由 `.gitkeep` 占位）。

## 运行环境

- Python 3.11
- numpy、pandas、matplotlib、Pillow
- Jupyter Notebook（打开 `.ipynb` 文件）

```bash
pip install numpy pandas matplotlib pillow jupyter
```

重新生成图集：

```bash
cd 偏振光学实验
python make_figures_pdf.py             # 生成 偏振光学实验_图集.pdf
python make_figures_pdf.py --preview   # 同时输出每页 PNG 预览
```

## 说明

- 所有图均由 notebook 中的代码生成，图集 PDF 由 `make_figures_pdf.py` 排版。修改时请改 notebook 或脚本，不建议手工编辑图片。
- 数据为实验现场原始记录，处理过程与拟合结果见各 notebook。
