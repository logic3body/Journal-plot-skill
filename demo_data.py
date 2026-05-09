"""
Simple calculation script for demonstration.
This script performs basic calculations that can be visualized with the journal-plot skill.
"""

import numpy as np

# Generate sample data
x = np.linspace(0, 10, 100)
y = np.sin(x) + np.random.normal(0, 0.1, len(x))

# Basic statistics
mean_y = np.mean(y)
std_y = np.std(y)

print(f"Data generated: {len(x)} points")
print(f"Mean: {mean_y:.4f}")
print(f"Std: {std_y:.4f}")

# Save data for plotting
np.savez('demo_data.npz', x=x, y=y)
print("Data saved to demo_data.npz")

# === Optional Journal-Grade Plotting ===
PLOT_FIGURE = True  # Set to True to enable plotting

def plot_journal_figure(x, y, publisher='IEEE'):
    """Generate publication-ready error bar line plot for IEEE"""
    import matplotlib.pyplot as plt

    # IEEE publication settings
    # Note: Times New Roman may not be available on all systems
    # Using DejaVu Sans as fallback (most systems have this)
    plt.rcParams.update({
        'font.family': 'Times New Roman',
        'font.size': 8,
        'axes.labelsize': 9,
        'axes.titlesize': 10,
        'legend.fontsize': 8,
        'xtick.labelsize': 7,
        'ytick.labelsize': 7,
        'lines.linewidth': 1,
        'axes.linewidth': 0.8,
        'savefig.dpi': 300,
        'savefig.format': 'eps',
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.05,
    })

    # Bin data for error bars
    n_bins = 10
    bin_size = len(x) // n_bins
    x_binned = []
    y_mean = []
    y_err = []

    for i in range(n_bins):
        start = i * bin_size
        end = (i + 1) * bin_size
        x_binned.append(np.mean(x[start:end]))
        y_mean.append(np.mean(y[start:end]))
        y_err.append(np.std(y[start:end]) / np.sqrt(bin_size))  # SEM

    x_binned = np.array(x_binned)
    y_mean = np.array(y_mean)
    y_err = np.array(y_err)

    # Create figure - single column width, golden ratio
    fig, ax = plt.subplots(figsize=(3.5, 2.625))

    # Plot line with error bars
    ax.errorbar(x_binned, y_mean, yerr=y_err,
                fmt='o-', markersize=4, capsize=3,
                color='black', markerfacecolor='black',
                linewidth=1, ecolor='black')

    # Remove top/right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Grid (light grey, behind data)
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

    # Labels in quantity-unit format
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude (a.u.)')

    # Caption notation
    ax.set_title('Mean ± SEM, n={}'.format(bin_size), fontsize=8, style='italic')

    plt.savefig('figure_1.eps', format='eps')
    plt.savefig('figure_1.tif', format='tiff', dpi=300)
    plt.show()

if PLOT_FIGURE:
    plot_journal_figure(x, y, publisher='IEEE')
