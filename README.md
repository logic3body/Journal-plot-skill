# Journal Plot

A Claude Code skill for generating publication-ready matplotlib figures that meet international journal submission standards.

## Overview

`journal-plot` is a custom skill for Claude Code that helps researchers create Python/matplotlib visualizations compliant with major scientific publishers (Nature, Elsevier, Springer, IEEE, PLOS, etc.).

When activated, it generates copy-paste-ready code with proper font settings, dimensions, color modes, and file formats for journal submissions.

## Features

- **Smart variable analysis**: Parses your Python file (AST) to detect numpy arrays, shapes, and types
- **Proactive chart suggestions**: Analyzes your data and suggests 2-4 chart types with reasoning
- **Multi-panel recommendation**: Automatically suggests multi-panel figures when 3+ related arrays are detected
- **Axis label inference**: Maps variable names to quantity-unit labels (e.g., `velocity` → "Velocity (m/s)"); asks when uncertain
- **Multi-publisher support**: Settings for Nature, Elsevier, Springer, IEEE, PLOS ONE, Cell Press, Science, PNAS
- **Publication-quality defaults**: Arial font, 1200 dpi vector output, golden-ratio dimensions
- **Color-blind friendly**: Viridis/cividis palettes, warns about red-green only combinations
- **Self-explanatory figures**: Quantity-unit axis labels, error bar definitions, statistical annotations
- **Data file analysis**: Analyzes `.npz`, `.npy`, `.csv` files loaded in your script
- **Runtime error auto-fix**: Detects common errors and proposes fixes
- **File injection mode**: Adds plotting code directly to your existing scripts
- **Duplicate injection prevention**: Detects existing plotting functions before modifying files
- **Bilingual support**: Full Chinese/English trigger keywords and responses

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
| Cell Press | 600 | PDF, EPS | Arial |
| Science | 300 | TIFF, JPEG | Arial |
| PNAS | 300-600 | EPS, TIFF | Arial |
| Default | 1200 | PDF, EPS | Arial |

## Requirements

- Python 3.9+
- matplotlib 3.5+
- (optional) seaborn for statistical plots

```
pip install matplotlib seaborn
```
