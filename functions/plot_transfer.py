"""Transmissibility (transfer function) plot matching MATLAB plotTransfer.m."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def plot_transfer(run_name, uut, accel_name, axis, axis_uut,
                  frequency, transfer_response, natural_freq,
                  plot_options):
    """Create transmissibility plot matching MATLAB plotTransfer.m output."""
    wide = plot_options.get('wide', 6.5)
    tall = plot_options.get('tall_res', 2.7)
    font_name = plot_options.get('font_name', 'Arial')
    font_size_title = plot_options.get('font_size_title', 11)
    font_size_axes = plot_options.get('font_size_axes', 11)
    font_size_ticks = plot_options.get('font_size_ticks', 10)
    font_size_text = plot_options.get('font_size_text', 7)

    ticks = [1.3, 5, 10, 20, 30]
    y_ticks = [1, 10, 50]

    fig = plt.figure(figsize=(wide, tall))
    fig.patch.set_facecolor('white')
    ax = fig.add_subplot(111)
    ax.set_facecolor('white')

    ax.set_xscale('log')
    ax.set_yscale('log')

    ax.set_xticks(ticks)
    ax.set_xticklabels([str(t) for t in ticks], fontsize=font_size_ticks)
    ax.xaxis.set_minor_locator(ticker.NullLocator())
    ax.set_yticks(y_ticks)
    ax.set_yticklabels([str(t) for t in y_ticks], fontsize=font_size_ticks)
    ax.yaxis.set_minor_locator(ticker.NullLocator())

    # Dotted grid matching MATLAB
    ax.grid(True, which='major', linestyle=':', linewidth=0.5, color='gray', alpha=0.7)
    ax.grid(False, which='minor')

    ax.loglog(frequency, transfer_response, 'k', linewidth=1)

    # Find actual peak near natural_freq (config value is a hint)
    if natural_freq is not None and natural_freq > 0:
        peak_idx = np.argmax(transfer_response)
        nat_freq_actual = frequency[peak_idx]
        nat_freq_value = transfer_response[peak_idx]

        # Plot open circle marker at actual peak
        ax.plot(nat_freq_actual, nat_freq_value, 'bo', markersize=8,
                markeredgewidth=2, markerfacecolor='none')
        label_text = f'{np.ceil(nat_freq_actual * 10) / 10:.1f}-Hz'
        ax.text(nat_freq_actual * np.exp(-0.1), nat_freq_value, label_text,
                ha='right', va='bottom', fontname=font_name,
                fontsize=font_size_text, color='b')

    ax.set_xlim([1, 35])
    ax.set_ylim([0.1, 55])

    title = (f"Transmissibility: {uut.replace('_', ' ')} "
             f"({accel_name.replace('_', ' ')}) {axis_uut} / Table {axis}")
    ax.set_title(title, fontname=font_name, fontsize=font_size_title,
                 fontweight='bold')
    ax.set_xlabel('Frequency (Hz)', fontname=font_name, fontsize=font_size_axes,
                   fontweight='bold')
    ax.set_ylabel('Ratio (g/g)', fontname=font_name, fontsize=font_size_axes,
                   fontweight='bold')

    # Tick direction: inward on all 4 sides, full box
    ax.tick_params(axis='both', which='both', direction='in',
                   top=True, right=True, length=4, width=0.5)
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)

    fig.subplots_adjust(left=0.130, right=0.904, top=0.919, bottom=0.160)
    return fig
