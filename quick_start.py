#!/usr/bin/env python3
"""
Quick Start Script for Journal-Plot Skill

This script demonstrates how to use the journal-plot skill to add
publication-ready figures to your existing calculation scripts.

Usage:
    1. Generate data: python quick_start.py
    2. Enable plotting: Set PLOT_FIGURE = True in demo_data.py
    3. Run again: python demo_data.py
"""

import subprocess
import sys

def print_banner():
    print("=" * 60)
    print("Journal-Plot Quick Start")
    print("=" * 60)
    print()

def main():
    print_banner()
    print("This script demonstrates the journal-plot skill workflow.\n")

    # Step 1: Show demo_data.py content
    print("[Step 1] Checking demo_data.py...")
    print("-" * 40)
    with open('demo_data.py', 'r') as f:
        content = f.read()
        # Show first 20 lines
        lines = content.split('\n')[:20]
        for i, line in enumerate(lines, 1):
            print(f"{i:2d}: {line}")
        print("   ...")
    print()

    # Step 2: Show how plotting was added
    print("[Step 2] Plotting code was injected after line 22:")
    print("-" * 40)
    lines = content.split('\n')[21:35]
    for i, line in enumerate(lines, 22):
        print(f"{i:2d}: {line}")
    print()

    # Step 3: Instructions
    print("[Step 3] To enable plotting:")
    print("-" * 40)
    print("    1. Open demo_data.py")
    print("    2. Find: PLOT_FIGURE = False")
    print("    3. Change to: PLOT_FIGURE = True")
    print("    4. Run: python demo_data.py")
    print()

    # Step 4: Show journal settings
    print("[Step 4] IEEE Publication Settings Applied:")
    print("-" * 40)
    print("    - Font: Times New Roman (or system fallback)")
    print("    - DPI: 300")
    print("    - Format: EPS, TIFF")
    print("    - Figure size: 3.5 x 2.625 inches (single column)")
    print()

    # Run demo_data.py
    print("[Step 5] Running demo_data.py with PLOT_FIGURE=True...")
    print("-" * 40)

    # Temporarily enable plotting
    with open('demo_data.py', 'r') as f:
        original = f.read()

    modified = original.replace('PLOT_FIGURE = False', 'PLOT_FIGURE = True')

    with open('demo_data.py', 'w') as f:
        f.write(modified)

    try:
        result = subprocess.run([sys.executable, 'demo_data.py'],
                              capture_output=True, text=True, timeout=30)
        print(result.stdout)
        if result.stderr:
            # Filter out common warnings
            stderr_lines = result.stderr.split('\n')
            important = [l for l in stderr_lines
                        if 'Font family' not in l
                        and 'qt.qpa.plugin' not in l
                        and 'findfont' not in l
                        and l.strip()]
            if important:
                print("\nWarnings:")
                for l in important[:5]:
                    print(f"  {l}")
    finally:
        # Restore original
        with open('demo_data.py', 'w') as f:
            f.write(original)

    print()
    print("=" * 60)
    print("Generated files:")
    print("    - figure_1.eps")
    print("    - figure_1.tif")
    print("=" * 60)

if __name__ == '__main__':
    main()
