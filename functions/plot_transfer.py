"""Transmissibility (transfer function) plot for resonance data."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def plot_transfer(run_name, uut, accel_name, axis, axis_uut,
                  frequency, transfer_response, natural_freq,
                  plot_options):
    """Create transmissibility plot.

    Parameters
    ----------
    run_name : str
    uut : str
        UUT name (e.g. 'UUT_1').
    accel_name : str
        Accelerometer name (e.g. 'Controller').
    axis : str
        Table axis ('X', 'Y', 'Z').
    axis_uut : str
        UUT axis label ('SS', 'FB', 'V').
    frequency : array
        Frequency array (Hz).
    transfer_response : array
        Transmissibility = UUT / Table magnitude.
    natural_freq : float
        Selected natural frequency (Hz).
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
    font_size_text = plot_options.get('font_size_text', 7)

    ticks = [1.3, 5, 10, 20, 30]
    y_ticks = [1, 10, 50]
    axis_limits = [1, 35, 0.1, 55]

    fig, ax = plt.subplots(figsize=(wide, tall))
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xticks(ticks)
    ax.set_xticklabels([str(t) for t in ticks])
    ax.set_yticks(y_ticks)
    ax.set_yticklabels([str(t) for t in y_ticks])
    ax.minorticks_on()
    ax.grid(True, which='both', linewidth=0.5)
    ax.tick_params(labelsize=font_size_ticks)

    ax.loglog(frequency, transfer_response, 'k', linewidth=1)

    # Plot natural frequency marker
    if natural_freq is not None and natural_freq > 0:
        y_point = np.interp(natural_freq, frequency, transfer_response)
        ax.plot(natural_freq, y_point, 'bo', markersize=8, markeredgewidth=2,
                markerfacecolor='none')
        label_text = f'{np.ceil(natural_freq * 10) / 10:.1f}-Hz'
        ax.text(natural_freq * np.exp(-0.1), y_point, label_text,
                ha='right', va='bottom', fontname=font_name,
                fontsize=font_size_text, color='b')

    ax.set_xlim(axis_limits[:2])
    ax.set_ylim(axis_limits[2:])

    title = (f"Transmissibility: {uut.replace('_', ' ')} "
             f"({accel_name.replace('_', ' ')}) {axis_uut} / Table {axis}")
    ax.set_title(title, fontname=font_name, fontsize=font_size_title)
    ax.set_xlabel('Frequency (Hz)', fontname=font_name, fontsize=font_size_axes)
    ax.set_ylabel('Ratio (g/g)', fontname=font_name, fontsize=font_size_axes)

    fig.tight_layout()
    return fig
