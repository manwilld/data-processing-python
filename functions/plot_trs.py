"""TRS vs RRS plot (single accelerometer)."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def plot_trs(run_name, accel_name, freq72, RRS, Aflx, Arig,
             freq06, TRS06, damping, low_cutoff, plot_options):
    """Create TRS vs RRS plot.

    Parameters
    ----------
    run_name, accel_name : str
    freq72 : array
        Full 1/72 octave frequency array.
    RRS : array
        Required Response Spectrum at 1/72 octave.
    Aflx, Arig : float
    freq06, TRS06 : array
        Optimized 1/6 octave frequency and TRS.
    damping : float
    low_cutoff : float
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
    font_size_legend = plot_options.get('font_size_legend', 6)

    max_trs = np.max(TRS06)
    x_ticks = [0.5, 1, 1.3, 8.3, 10, 20, 35]
    x_min, x_max = 0.5, 35
    y_ticks = [0.1, 0.5, 1, 5, 10, 50]

    is_table = 'Table' in accel_name
    upper_y = max(max_trs, 1.3 * Aflx) if is_table else max_trs

    if upper_y < 3:
        y_max = 4
    elif upper_y < 5:
        y_max = 6.5
    elif upper_y < 7.5:
        y_max = 9
    elif upper_y < 10:
        y_max = 12
    else:
        y_max = np.ceil(max_trs * 1.2)

    y_min = min(np.floor(Arig * 0.85 * 10) / 10, 0.9)

    fig, ax = plt.subplots(figsize=(wide, tall))

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([str(t) for t in x_ticks])
    ax.set_yticks(y_ticks)
    ax.set_yticklabels([str(t) for t in y_ticks])
    ax.minorticks_on()
    ax.grid(True, which='both', linewidth=0.5)
    ax.tick_params(labelsize=font_size_ticks)

    # Plot TRS
    ax.loglog(freq06, TRS06, 'k', linewidth=1, label=accel_name.replace('_', ' '))

    if is_table:
        ax.loglog(freq72, RRS, '--b', linewidth=1.5, label='RRS')
        ax.loglog(freq72, 0.9 * RRS, '--r', linewidth=0.5, label='0.9*RRS')
        ax.loglog(freq72, 1.3 * RRS, '--y', linewidth=0.5)

        # Aflx reference line and text
        ax.text(x_min * 1.1, Aflx, f'Aflx = {Aflx:.2f}', color='blue',
                ha='left', va='top', fontsize=font_size_text)
        ax.plot([freq72[0], 1.3], [Aflx, Aflx], '--',
                color=[0.7, 0.7, 1], linewidth=0.25)

        # Arig reference line and text
        ax.text(10, Arig, f'Arig = {Arig:.2f}', color='blue',
                ha='left', va='top', fontsize=font_size_text)
        ax.plot([8.3, freq72[-1]], [Arig, Arig], '--',
                color=[0.7, 0.7, 1], linewidth=0.25)

        # Low cutoff frequency
        ax.axvline(x=low_cutoff, color=[0.7, 0.7, 1], linestyle='--', linewidth=0.25)
        ax.text(low_cutoff, y_min, f' {low_cutoff:.1f}-Hz Lower Limit',
                color='blue', ha='left', va='bottom', fontsize=font_size_text)

    ax.set_xlim([x_min, x_max])
    ax.set_ylim([y_min, y_max])

    if is_table:
        title = f"TRS vs. RRS: {accel_name.replace('_', ' ')} ({run_name.replace('_', ' ')})"
    else:
        title = f"TRS: {accel_name.replace('_', ' ')} ({run_name.replace('_', ' ')})"
    ax.set_title(title, fontname=font_name, fontsize=font_size_title)
    ax.set_xlabel('Frequency (Hz)', fontname=font_name, fontsize=font_size_axes)
    ylabel = f'Spectral Acceleration (g)\n{int(damping*100)}% Damping'
    ax.set_ylabel(ylabel, fontname=font_name, fontsize=font_size_axes)
    ax.legend(loc='upper left', fontsize=font_size_legend)

    fig.tight_layout()
    return fig
