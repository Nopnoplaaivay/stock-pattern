from dataclasses import dataclass

@dataclass
class DoubleTopPattern:
    first_peak: int  # Chỉ số thời gian của đỉnh đầu tiên
    first_peak_price: float  # Giá tại đỉnh đầu tiên
    trough: int  # Chỉ số thời gian của đáy giữa
    trough_price: float  # Giá tại đáy giữa
    second_peak: int  # Chỉ số thời gian của đỉnh thứ hai
    second_peak_price: float  # Giá tại đỉnh thứ hai
    neckline_start: int  # Điểm bắt đầu đường Neckline
    neckline_end: int  # Điểm kết thúc đường Neckline
    neckline_price: float  # Giá của đường Neckline
    confirmed_at: int = -1  # Điểm xác nhận mẫu
    confirmed_price: float = -1.0  # Giá xác nhận mẫu