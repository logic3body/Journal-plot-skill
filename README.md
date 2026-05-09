# Journal Plot

A Claude Code skill for generating publication-ready matplotlib figures that meet international journal submission standards.

## Overview

`journal-plot` is a custom skill for Claude Code that helps researchers create Python/matplotlib visualizations compliant with major scientific publishers (Nature, Elsevier, Springer, IEEE, PLOS, etc.).

When activated, it generates copy-paste-ready code with proper font settings, dimensions, color modes, and file formats for journal submissions.

## Installation

Copy the `.claude` folder into your project root:

```
your-project/
└── .claude/
    └── skills/
        └── journal-plot/
            └── SKILL.md
```

Then invoke with `/journal-plot` in Claude Code.

## Features

- **Multi-publisher support**: Settings for Nature, Elsevier, Springer, IEEE, PLOS ONE, Cell Press, Science, PNAS
- **Publication-quality defaults**: Arial font, 1200 dpi vector output, golden-ratio dimensions
- **Color-blind friendly**: Viridis/cividis palettes, warns about red-green only combinations
- **Self-explanatory figures**: Quantity-unit axis labels, error bar definitions, statistical annotations
- **Code skeleton**: Ready-to-run template with global rcParams
- **File injection mode**: Adds plotting code directly to your existing scripts

## Usage

### Quick Start

1. **Run the demo:**
   ```bash
   python quick_start.py
   ```

2. **Or manually:**
   ```bash
   # Generate data (plotting disabled by default)
   python demo_data.py

   # Enable plotting in demo_data.py:
   # PLOT_FIGURE = True

   # Run again to generate figures
   python demo_data.py
   ```

### Invoking the Skill

```
/journal-plot
```

Then describe your figure, e.g.:
- "Create a scatter plot of temperature vs pressure with error bars for Elsevier"
- "Make a two-panel figure for Nature with (a) bar chart and (b) line plot"
- "Generate a time-series plot for PLOS ONE"
- "帮我添加 IEEE 标准的误差棒折线图到 demo_data.py"

### File Injection Mode

When you mention an existing file, the skill will inject conditional plotting code:

```
/journal-plot 帮我添加绘图到 my_script.py
```

The skill will:
1. Read your existing Python file
2. Inject `PLOT_FIGURE` flag and `plot_journal_figure()` function
3. Set `PLOT_FIGURE = False` by default (no plot on run)
4. Set `PLOT_FIGURE = True` when you want to generate figures

## Example Output

```python
# === Optional Journal-Grade Plotting ===
PLOT_FIGURE = False  # Set to True to enable plotting

def plot_journal_figure(x, y, publisher='IEEE'):
    """Generate publication-ready figure"""
    import matplotlib.pyplot as plt

    # IEEE publication settings
    plt.rcParams.update({
        'font.family': 'Times New Roman',
        'font.size': 8,
        'axes.labelsize': 9,
        'savefig.dpi': 300,
        'savefig.format': 'eps',
    })

    fig, ax = plt.subplots(figsize=(3.5, 2.625))
    ax.errorbar(x, y, yerr=0.1, fmt='o-')
    plt.savefig('figure_1.eps')
    plt.show()

if PLOT_FIGURE:
    plot_journal_figure(x, y)
```

## Supported Publishers

| Publisher | Line Art DPI | Format | Font |
|-----------|-------------|--------|------|
| Nature | 300 max | JPEG, TIFF | Arial |
| Elsevier | 1000 | EPS, TIFF | Arial/Helvetica |
| IEEE | 300 | EPS, TIFF | Times New Roman |
| PLOS ONE | 900-1200 | TIFF, EPS | Arial |
| Default | 1200 | PDF, EPS | Arial |

## Requirements

- Python 3.9+
- matplotlib 3.5+
- (optional) seaborn for statistical plots

```
pip install matplotlib seaborn
```

---

# Journal Plot（期刊图表）

用于生成符合国际期刊投稿标准的可发表级别 matplotlib 图表的 Claude Code 技能。

## 概述

`journal-plot` 是 Claude Code 的自定义技能，帮助研究人员创建符合主流科研出版机构（Nature、Elsevier、Springer、IEEE、PLOS 等）规范的 Python/matplotlib 可视化图表。

启用后，它会生成可直接复制使用的代码，包含正确的字体设置、尺寸、颜色模式和文件格式，适用于期刊投稿。

## 功能特点

- **多出版机构支持**：Nature、Elsevier、Springer、IEEE、PLOS ONE、Cell Press、Science、PNAS 的设置
- **发表级默认配置**：Arial 字体、1200 dpi 矢量输出、黄金比例尺寸
- **色盲友好**：Viridis/cividis 色板，对红绿组合发出警告
- **自解释图表**：带量纲的坐标轴标签、误差棒定义、统计注释
- **代码骨架**：包含全局 rcParams 的可直接运行的模板
- **文件注入模式**：可将绘图代码直接添加到现有脚本中

## 使用方法

### 快速开始

1. **运行演示：**
   ```bash
   python quick_start.py
   ```

2. **或手动操作：**
   ```bash
   # 生成数据（默认绘图关闭）
   python demo_data.py

   # 在 demo_data.py 中启用绘图：
   # PLOT_FIGURE = True

   # 再次运行以生成图表
   python demo_data.py
   ```

### 调用技能

```
/journal-plot
```

然后描述你的图表需求，例如：
- "为 Elsevier 创建一张温度 vs 压强的带误差棒的散点图"
- "为 Nature 创建一张双面板图，包含 (a) 柱状图和 (b) 折线图"
- "为 PLOS ONE 生成一张时间序列图"
- "帮我添加 IEEE 标准的误差棒折线图到 demo_data.py"

### 文件注入模式

当你提到现有文件名时，技能会将绘图代码直接注入文件中：

```
/journal-plot 帮我添加绘图到 my_script.py
```

技能会：
1. 读取你现有的 Python 文件
2. 注入 `PLOT_FIGURE` 标志和 `plot_journal_figure()` 函数
3. 默认设置 `PLOT_FIGURE = False`（运行时不绘图）
4. 当你需要生成图表时设置 `PLOT_FIGURE = True`

## 示例输出

```python
# === 可选期刊级绘图 ===
PLOT_FIGURE = False  # 设置为 True 启用绘图

def plot_journal_figure(x, y, publisher='IEEE'):
    """生成符合期刊标准的图表"""
    import matplotlib.pyplot as plt

    # IEEE 出版设置
    plt.rcParams.update({
        'font.family': 'Times New Roman',
        'font.size': 8,
        'axes.labelsize': 9,
        'savefig.dpi': 300,
        'savefig.format': 'eps',
    })

    fig, ax = plt.subplots(figsize=(3.5, 2.625))
    ax.errorbar(x, y, yerr=0.1, fmt='o-')
    plt.savefig('figure_1.eps')
    plt.show()

if PLOT_FIGURE:
    plot_journal_figure(x, y)
```

## 支持的出版机构

| 出版机构 | 线图 DPI | 格式 | 字体 |
|-----------|-------------|--------|------|
| Nature | 300 最大 | JPEG, TIFF | Arial |
| Elsevier | 1000 | EPS, TIFF | Arial/Helvetica |
| IEEE | 300 | EPS, TIFF | Times New Roman |
| PLOS ONE | 900-1200 | TIFF, EPS | Arial |
| 默认 | 1200 | PDF, EPS | Arial |

## 依赖要求

- Python 3.9+
- matplotlib 3.5+
- （可选）seaborn 用于统计图表

```
pip install matplotlib seaborn
```
