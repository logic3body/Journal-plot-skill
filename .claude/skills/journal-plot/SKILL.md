---
name: journal-plot
description: Generate publication-ready matplotlib figures for international journals. Use when user asks for journal figures, submission-ready plots, scientific visualizations for Nature/Elsevier/Springer/IEEE/PLOS, or any figure intended for academic publication. Triggers on keywords like "publication figure", "journal plot", "figure for submission", "academic figure", "EPS/PDF for submission", or in Chinese: "期刊图表", "期刊图片", "发表级图片", "投稿图", "学术图表", "期刊投稿", "EPS/PDF投稿", "matplotlib图表", "科研图表". The skill reads the user's existing Python file and injects conditional plotting code that can be toggled on/off.
---

# Figure-Ready Skill

Generate Python/matplotlib code for figures that meet international journal submission standards.

## Core Capability

When the user describes a figure request, the skill should:

1. **Read the user's existing Python file** (e.g., demo_calculation.py)
2. **Analyze the file structure** - identify existing data variables (x, y, arrays, etc.)
3. **Inject journal-grade plotting code** as a conditional branch at the end of the file:
   - Add a `PLOT_FIGURE = False` flag (set to `True` to enable)
   - Create a `plot_journal_figure()` function using existing data variables
   - Wrap in an `if PLOT_FIGURE:` block so plotting is optional
4. **Preserve all original computation logic** - never modify existing code

Example injection structure:
```python
# === Optional Journal-Grade Plotting ===
PLOT_FIGURE = False  # Set to True to enable plotting

def plot_journal_figure(x, y, publisher='IEEE'):
    """Generate publication-ready figure"""
    # ... matplotlib code with journal settings ...
    pass

if PLOT_FIGURE:
    # Uses existing data from the file
    plot_journal_figure(x, y, publisher='IEEE')
```

**Key behaviors:**
- Use `Edit` or `Write` tools to modify the user's existing file
- Reuse variables already defined in the file (x, y, mean_y, etc.)
- Default to `PLOT_FIGURE = False` so running the script doesn't show plots unless explicitly enabled
- When user enables PLOT_FIGURE and runs the script, figure appears

## When to Trigger

Use this skill when the user mentions:
- "publication figure", "journal figure", "figure for submission", "academic figure"
- "Nature/Elsevier/Springer/IEEE/PLOS figure"
- "EPS/PDF/TIFF for journal submission"
- "ready-to-submit plot"
- Wants to create a scientific figure that will be submitted to a journal

**File editing mode** (user mentions existing file):
- "帮我添加绘图到 demo_calculation.py"
- "在 script.py 中添加 IEEE 标准的图表"
- "add plotting to my existing file"

Chinese triggers / 中文触发词：
- "期刊图表", "期刊图片", "发表级图片", "投稿图"
- "学术图表", "期刊投稿", "科研图表"
- "Nature/Elsevier/Springer/IEEE/PLOS 图表"
- "EPS/PDF/TIFF 投稿格式"
- "帮我添加绘图", "在文件中添加图表"

## Journal Format Specifications

### Publisher Lookup Table

| Publisher | Line Art DPI | Color Mode | Accepted Formats | Font |
|-----------|--------------|-------------|-------------------|------|
| Nature | 300 max | RGB | JPEG, TIFF | Arial |
| Elsevier | 1000 | RGB/CMYK | EPS, TIFF | Arial/Helvetica |
| Springer | 300-600 | RGB | EPS, PDF, TIFF | Arial |
| IEEE | 300 | RGB | EPS, TIFF | Times New Roman |
| PLOS ONE | 900-1200 | RGB | TIFF, EPS | Arial |
| Cell Press | 600 | RGB | PDF, EPS | Arial |
| Science | 300 | RGB | TIFF, JPEG | Arial |
| PNAS | 300-600 | RGB | EPS, TIFF | Arial |
| Default (generic) | 1200 | RGB | PDF, EPS | Arial |

When user specifies a publisher, consult this table and override the default settings accordingly.

## Visual Style Rules

### Figure Dimensions
- **Single column**: width = 3.5 inches (≈89 mm)
- **Full page width**: width = 7 inches (≈178 mm)
- **Height**: width × 0.75 (golden ratio) or user-specified
- Set `figsize` in inches at creation

### Font Settings
```python
plt.rcParams.update({
    'font.family': 'Arial',
    'font.size': 8,
    'axes.labelsize': 9,
    'axes.titlesize': 10,
    'legend.fontsize': 8,
    'xtick.labelsize': 7,
    'ytick.labelsize': 7,
    'lines.linewidth': 1,
    'axes.linewidth': 0.8,
})
```
- Title and axis label size: 8–10 pt
- Tick label size: 7–8 pt
- All text must remain editable in output (never rasterize text)

### Color Mode
- Default: RGB for on-screen review
- Note: final submission may require CMYK conversion
- Use color-blind friendly palettes: `viridis`, `cividis`, `ColorBrewer Set2`
- Warn against red-green only combinations

### Background & Borders
- No decorative backgrounds
- Remove top/right spines (standard seaborn style)
- Grid lines: only if strictly necessary, light grey (`0.85`), behind data

### Legends
- Inside or outside axes, clearly readable
- No border box unless required
- Legend frame off or very thin line

### Subplot Labelling
- Use lowercase bold letters: **(a)**, **(b)** placed top-left of each panel
- Use `fig.text()` or `axes.set_title(..., loc='left')`

## Data Presentation Rules

### Axis Labels
- Every axis must have label with quantity-unit format: `Time (s)`, `Velocity (m/s)`
- Never use undefined abbreviations

### Error Bars
- Define and explain: "Mean ± SEM, n=5"
- Use consistent error representation across all panels

### Statistics Display
- Use standard notation: `***`, `**`, `n.s.` with explanation in caption
- Provide legend or annotation explaining symbols

### Self-Explanatory Requirement
- Figure must be understandable without reading the main text
- Include all necessary identifiers in the plot
- Add descriptive title if needed

### Chart Types to Avoid
- No 3D bar charts
- No exploded pie charts
- No "chartjunk" (unnecessary decorative elements)

## Code Generation Skeleton

```python
import matplotlib.pyplot as plt
import numpy as np

# === Global settings for publication quality ===
plt.rcParams.update({
    'font.family': 'Arial',
    'font.size': 8,
    'axes.labelsize': 9,
    'axes.titlesize': 10,
    'legend.fontsize': 8,
    'xtick.labelsize': 7,
    'ytick.labelsize': 7,
    'lines.linewidth': 1,
    'axes.linewidth': 0.8,
    'savefig.dpi': 1200,
    'savefig.format': 'pdf',
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
    'figure.constrained_layout.use': True,
})

# User data goes here...
# fig, ax = plt.subplots(figsize=(7, 5.25))  # full-page width
# OR: fig, axes = plt.subplots(1, 2, figsize=(7, 3.5))  # single-column multi-panel

# plotting commands...
# ax.set_xlabel('Time (s)')
# ax.set_ylabel('Velocity (m/s)')
# ax.set_title('(a)', loc='left', fontweight='bold', pad=10)

# ... more plotting ...

plt.savefig('figure_1.pdf')
plt.show()
```

### Format-Specific Save Settings

**Line Art (vector):**
```python
plt.savefig('figure_1.pdf', format='pdf', dpi=1200, bbox_inches='tight', pad_inches=0.05)
```

**Photographs/Microscopy (raster):**
```python
plt.savefig('figure_1.tiff', format='tiff', dpi=300, bbox_inches='tight')
```

**Combination charts:**
```python
plt.savefig('figure_1.pdf', format='pdf', dpi=1200, bbox_inches='tight')
# With embedded raster ≥600 dpi
```

## Decision Tree

1. **Does user mention an existing file?**
   - Yes → Read the file, identify data variables, inject conditional plotting code
   - No → Generate standalone code block as before

2. **Is this line art or photograph?**
   - Line art (plots, charts, graphs) → use vector format (PDF/EPS)
   - Photograph/microscopy → use TIFF, CMYK, ≥300 dpi

3. **Does user specify a journal?**
   - Yes → consult Publisher Lookup Table, override default settings
   - No → use generic defaults (PDF, 1200 dpi, RGB)

4. **Does user have existing matplotlib code?**
   - Yes → refactor to meet standards (font, size, format, spine removal)
   - No → generate from skeleton

5. **What type of plot?**
   - Scatter/bar/line → standard 2D plot
   - Statistical (box, violin) → seaborn with error annotations
   - Time series → appropriate time formatting on x-axis

## Usage Examples

### Example 1: Simple scatter plot
User: "Create a scatter plot showing temperature vs. pressure with error bars for a PLOS ONE paper"

Generated code uses:
- Single column width (3.5 inches) or full page (7 inches)
- Arial font, 8pt base size
- Error bars with "Mean ± SEM, n=X" notation
- PLOS ONE settings: 900-1200 dpi, TIFF/EPS, Arial
- Axis labels in quantity-unit format

### Example 2: Multi-panel figure
User: "Make a two-panel figure for Elsevier with (a) bar chart and (b) line plot"

Generated code:
- Two axes side by side
- Each panel labelled (a), (b) top-left
- Elsevier overrides: 1000 dpi, EPS/TIFF, Arial/Helvetica
- Vector format

### Example 3: Refactor existing code
User: "Take my existing matplotlib code and adjust it for Nature"

Generated code:
- Apply Nature settings: 300 dpi max, RGB, JPEG or TIFF
- Keep user's plot structure but update font/size/format

## Interaction Guidelines

1. **Always ask**: "What is your target journal?" if not specified — allows precision
   - 也可以用中文问："您打算投稿到哪个期刊？"
2. **Confirm format**: "Should this be vector (PDF/EPS) or raster (TIFF)?" for ambiguous cases
   - 中文确认："需要矢量格式（PDF/EPS）还是光栅格式（TIFF）？"
3. **Warn about color-blindness**: If user requests red-green palette, suggest alternative
   - 色盲友好提醒：如用户要求红绿色组合，建议使用 viridis/cividis 等色盲友好色板
4. **Offer caption suggestion**: After generating code, provide a figure caption template
   - 提供图表说明建议：生成代码后，提供英文图表说明模板
5. **Handle 3D requests**: If user asks for 3D plot, explain why 2D is preferred for publication and offer 2D alternative
   - 处理3D请求：说明为什么期刊投稿偏好2D，并提供2D替代方案

## Limitations

- Raster image export (TIFF at specific DPI) requires Pillow: `pip install Pillow`
- CMYK conversion must be done externally (recommend Inkscape or Adobe tools)
- Seaborn must be installed: `pip install seaborn`
- Animations not supported (static figures only)

## Output Summary

After generating code, provide:
1. Copy-paste ready Python code block
2. Target journal settings applied
3. Recommended file format and naming
4. Suggested figure caption (English)