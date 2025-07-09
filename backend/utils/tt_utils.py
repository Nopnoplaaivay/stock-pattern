from typing import List
import numpy as np

from backend.modules.patterns import TripleTopPattern


def check_tt_pattern(extrema_indices: List[int], data: np.array, i: int, early_find: bool = False) -> TripleTopPattern:
    """ Returns a TripleTopPattern if the pattern is confirmed, otherwise None. """
    l_peak = extrema_indices[0]
    l_trough = extrema_indices[1]
    m_peak = extrema_indices[2]
    r_trough = extrema_indices[3]

    if i - r_trough < 2:
        return None

    # Find right shoulder as max price since r_armpit
    r_peak = r_trough + data[r_trough + 1: i].argmax() + 1
    if data[r_peak] < data[r_trough] or data[l_peak] < data[l_trough]:
        return None

    # Condition 2
    max_peak = max(data[l_peak], data[r_peak])
    min_peak = min(data[l_peak], data[r_peak])
    if (max_peak - min_peak) / min_peak > 0.04 or data[m_peak] > max_peak:
        return None

    # Condition 3
    if data[r_trough] < data[l_trough] or data[r_trough] > 1.04 * data[l_trough]:
        return None

    # Condition 4
    r_to_m_time = r_peak - m_peak
    l_to_m_time = m_peak - l_peak
    if r_to_m_time > 2.5 * l_to_m_time or l_to_m_time > 2.5 * r_to_m_time:
        return None

    neck_val = data[l_trough]

    r_midpoint = 0.5 * (data[r_peak] + data[r_trough])
    if early_find:
        if data[i] > r_midpoint:
            return None
    else:
        if data[i] > neck_val:
            return None

    mid_width = r_trough - l_trough
    pat_start = -1
    neck_start = -1
    for j in range(1, mid_width):
        neck = data[l_trough]
        if l_peak - j < 0:
            return None

        if data[l_peak - j] < neck:
            pat_start = l_peak - j
            neck_start = neck
            break

    if pat_start == -1:
        return None

    pat = TripleTopPattern(inverted=False)

    pat.l_peak = l_peak
    pat.r_peak = r_peak
    pat.l_trough = l_trough
    pat.r_trough = r_trough
    pat.m_peak = m_peak

    pat.l_peak_p = data[l_peak]
    pat.r_peak_p = data[r_peak]
    pat.l_trough_p = data[l_trough]
    pat.r_trough_p = data[r_trough]
    pat.m_peak_p = data[m_peak]

    pat.start_i = pat_start
    pat.break_i = i
    pat.break_p = data[i]

    pat.neck_start = neck_start
    pat.neck_end = neck_val

    return pat


def check_tb_pattern(extrema_indices: List[int], data: np.array, i: int, early_find: bool = False) -> TripleTopPattern:
    """ Returns a TripleTopPattern if the pattern is confirmed, otherwise None. """
    l_peak = extrema_indices[0]
    l_trough = extrema_indices[1]
    m_peak = extrema_indices[2]
    r_trough = extrema_indices[3]

    if i - r_trough < 2:
        return None

    # Find right shoulder as max price since r_armpit
    r_peak = r_trough + data[r_trough + 1: i].argmin() + 1
    if data[r_peak] > data[r_trough] or data[l_peak] > data[l_trough]:
        return None

    # Condition 2
    max_peak = max(data[l_peak], data[r_peak])
    min_peak = min(data[l_peak], data[r_peak])
    if (max_peak - min_peak) / min_peak > 0.04 or data[m_peak] < min_peak:
        return None

    # Condition 3
    if data[r_trough] > data[l_trough] or data[l_trough] > 1.04 * data[r_trough]:
        return None

    # Condition 4
    r_to_m_time = r_peak - m_peak
    l_to_m_time = m_peak - l_peak
    if r_to_m_time > 2.5 * l_to_m_time or l_to_m_time > 2.5 * r_to_m_time:
        return None

    neck_val = data[l_trough]
    r_midpoint = 0.5 * (data[r_peak] + data[r_trough])
    if early_find:
        if data[i] < r_midpoint:
            return None
    else:
        if data[i] < neck_val:
            return None

    mid_width = r_trough - l_trough
    pat_start = -1
    neck_start = -1
    for j in range(1, mid_width):
        neck = data[l_trough]
        if l_peak - j < 0:
            return None

        if data[l_peak - j] > neck:
            pat_start = l_peak - j
            neck_start = neck
            break

    if pat_start == -1:
        return None

    pat = TripleTopPattern(inverted=False)

    pat.l_peak = l_peak
    pat.r_peak = r_peak
    pat.l_trough = l_trough
    pat.r_trough = r_trough
    pat.m_peak = m_peak

    pat.l_peak_p = data[l_peak]
    pat.r_peak_p = data[r_peak]
    pat.l_trough_p = data[l_trough]
    pat.r_trough_p = data[r_trough]
    pat.m_peak_p = data[m_peak]

    pat.start_i = pat_start
    pat.break_i = i
    pat.break_p = data[i]

    pat.neck_start = neck_start
    pat.neck_end = neck_val

    return pat