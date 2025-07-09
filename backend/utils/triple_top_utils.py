from typing import List
import numpy as np

from backend.modules.patterns import TripleTopPattern


def check_tt_pattern(extrema_indices: List[int], data: np.array, i: int, early_find: bool = False) -> TripleTopPattern:
    """ Returns a TripleTopPattern if the pattern is confirmed, otherwise None. """
    pre_top = extrema_indices[0]
    pre_trough = extrema_indices[1]
    l_top = extrema_indices[2]
    l_trough = extrema_indices[3]
    m_top = extrema_indices[4]
    r_trough = extrema_indices[5]

    if i - r_trough < 2:
        return None

    # Find right shoulder as max price since r_armpit
    r_top = r_trough + data[r_trough + 1: i].argmax() + 1
    if data[r_top] < data[r_trough] or data[l_top] < data[l_trough]:
        return None

    # Condition 1
    if data[pre_top] > 0.5 * (data[l_top] + data[l_trough]) or data[pre_trough] > data[pre_top]:
        return None

    # Condition 2
    max_top = max(data[l_top], data[r_top])
    min_top = min(data[l_top], data[r_top])
    if (max_top - min_top) / min_top > 0.04 or data[m_top] > max_top:
        return None

    # Condition 3
    if data[r_trough] < data[l_trough] or data[r_trough] > 1.04 * data[l_trough]:
        return None

    # Condition 4
    r_to_m_time = r_top - m_top
    l_to_m_time = m_top - l_top
    if r_to_m_time > 2.5 * l_to_m_time or l_to_m_time > 2.5 * r_to_m_time:
        return None

    neck_val = data[l_trough]

    r_midpoint = 0.5 * (data[r_top] + data[r_trough])
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
        if l_top - j < 0:
            return None

        if data[l_top - j] < neck:
            pat_start = l_top - j
            neck_start = neck
            break

    if pat_start == -1:
        return None

    pat = TripleTopPattern(inverted=False)

    pat.pre_top = pre_top
    pat.pre_trough = pre_trough
    pat.l_top = l_top
    pat.r_top = r_top
    pat.l_trough = l_trough
    pat.r_trough = r_trough
    pat.m_top = m_top

    pat.pre_top_p = data[pre_top]
    pat.pre_trough_p = data[pre_trough]
    pat.l_top_p = data[l_top]
    pat.r_top_p = data[r_top]
    pat.l_trough_p = data[l_trough]
    pat.r_trough_p = data[r_trough]
    pat.m_top_p = data[m_top]

    pat.start_i = pat_start
    pat.break_i = i
    pat.break_p = data[i]

    pat.neck_start = neck_start
    pat.neck_end = neck_val

    return pat


def check_tb_pattern(extrema_indices: List[int], data: np.array, i: int, early_find: bool = False) -> TripleTopPattern:
    """ Returns a TripleTopPattern if the pattern is confirmed, otherwise None. """
    pre_top = extrema_indices[0]
    pre_trough = extrema_indices[1]
    l_top = extrema_indices[2]
    l_trough = extrema_indices[3]
    m_top = extrema_indices[4]
    r_trough = extrema_indices[5]

    if i - r_trough < 2:
        return None

    # Find right shoulder as max price since r_armpit
    r_top = r_trough + data[r_trough + 1: i].argmin() + 1
    if data[r_top] > data[r_trough] or data[l_top] > data[l_trough]:
        return None

    # Condition 1
    if data[pre_top] < 0.5 * (data[l_top] + data[l_trough]) or data[pre_trough] < data[pre_top]:
        return None

    # Condition 2
    max_top = max(data[l_top], data[r_top])
    min_top = min(data[l_top], data[r_top])
    if (max_top - min_top) / min_top > 0.04 or data[m_top] < min_top:
        return None

    # Condition 3
    if data[r_trough] > data[l_trough] or data[l_trough] > 1.04 * data[r_trough]:
        return None

    # Condition 4
    r_to_m_time = r_top - m_top
    l_to_m_time = m_top - l_top
    if r_to_m_time > 2.5 * l_to_m_time or l_to_m_time > 2.5 * r_to_m_time:
        return None

    neck_val = data[l_trough]
    r_midpoint = 0.5 * (data[r_top] + data[r_trough])
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
        if l_top - j < 0:
            return None

        if data[l_top - j] > neck:
            pat_start = l_top - j
            neck_start = neck
            break

    if pat_start == -1:
        return None

    pat = TripleTopPattern(inverted=True)

    pat.pre_top = pre_top
    pat.pre_trough = pre_trough
    pat.l_top = l_top
    pat.r_top = r_top
    pat.l_trough = l_trough
    pat.r_trough = r_trough
    pat.m_top = m_top

    pat.pre_top_p = data[pre_top]
    pat.pre_trough_p = data[pre_trough]
    pat.l_top_p = data[l_top]
    pat.r_top_p = data[r_top]
    pat.l_trough_p = data[l_trough]
    pat.r_trough_p = data[r_trough]
    pat.m_top_p = data[m_top]

    pat.start_i = pat_start
    pat.break_i = i
    pat.break_p = data[i]

    pat.neck_start = neck_start
    pat.neck_end = neck_val

    return pat