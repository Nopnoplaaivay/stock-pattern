from dataclasses import dataclass

@dataclass
class TripleTopPattern:
    inverted: bool

    # Indices of the parts of the Triple Top pattern
    l_top: int  = -1
    r_top: int = -1
    l_trough: int = -1
    r_trough: int = -1
    m_top: int = -1

    # Price of the parts of the Triple Top pattern
    l_top_p: float = -1
    r_top_p: float = -1
    m_top_p: float = -1
    l_trough_p: float = -1
    r_trough_p: float = -1

    start_i: int = -1
    break_i: int = -1
    break_p: float = -1.0

    neck_start: float = -1
    neck_end: float = -1
