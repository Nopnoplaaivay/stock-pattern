from typing import List
import numpy as np

from backend.modules.patterns import DoubleTopPattern


def check_dt_pattern(extrema_indices: List[int], data: np.array, i: int, early_find: bool = False) -> DoubleTopPattern:
    """ Returns a TripleTopPattern if the pattern is confirmed, otherwise None. """
    pre_top = extrema_indices[0]
    pre_trough = extrema_indices[1]
    f_top = extrema_indices[2]
    f_trough = extrema_indices[3]

    if i - f_trough < 2:
        return None

    # Find second top as max price since f_trough
    s_top = f_trough + data[f_trough + 1: i].argmax() + 1
    if data[s_top] < data[f_trough] or data[pre_top] < data[pre_trough]:
        return None

    # Condition 1: pre_top <= (f_top + f_trough) / 2
    if data[pre_top] > 0.5 * (data[f_top] + data[f_trough]) or data[pre_trough] > data[pre_top]:
        return None


    # Condition 2:
    min_top = min(data[f_top], data[s_top])
    if abs(data[f_top] - data[s_top]) / min_top > 0.02:
        return None

    # Condition 3: At least 10% decline between f_top and s_top
    if (data[f_trough] - data[f_top]) / data[f_top] > -0.1:
        return None

    # Condition 4:


    r_midpoint = 0.5 * (data[s_top] + data[f_trough])
    if early_find:
        if data[i] > r_midpoint:
            return None
    else:
        if data[i] > data[f_trough]:
            return None

    mid_width = s_top - f_top
    pat_start = -1
    neck_start = -1
    for j in range(1, mid_width):
        if f_top - j < 0:
            return None

        if data[f_top - j] < data[f_trough]:
            pat_start = f_top - j
            neck_start = data[f_trough]
            break

    if pat_start == -1:
        return None

    pat = DoubleTopPattern(inverted=False)

    pat.pre_top = pre_top
    pat.s_top = s_top
    pat.pre_trough = pre_trough
    pat.f_trough = f_trough
    pat.f_top = f_top

    pat.pre_top_p = data[pre_top]
    pat.s_top_p = data[s_top]
    pat.pre_trough_p = data[pre_trough]
    pat.f_trough_p = data[f_trough]
    pat.f_top_p = data[f_top]

    pat.start_i = pat_start
    pat.break_i = i
    pat.break_p = data[i]

    pat.neck_start = neck_start
    pat.neck_end = neck_start

    return pat


def check_db_pattern(extrema_indices: List[int], data: np.array, i: int, early_find: bool = False) -> DoubleTopPattern:
    """ Returns a TripleTopPattern if the pattern is confirmed, otherwise None. """
    pre_top = extrema_indices[0]
    pre_trough = extrema_indices[1]
    f_top = extrema_indices[2]
    f_trough = extrema_indices[3]

    if i - f_trough < 2:
        return None

    # Find second top as max price since f_trough
    s_top = f_trough + data[f_trough + 1: i].argmin() + 1
    if data[s_top] > data[f_trough] or data[pre_top] > data[pre_trough]:
        return None

    # Condition 1: pre_top <= (f_top + s_top) / 2
    if data[pre_top] < 0.5 * (data[f_top] + data[f_trough]) or data[pre_trough] < data[pre_top]:
        return None


    # Condition 2:
    min_top = min(data[f_top], data[s_top])
    if abs(data[f_top] - data[s_top]) / min_top > 0.02:
        return None

    # Condition 3: At least 10% rise between f_top and s_top
    if (data[f_trough] - data[f_top]) / data[f_top] < 0.1:
        return None

    # Condition 4:

    r_midpoint = 0.5 * (data[s_top] + data[f_trough])
    if early_find:
        if data[i] < r_midpoint:
            return None
    else:
        if data[i] < data[f_trough]:
            return None

    mid_width = s_top - f_top
    pat_start = -1
    neck_start = -1
    for j in range(1, mid_width):
        if f_top - j < 0:
            return None

        if data[f_top - j] > data[f_trough]:
            pat_start = f_top - j
            neck_start = data[f_trough]
            break

    if pat_start == -1:
        return None

    pat = DoubleTopPattern(inverted=True)

    pat.pre_top = pre_top
    pat.s_top = s_top
    pat.pre_trough = pre_trough
    pat.f_trough = f_trough
    pat.f_top = f_top

    pat.pre_top_p = data[pre_top]
    pat.s_top_p = data[s_top]
    pat.pre_trough_p = data[pre_trough]
    pat.f_trough_p = data[f_trough]
    pat.f_top_p = data[f_top]

    pat.start_i = pat_start
    pat.break_i = i
    pat.break_p = data[i]

    pat.neck_start = neck_start
    pat.neck_end = neck_start

    return pat