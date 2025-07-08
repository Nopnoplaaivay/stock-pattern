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

    # Compute neckline
    # neck_run = r_peak - l_peak
    # neck_rise = data[r_peak] - data[l_peak]
    # neck_slope = neck_rise / neck_run

    # neckline value at current index
    # neck_val = data[l_trough] + (i - l_trough) * neck_slope
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
    return None

    # # Unpack list
    # l_shoulder = extrema_indices[0]
    # l_armpit = extrema_indices[1]
    # head = extrema_indices[2]
    # r_armpit = extrema_indices[3]
    #
    # if i - r_armpit < 2:
    #     return None
    #
    # # Find right shoulder as max price since r_armpit
    # r_shoulder = r_armpit + data[r_armpit + 1: i].argmin() + 1
    #
    # # Head must be lower than shoulders
    # if data[head] >= min(data[l_shoulder], data[r_shoulder]):
    #     return None
    #
    # # Balance rule. Shoulders are below the others midpoint.
    # # A shoulder's midpoint is the midpoint between the shoulder and armpit
    # r_midpoint = 0.5 * (data[r_shoulder] + data[r_armpit])
    # l_midpoint = 0.5 * (data[l_shoulder] + data[l_armpit])
    # if data[l_shoulder] > r_midpoint or data[r_shoulder] > l_midpoint:
    #     return None
    #
    # # Symmetry rule. time from shoulder to head are comparable
    # r_to_h_time = r_shoulder - head
    # l_to_h_time = head - l_shoulder
    # if r_to_h_time > 2.5 * l_to_h_time or l_to_h_time > 2.5 * r_to_h_time:
    #     return None
    #
    # # Compute neckline
    # neck_run = r_armpit - l_armpit
    # neck_rise = data[r_armpit] - data[l_armpit]
    # neck_slope = neck_rise / neck_run
    #
    # # neckline value at current index
    # neck_val = data[l_armpit] + (i - l_armpit) * neck_slope
    #
    # # Confirm pattern when price is halfway from right shoulder
    # if early_find:
    #     if data[i] < r_midpoint:
    #         return None
    # else:
    #
    #     # Price has yet to break neckline, unconfirmed
    #     if data[i] < neck_val:
    #         return None
    #
    # # Find beginning of pattern. Neck to left shoulder
    # head_width = r_armpit - l_armpit
    # pat_start = -1
    # neck_start = -1
    # for j in range(1, head_width):
    #     neck = data[l_armpit] + (l_shoulder - l_armpit - j) * neck_slope
    #
    #     if l_shoulder - j < 0:
    #         return None
    #
    #     if data[l_shoulder - j] > neck:
    #         pat_start = l_shoulder - j
    #         neck_start = neck
    #         break
    #
    # if pat_start == -1:
    #     return None
    #
    # # Pattern confirmed if here :)
    # pat = HSPattern(inverted=True)
    #
    # pat.l_shoulder = l_shoulder
    # pat.r_shoulder = r_shoulder
    # pat.l_armpit = l_armpit
    # pat.r_armpit = r_armpit
    # pat.head = head
    #
    # pat.l_shoulder_p = data[l_shoulder]
    # pat.r_shoulder_p = data[r_shoulder]
    # pat.l_armpit_p = data[l_armpit]
    # pat.r_armpit_p = data[r_armpit]
    # pat.head_p = data[head]
    #
    # pat.start_i = pat_start
    # pat.break_i = i
    # pat.break_p = data[i]
    #
    # pat.neck_start = neck_start
    # pat.neck_end = neck_val
    # pat.pattern_r2 = compute_pattern_r2(data, pat)
    #
    # pat.neck_slope = neck_slope
    # pat.head_width = head_width
    # pat.head_height = (data[l_armpit] + (head - l_armpit) * neck_slope) - data[head]
    # pat.pattern_r2 = compute_pattern_r2(data, pat)
    #
    # # if pat.pattern_r2 < 0.0:
    # #    return None
    #
    # return pat