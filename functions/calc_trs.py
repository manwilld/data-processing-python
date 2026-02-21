"""Smallwood TRS (Test Response Spectrum) calculation."""

import numpy as np
from scipy.signal import lfilter


def calc_trs(time, accel, freq72, damping):
    """Calculate TRS using Smallwood algorithm.

    Parameters
    ----------
    time : array-like
        Time vector (seconds, uniformly spaced).
    accel : array-like
        Acceleration vector (g).
    freq72 : array-like
        Frequency array at 1/72 octave (Hz).
    damping : float
        Damping ratio (e.g. 0.05 for 5%).

    Returns
    -------
    numpy.ndarray
        TRS values (peak absolute response) at each frequency.
    """
    delta_t = time[1] - time[0]
    num_freq = len(freq72)
    trs = np.zeros(num_freq)

    for j in range(num_freq):
        omega = 2 * np.pi * freq72[j]
        omega_d = omega * np.sqrt(1.0 - damping ** 2)

        E = np.exp(-damping * omega * delta_t)
        K = omega_d * delta_t
        C = E * np.cos(K)
        S = E * np.sin(K)
        Sp = S / K

        a1 = 2 * C
        a2 = -(E ** 2)
        b1 = 1 - Sp
        b2 = 2 * (Sp - C)
        b3 = (E ** 2) - Sp

        resp = lfilter([b1, b2, b3], [1, -a1, -a2], accel)

        trs[j] = np.max(np.abs(resp))

    return trs
