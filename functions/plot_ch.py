"""Coherence plot."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def plot_ch(ch_result, run_name, plot_options):
    """Create magnitude squared coherence plot.

    Parameters
    ----------
    ch_result : dict
        Output from calc_ch().
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

    ticks = [1.3, 10, 20, 33.3]
    y_ticks = [0.0, 0.25, 0.5, 0.75, 1.0]

    fig, ax = plt.subplots(figsize=(wide, tall))
    ax.set_xscale('log')
    ax.set_xticks(ticks)
    ax.set_xticklabels([str(t) for t in ticks])
    ax.minorticks_on()
    ax.grid(True, which='both', linewidth=0.5)
    ax.tick_params(labelsize=font_size_ticks)

    colors = ['k', 'c', 'm']
    legend_entries = []

    for k, pair in enumerate(ch_result['pairs']):
        color = colors[k % len(colors)]
        ax.semilogx(pair['frequencies'], pair['coherence'], color, linewidth=0.75)
        legend_entries.append(pair['axes'])

    # Threshold at 0.5
    if ch_result['pairs']:
        f = ch_result['pairs'][0]['frequencies']
        ax.semilogx([f[0], f[-1]], [0.5, 0.5], 'r--', linewidth=0.5)

    ax.set_xlim([1.3, 33.3])
    ax.set_ylim([0, 1])
    ax.set_yticks(y_ticks)

    title = f"Magnitude Squared Coherence ({run_name.replace('_', ' ')})"
    ax.set_title(title, fontname=font_name, fontsize=font_size_title)
    ax.legend(legend_entries, loc='upper left', fontsize=7)

    max_ch = ch_result['max_ch']
    xlabel = f'Frequency (Hz)                              Max. Coher. = {max_ch:.2f}'
    ax.set_xlabel(xlabel, fontname=font_name, fontsize=font_size_axes)
    ax.set_ylabel('Coherence', fontname=font_name, fontsize=font_size_axes)

    fig.tight_layout()
    return fig
