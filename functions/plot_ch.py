"""Coherence plot matching MATLAB plotCH.m."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def plot_ch(ch_result, run_name, plot_options):
    """Create magnitude squared coherence plot matching MATLAB plotCH.m output."""
    wide = plot_options.get('wide', 6.5)
    tall = plot_options.get('tall_ch', 2.7)
    font_name = plot_options.get('font_name', 'Arial')
    font_size_title = plot_options.get('font_size_title', 11)
    font_size_axes = plot_options.get('font_size_axes', 11)
    font_size_ticks = plot_options.get('font_size_ticks', 10)

    ticks = [1.3, 10, 20, 33.3]
    y_ticks = [0.0, 0.25, 0.5, 0.75, 1.0]

    fig = plt.figure(figsize=(wide, tall))
    fig.patch.set_facecolor('white')
    ax = fig.add_subplot(111)
    ax.set_facecolor('white')

    ax.set_xscale('log')
    ax.set_xticks(ticks)
    ax.set_xticklabels([str(t) for t in ticks], fontsize=font_size_ticks)

    # MATLAB colors: k (XY), c (XZ), m (YZ)
    colors = ['k', 'c', 'm']
    legend_entries = []

    for k, pair in enumerate(ch_result['pairs']):
        color = colors[k % len(colors)]
        ax.semilogx(pair['frequencies'], pair['coherence'], color, linewidth=0.75)
        legend_entries.append(pair['axes'])

    # Threshold at 0.5 (red dashed)
    if ch_result['pairs']:
        f = ch_result['pairs'][0]['frequencies']
        ax.semilogx([f[0], f[-1]], [0.5, 0.5], 'r--', linewidth=1.0)

    ax.set_xlim([1.3, 33.3])
    ax.set_ylim([0, 1])
    ax.set_yticks(y_ticks)

    ax.grid(True, which='major', linewidth=0.5)

    title = f"Magnitude Squared Coherence ({run_name.replace('_', ' ')})"
    ax.set_title(title, fontname=font_name, fontsize=font_size_title,
                 fontweight='bold')
    ax.legend(legend_entries, loc='upper left', fontsize=7)

    max_ch = ch_result['max_ch']
    xlabel_text = (f'{"":>46s}Frequency (Hz) '
                   f'{"":>11s}Max. Coher. = {max_ch:.2f}')
    ax.set_xlabel(xlabel_text, fontname=font_name, fontsize=font_size_axes,
                   fontweight='bold')
    ax.set_ylabel('Coherence', fontname=font_name, fontsize=font_size_axes,
                   fontweight='bold')

    # Tick direction: inward on all 4 sides, full box
    ax.tick_params(axis='both', which='both', direction='in',
                   top=True, right=True, length=4, width=0.5)
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)

    fig.subplots_adjust(left=0.130, right=0.904, top=0.919, bottom=0.160)
    return fig
