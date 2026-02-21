"""Cross-correlation plot."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def plot_cc(cc_result, run_name, plot_options):
    """Create cross-correlation plot.

    Parameters
    ----------
    cc_result : dict
        Output from calc_cc().
    run_name : str
    plot_options : dict

    Returns
    -------
    matplotlib.figure.Figure
    """
    wide = plot_options.get('wide', 6.5)
    tall = plot_options.get('tall', 2.7)
    font_name = plot_options.get('font_name', 'Arial')
    font_size_title = plot_options.get('font_size_title', 11)
    font_size_axes = plot_options.get('font_size_axes', 11)
    font_size_ticks = plot_options.get('font_size_ticks', 10)

    y_ticks = [-0.5, -0.3, -0.1, 0, 0.1, 0.3, 0.5]

    fig, ax = plt.subplots(figsize=(wide, tall))

    colors = ['k', 'c', 'm']
    legend_entries = []

    for k, pair in enumerate(cc_result['pairs']):
        color = colors[k % len(colors)]
        ax.plot(pair['lag_time'], pair['corr'], color, linewidth=0.5)
        legend_entries.append(pair['axes'])

    # Threshold lines at +/- 0.3
    if cc_result['pairs']:
        lag = cc_result['pairs'][0]['lag_time']
        ax.plot([lag[0], lag[-1]], [0.3, 0.3], 'r--', linewidth=0.5)
        ax.plot([lag[0], lag[-1]], [-0.3, -0.3], 'r--', linewidth=0.5)

    ax.grid(True)
    ax.set_ylim([-0.5, 0.5])
    ax.set_yticks(y_ticks)
    ax.tick_params(labelsize=font_size_ticks)

    title = f"Cross Correlation ({run_name.replace('_', ' ')})"
    ax.set_title(title, fontname=font_name, fontsize=font_size_title)
    ax.legend(legend_entries, loc='upper left', fontsize=7)

    max_cc = cc_result['max_cc']
    xlabel = f'Time Lag (s)                              Max. Corr. = {max_cc:.2f}'
    ax.set_xlabel(xlabel, fontname=font_name, fontsize=font_size_axes)
    ax.set_ylabel('Correlation', fontname=font_name, fontsize=font_size_axes)

    fig.tight_layout()
    return fig
