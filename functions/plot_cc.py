"""Cross-correlation plot matching MATLAB plotCC.m."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def plot_cc(cc_result, run_name, plot_options):
    """Create cross-correlation plot matching MATLAB plotCC.m output."""
    wide = plot_options.get('wide', 6.5)
    tall = plot_options.get('tall_cc', 2.7)
    font_name = plot_options.get('font_name', 'Arial')
    font_size_title = plot_options.get('font_size_title', 11)
    font_size_axes = plot_options.get('font_size_axes', 11)
    font_size_ticks = plot_options.get('font_size_ticks', 10)

    # MATLAB ticks: every 5 from -65 to 65 (MATLAB plotCC.m exact)
    x_ticks = list(range(-65, 66, 5))
    y_ticks = [-0.5, -0.3, -0.1, 0, 0.1, 0.3, 0.5]

    fig = plt.figure(figsize=(wide, tall))
    fig.patch.set_facecolor('white')
    ax = fig.add_subplot(111)
    ax.set_facecolor('white')

    # MATLAB colors: k (XY), c (XZ), m (YZ)
    colors = ['k', 'c', 'm']
    legend_entries = []

    for k, pair in enumerate(cc_result['pairs']):
        color = colors[k % len(colors)]
        ax.plot(pair['lag_time'], pair['corr'], color, linewidth=0.5)
        legend_entries.append(pair['axes'])

    # Threshold lines at +/- 0.3 (red dashed)
    if cc_result['pairs']:
        lag = cc_result['pairs'][0]['lag_time']
        ax.plot([lag[0], lag[-1]], [0.3, 0.3], 'r--', linewidth=1.0)
        ax.plot([lag[0], lag[-1]], [-0.3, -0.3], 'r--', linewidth=1.0)

    ax.grid(True, which='major', color='lightgray', linewidth=0.4)
    ax.set_ylim([-0.5, 0.5])
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)

    title = f"Cross Correlation ({run_name.replace('_', ' ')})"
    ax.set_title(title, fontname=font_name, fontsize=font_size_title,
                 fontweight='bold')
    ax.legend(legend_entries, loc='upper left', fontsize=7)

    max_cc = cc_result['max_cc']
    xlabel_text = (f'{"":>46s}Time Lag (s) '
                   f'{"":>11s}Max. Corr. = {max_cc:.2f}')
    ax.set_xlabel(xlabel_text, fontname=font_name, fontsize=font_size_axes,
                   fontweight='bold')
    ax.set_ylabel('Correlation', fontname=font_name, fontsize=font_size_axes,
                   fontweight='bold')

    # Tick direction: inward on all 4 sides, full box
    ax.tick_params(axis='both', which='both', direction='in',
                   top=True, right=True, length=4, width=0.5,
                   labelsize=font_size_ticks)
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)

    fig.subplots_adjust(left=0.130, right=0.904, top=0.919, bottom=0.160)
    return fig
