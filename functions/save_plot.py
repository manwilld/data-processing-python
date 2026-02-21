"""Save figure as both SVG and PNG with sequential numbering."""

import os
import matplotlib.pyplot as plt


def save_plot(fig, name, run_name, plot_number, output_dir):
    """Save figure as SVG and PNG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
    name : str
        Plot type/identifier (e.g. 'TH_Table_X').
    run_name : str
    plot_number : int
    output_dir : str

    Returns
    -------
    int
        Next plot number (plot_number + 1).
    """
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{plot_number}_{run_name}_{name}"
    svg_path = os.path.join(output_dir, f"{filename}.svg")
    png_path = os.path.join(output_dir, f"{filename}.png")

    fig.savefig(svg_path, format='svg', facecolor='white')
    fig.savefig(png_path, dpi=150, facecolor='white')
    print(png_path)
    plt.close(fig)
    return plot_number + 1
