# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
## Git 提交规则

- commit message 中禁止包含任何 `Co-Authored-By` 署名（包括但不限于 Claude、Anthropic、noreply@anthropic.com 等任何 AI 相关署名）

- 所有提交仅保留用户本人的 git 作者信息（`用户名 <邮箱>`）

- 创建 PR 时同样不添加任何 AI 合作者信息
## Project Overview

This is a **Claude Code skill** for generating publication-ready matplotlib figures for international journals. The skill is invoked with `/journal-plot` and supports both English and Chinese trigger keywords.

## Quick Start

```bash
# Run the demo script
python quick_start.py

# Or manually:
python demo_data.py                    # generates data (plotting disabled)
# Edit demo_data.py: set PLOT_FIGURE = True
python demo_data.py                     # generates figures
```

## Architecture

- `.claude/skills/journal-plot/SKILL.md` - Skill definition file containing trigger keywords, journal specifications, and plotting code templates
- `demo_data.py` - Sample data generation script demonstrating conditional plotting injection
- `quick_start.py` - Interactive demo script

## Skill Behavior

When triggered, the skill:
1. Reads the user's existing Python file
2. Injects `PLOT_FIGURE` flag and `plot_journal_figure()` function at the end
3. Uses `if PLOT_FIGURE:` to wrap plotting code (disabled by default)
4. Reuses existing variables (x, y, etc.) from the user's file

## Supported Journals

| Publisher | DPI | Format | Font |
|-----------|-----|--------|------|
| IEEE | 300 | EPS, TIFF | Times New Roman |
| Nature | 300 max | JPEG, TIFF | Arial |
| Elsevier | 1000 | EPS, TIFF | Arial/Helvetica |
| PLOS ONE | 900-1200 | TIFF, EPS | Arial |

## Trigger Keywords

English: "journal plot", "publication figure", "figure for submission", "EPS/PDF for submission"
Chinese: "期刊图表", "期刊图片", "发表级图片", "投稿图", "学术图表", "科研图表"

## Key Conventions

- Plotting code uses `PLOT_FIGURE = False` by default to avoid plots on every run
- Font fallback: Times New Roman (system), DejaVu Sans (fallback)
- Figure dimensions: 3.5" single column, 7" full page, height = width × 0.75 (golden ratio)
