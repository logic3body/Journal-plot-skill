---
name: journal-plot
description: Generate publication-ready matplotlib figures for international journals. Use when user asks for journal figures, submission-ready plots, scientific visualizations for Nature/Elsevier/Springer/IEEE/PLOS, or any figure intended for academic publication. Triggers on keywords like "publication figure", "journal plot", "figure for submission", "academic figure", "EPS/PDF for submission", or in Chinese: "期刊图表", "期刊图片", "发表级图片", "投稿图", "学术图表", "期刊投稿", "EPS/PDF投稿", "matplotlib图表", "科研图表". The skill reads the user's existing Python file and injects conditional plotting code that can be toggled on/off.
---

# Figure-Ready Skill

Generate Python/matplotlib code for figures that meet international journal submission standards.

## Core Capability

When the user describes a figure request, the skill follows this **Smart Analysis Flow**:

### New Flow: Variable Analysis → Suggestion → Generate

```
1. READ file content

2. ANALYZE variables (AST parsing):
   → Extract numpy arrays: names, inferred shapes, types
   → Identify scalar values and summary statistics
   → Report: "Found: x (100,), y (100,), mean_y (10,)"

3. IF user specified chart type explicitly ("scatter plot", "散点图"):
   → Skip suggestion step
   → Proceed to step 5
   ELSE:
   → PRESENT 2-4 chart options with reasoning (see Variable Analysis Mode)
   → ASK user to select: "Which chart type would you like?"
   → Wait for user response

4. CONFIRM journal if not specified:
   → "What is your target journal?" / "您打算投稿到哪个期刊？"

5. CHECK for existing `plot_journal_figure`:
   → EXISTS → Ask overwrite, replace body only if confirmed
   → NOT EXISTS → Proceed with injection

6. INJECT code:
   → Find appropriate import insertion point
   → Append conditional plotting block to end of file
   → Validate required variables exist

7. CONFIRM completion:
   → "Code injected. Set PLOT_FIGURE = True and run to generate figure."
```

### Key Injection Rules

| Situation | Action |
|-----------|--------|
| `plot_journal_figure` exists | Ask user, replace body only if confirmed |
| No `plot_journal_figure` + has def/class | Import before first def/class |
| No `def/class` + has `import numpy` | Import after numpy import |
| No imports at all | After shebang + docstring |
| Required variables missing | Error out, do not inject |
| User refuses overwrite | Inform about direct usage, exit |

**Key behaviors:**
- Use `Edit` or `Write` tools to modify the user's existing file
- Reuse variables already defined in the file (x, y, mean_y, etc.)
- Default to `PLOT_FIGURE = False` so running the script doesn't show plots unless explicitly enabled
- When user enables PLOT_FIGURE and runs the script, figure appears
- **NEW**: Analyze variables first, suggest chart types, then generate

## Variable Analysis Mode

When the user asks for plotting **without specifying chart type**, the skill enters Variable Analysis Mode.

### Step 1: Variable Detection (AST Parsing)

Parse the user's Python file using `ast` module to extract:

| Property | Detection Method | Example |
|----------|------------------|---------|
| Variable name | AST `Assign` nodes | `temperature = np.array([...])` → `temperature` |
| Type | Detect `np.array()`, `np.linspace()`, `np.random.normal()`, etc. | numpy.ndarray |
| Inferred shape | From constant args or `.shape` attribute | `(100,)`, `(50, 3)`, `(10, 10)` |

**Target patterns:**
```python
x = np.linspace(0, 10, 100)        # name='x', type='numpy.ndarray', shape=(100,)
y = np.sin(x)                      # name='y', type='numpy.ndarray', shape=(100,)
mean_y = np.mean(y)                # name='mean_y', type='scalar'
error = np.std(y) / np.sqrt(n)     # name='error', type='scalar'
```

### Step 2: Chart Type Inference

Based on detected variables and their properties:

| Condition | Inferred Chart Type | Reasoning |
|-----------|---------------------|----------|
| 1D array + name contains `time` | Line plot (time series) | Temporal data suits connected points |
| 2 arrays of same length | Scatter plot | Bivariate data, x-y relationship |
| Name contains `mean` + `std`/`error` | Error bar plot | Summary statistics with uncertainty |
| 2D square-ish array | Heatmap | Matrix data suits color grid |
| Name contains `count`/`freq`/`category` | Bar chart | Categorical/frequency data |

**Name-based keyword inference:**
```python
time_keywords = {'time', 't', 'timestamp', 'date', 'hour'}
heatmap_keywords = {'grid', 'spatial', 'map', 'latitude', 'longitude'}
bar_keywords = {'count', 'freq', 'category', 'label', 'group'}
error_keywords = {'mean', 'std', 'error', 'sem', 'uncertainty'}
```

### Step 3: Suggestion Presentation

Present 2-4 chart options as a numbered list:

**English:**
```
Based on your data, I detected:
- `x` (100 points, 1D array)
- `y` (100 points, 1D array)
- `mean_y` (10 points, 1D array)
- `std_y` (10 points, 1D array)

Suggested chart types:

| # | Chart Type | Best For | Reasoning |
|---|------------|----------|-----------|
| 1 | **Error bar plot** | Measurements with uncertainty | You have `mean_y` and `std_y`; error bars show variability |
| 2 | **Scatter plot** | Correlations | `x` and `y` are same length (100); ideal for x-y relationships |
| 3 | **Line plot** | Trends | Continuous data; good for showing `y` over `x` |

Which chart type would you like? Enter a number or describe your desired plot.
```

**中文:**
```
根据您的数据，我检测到：
- `x`（100个点，一维数组）
- `y`（100个点，一维数组）
- `mean_y`（10个点，一维数组）
- `std_y`（10个点，一维数组）

建议的图表类型：

| # | 图表类型 | 适用场景 | 原因 |
|---|----------|----------|------|
| 1 | **误差棒折线图** | 测量数据与不确定性 | 您有 `mean_y` 和 `std_y`；误差棒显示变异性 |
| 2 | **散点图** | 相关性 | `x` 和 `y` 长度相同（100点）；适合展示两者关系 |
| 3 | **折线图** | 趋势变化 | 连续数据；适合展示 `y` 随 `x` 的变化趋势 |

您想要哪种图表类型？输入编号或描述您想要的图表。
```

### Step 4: User Selection Handling

- **Number input (1, 2, 3)**: Use that chart type
- **Natural language**: Parse keywords (scatter/散点, line/折线, bar/柱状, error/误差)
- **No specific request**: Use first suggestion, confirm before proceeding

### Edge Cases

**No numpy variables found:**
```
I couldn't find any numpy arrays in your file. Please ensure your data is stored as:
- numpy arrays: `x = np.array([...])`
- numpy functions: `x = np.linspace(0, 10, 100)`

Or specify your desired chart type directly and I can generate code with sample data.
```

**Only scalars found:**
```
Your file contains only scalar values. For publication figures, you'll typically need:
- 1D arrays for line/scatter plots
- 2D arrays for heatmaps

Would you like me to generate code with sample data to demonstrate the expected structure?
```

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

### Example 4: Variable Analysis - Chinese user
**User**: 帮我添加绘图到 demo_data.py

**Skill**:
正在读取 demo_data.py...

在您的文件中检测到以下变量：
| 变量名 | 类型 | 形状 |
|--------|------|------|
| `x` | numpy.ndarray | (100,) |
| `y` | numpy.ndarray | (100,) |
| `mean_y` | numpy.ndarray | (10,) |
| `std_y` | numpy.ndarray | (10,) |

建议的图表类型：

| # | 图表类型 | 适用场景 | 原因 |
|---|----------|----------|------|
| 1 | **误差棒折线图** | 测量数据与不确定性 | 您有 `mean_y` 和 `std_y`；误差棒显示变异性 |
| 2 | **散点图** | 相关性 | `x` 和 `y` 长度相同（100点）；适合展示两者关系 |
| 3 | **折线图** | 趋势变化 | 连续数据；适合展示 `y` 随 `x` 的变化趋势 |

您想要哪种图表类型？输入编号或描述您想要的图表。

**User**: 1

**Skill**:
好的，将为您创建**误差棒折线图**。

请问您打算投稿到哪个期刊？（IEEE / Nature / Elsevier / Springer / PLOS ONE / 其他）

**User**: IEEE

**Skill**:
正在生成 IEEE 标准的误差棒折线图代码...
[Code injection with IEEE settings: 300 dpi, EPS, Times New Roman]

代码已注入。设置 `PLOT_FIGURE = True` 后运行即可生成图表。

### Example 5: Variable Analysis - English user
**User**: add plotting to my_file.py

**Skill**:
Reading my_file.py...

Found variables:
| Variable | Type | Shape |
|----------|------|-------|
| `time` | numpy.ndarray | (50,) |
| `velocity` | numpy.ndarray | (50,) |
| `velocity_std` | numpy.ndarray | (50,) |

Based on your data, here are suggested chart types:

| # | Chart Type | Best For | Reasoning |
|---|------------|----------|-----------|
| 1 | **Error bar plot** | Measurements with uncertainty | You have `velocity_std`; error bars show variability |
| 2 | **Line plot** | Trends over time | `time` in variable name suggests time series |
| 3 | **Scatter plot** | Correlations | Two paired arrays of same length |

Which would you like? Enter number or describe your desired plot.

**User**: error bar plot please

**Skill**:
I'll create an **error bar plot** for you.

Target journal? (IEEE / Nature / Elsevier / Springer / PLOS ONE)

**User**: PLOS ONE

**Skill**:
Generating PLOS ONE error bar plot...
[Code injection with PLOS ONE settings: 900-1200 dpi, TIFF/EPS, Arial]

Code injected. Set `PLOT_FIGURE = True` and run to generate figure.

### Example 6: Direct specification (skip analysis)
**User**: 在 demo_data.py 中添加 IEEE 标准的散点图

**Skill**:
Reading demo_data.py...

Found variables: `x` (100,), `y` (100,)

您指定了散点图和 IEEE 标准，我将直接生成代码。
[Skips suggestion step, goes directly to code generation with IEEE settings]

## Interaction Guidelines

### New Variable Analysis Flow

1. **Detect variables first**: When user asks for plotting without specifics, parse the file and report what was found
   - "我在文件中检测到以下变量：`x` (100点), `y` (100点), `mean_y` (10点)"
   - "I found these variables in your file: `x` (100 pts), `y` (100 pts), `mean_y` (10 pts)"

2. **Present suggestions proactively**: Offer 2-4 chart types with brief reasoning
   - Use numbered list format for easy selection
   - Include reasoning based on variable names and shapes

3. **Handle selection**:
   - Number input → use that chart type
   - Natural language → interpret keywords (scatter/散点, line/折线, bar/柱状, error/误差)
   - No specific request → use first suggestion, confirm before proceeding

4. **Confirm before injection**: After selection, briefly confirm the plan
   - "我将为您创建误差棒折线图，使用IEEE格式设置，可以吗？"
   - "I'll create an error bar line plot with IEEE settings. Proceed?"

5. **Journal check**: Ask if not specified
   - "您打算投稿到哪个期刊？" / "What is your target journal?"

### Legacy Direct Injection (unchanged)

When user **specifies** chart type explicitly:
- "为 IEEE 创建带误差棒的散点图"
- "Create a scatter plot with error bars for Nature"

→ Skip suggestion step, go directly to code generation

### Original Guidelines (apply throughout)

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