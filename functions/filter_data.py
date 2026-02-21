"""Butterworth lowpass filter with filtfilt."""

from scipy.signal import butter, filtfilt


def filter_th(accel, sample_rate, order, cutoff_hz):
    """Apply Butterworth lowpass filter using filtfilt (zero-phase).

    Parameters
    ----------
    accel : array-like
        Acceleration signal.
    sample_rate : float
        Sampling rate in Hz.
    order : int
        Filter order.
    cutoff_hz : float
        Cutoff frequency in Hz.

    Returns
    -------
    numpy.ndarray
        Filtered acceleration signal.
    """
    Wn = cutoff_hz / sample_rate / 2
    b, a = butter(order, Wn, btype='low')
    return filtfilt(b, a, accel)
