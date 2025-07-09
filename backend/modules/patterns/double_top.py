from dataclasses import dataclass

@dataclass
class DoubleTopPattern:
    inverted: bool

    # Indices of the parts of the Double Top pattern
    pre_top: int  = -1
    pre_trough: int = -1
    f_top: int = -1
    f_trough: int = -1
    s_top: int = -1

    pre_top_p: float = -1
    pre_trough_p: float = -1
    f_top_p: float = -1
    f_trough_p: float = -1
    s_top_p: float = -1

    start_i: int = -1
    break_i: int = -1
    break_p: float = -1.0

    neck_start: float = -1
    neck_end: float = -1