# import pandas as pd
# import numpy as np
# import plotly.graph_objects as go
# 
# from backend.patterns import DoubleTopPattern
# from backend.base_strategies import BasePatternStrategy
# from backend.utils.rolling_window import rw_top
# 
# 
# 
# 
# 
# class DoubleTopStrategy(BasePatternStrategy):
#     def __init__(self, order=6, min_peak_distance=None, max_price_diff=0.05, min_trough_decline=0.03):
#         self.order = order
#         # Khoảng cách tối thiểu giữa 2 đỉnh (mặc định = 2 * order)
#         self.min_peak_distance = min_peak_distance or order * 2
#         # Sai số giá tối đa giữa 2 đỉnh (5%)
#         self.max_price_diff = max_price_diff
#         # Mức giảm tối thiểu từ đỉnh xuống đáy (3%)
#         self.min_trough_decline = min_trough_decline
# 
#     @property
#     def name(self) -> str:
#         return "Double Top"
# 
#     def transform_data(self, raw_data: pd.DataFrame) -> pd.DataFrame:
#         data = raw_data.copy()
#         data['date'] = data['date'].astype('datetime64[s]')
#         data = data.set_index('date')
#         return data
# 
#     def find_patterns(self, data: pd.DataFrame):
#         transformed_data = self.transform_data(raw_data=data)
#         data_slice = transformed_data['close'].to_numpy()
#         double_tops = self._find_double_top_logic(data=data_slice, order=self.order)
#         return double_tops
# 
#     def plot_pattern(self, candle_data: pd.DataFrame, pat: DoubleTopPattern):
#         self._plot_double_top_logic(candle_data=candle_data, pat=pat)
# 
#     def _find_double_top_logic(self, data: np.array, order: int):
#         """
#         Tìm kiếm mẫu hình Double Top với logic cải thiện:
#         1. Tìm các đỉnh cục bộ
#         2. Kiểm tra 2 đỉnh có cùng mức giá (±5%)
#         3. Tìm đáy giữa 2 đỉnh
#         4. Đường neckline nối từ đáy trung tâm
#         5. Xác nhận khi giá phá vỡ neckline
#         """
#         # Tìm tất cả các đỉnh cục bộ
#         peaks = []
#         for i in range(order, len(data) - order):
#             if rw_top(data, i + order, order):  # i + order vì rw_top cần điều chỉnh
#                 peaks.append(i)
# 
#         patterns = []
# 
#         # Kiểm tra từng cặp đỉnh
#         for i in range(len(peaks) - 1):
#             for j in range(i + 1, len(peaks)):
#                 first_peak = peaks[i]
#                 second_peak = peaks[j]
# 
#                 # 1. Kiểm tra khoảng cách tối thiểu
#                 if second_peak - first_peak < self.min_peak_distance:
#                     continue
# 
#                 # 2. Kiểm tra giá của 2 đỉnh gần bằng nhau
#                 price_diff = abs(data[first_peak] - data[second_peak]) / max(data[first_peak], data[second_peak])
#                 if price_diff > self.max_price_diff:
#                     continue
# 
#                 # 3. Tìm đáy giữa 2 đỉnh
#                 trough = np.argmin(data[first_peak:second_peak + 1]) + first_peak
# 
#                 # Kiểm tra đáy có thực sự thấp hơn 2 đỉnh
#                 trough_decline_1 = (data[first_peak] - data[trough]) / data[first_peak]
#                 trough_decline_2 = (data[second_peak] - data[trough]) / data[second_peak]
# 
#                 if trough_decline_1 < self.min_trough_decline or trough_decline_2 < self.min_trough_decline:
#                     continue
# 
#                 # 4. Tạo pattern với neckline tại mức giá của đáy
#                 pattern = DoubleTopPattern(
#                     first_peak=first_peak,
#                     first_peak_price=data[first_peak],
#                     trough=trough,
#                     trough_price=data[trough],
#                     second_peak=second_peak,
#                     second_peak_price=data[second_peak],
#                     neckline_start=trough,  # Neckline bắt đầu từ đáy
#                     neckline_end=len(data) - 1,  # Kéo dài đến cuối dữ liệu
#                     neckline_price=data[trough]  # Mức giá neckline = giá đáy
#                 )
# 
#                 # 5. Kiểm tra xác nhận breakout sau đỉnh thứ 2
#                 confirmed = False
#                 for k in range(second_peak + 1, len(data)):
#                     # Xác nhận khi giá đóng cửa vượt qua neckline
#                     if data[k] < pattern.neckline_price:
#                         pattern.confirmed_at = k
#                         pattern.confirmed_price = data[k]
#                         confirmed = True
#                         break
# 
#                 # Chỉ thêm pattern đã được xác nhận
#                 if confirmed:
#                     patterns.append(pattern)
#                     break  # Thoát khỏi vòng lặp j để tránh trùng lặp
# 
#         return patterns
# 
#     def _plot_double_top_logic(self, candle_data: pd.DataFrame, pat: DoubleTopPattern, pad=5):
#         """
#         Vẽ biểu đồ Double Top pattern với:
#         - Candlestick chart
#         - Đánh dấu 2 đỉnh và đáy
#         - Đường neckline
#         - Điểm xác nhận breakout
#         """
#         if pad < 0:
#             pad = 0
# 
#         candle_data = self.transform_data(candle_data)
#         idx = candle_data.index
# 
#         # Xác định phạm vi hiển thị
#         start_i = max(0, pat.first_peak - pad)
#         end_i = min(len(candle_data) - 1,
#                     pat.confirmed_at + pad if pat.confirmed_at != -1 else pat.second_peak + pad * 2)
# 
#         dat = candle_data.iloc[start_i:end_i + 1]
# 
#         fig = go.Figure()
# 
#         # 1. Candlestick chính
#         fig.add_trace(
#             go.Candlestick(
#                 x=dat.index,
#                 open=dat['open'],
#                 high=dat['high'],
#                 low=dat['low'],
#                 close=dat['close'],
#                 name='Price',
#                 increasing_line_color='#00FF88',
#                 decreasing_line_color='#FF4444',
#                 increasing_fillcolor='rgba(0, 255, 136, 0.3)',
#                 decreasing_fillcolor='rgba(255, 68, 68, 0.3)',
#                 line=dict(width=1)
#             )
#         )
# 
#         # 2. Đường neckline (đường kháng cự/hỗ trợ)
#         neckline_start_idx = max(start_i, pat.trough)
#         neckline_end_idx = min(end_i, pat.confirmed_at if pat.confirmed_at != -1 else end_i)
# 
#         fig.add_trace(
#             go.Scatter(
#                 x=[idx[neckline_start_idx], idx[neckline_end_idx]],
#                 y=[pat.neckline_price, pat.neckline_price],
#                 mode='lines',
#                 line=dict(color='#FFD700', width=3, dash='dash'),
#                 name='Neckline (Support)',
#                 hovertemplate='<b>Neckline</b><br>Price: %{y:.4f}<extra></extra>'
#             )
#         )
# 
#         # 3. Đường kết nối các điểm chính
#         # Kết nối đỉnh 1 -> đáy -> đỉnh 2
#         connection_x = [idx[pat.first_peak], idx[pat.trough], idx[pat.second_peak]]
#         connection_y = [pat.first_peak_price, pat.trough_price, pat.second_peak_price]
# 
#         fig.add_trace(
#             go.Scatter(
#                 x=connection_x,
#                 y=connection_y,
#                 mode='lines',
#                 line=dict(color='#FF6B6B', width=2),
#                 name='Pattern Structure',
#                 hovertemplate='<b>Pattern Line</b><br>Price: %{y:.4f}<extra></extra>'
#             )
#         )
# 
#         # 4. Đánh dấu các điểm quan trọng
#         key_points = [
#             (idx[pat.first_peak], pat.first_peak_price, 'First Peak', '#FF6B6B', 'diamond'),
#             (idx[pat.trough], pat.trough_price, 'Trough', '#4ECDC4', 'triangle-down'),
#             (idx[pat.second_peak], pat.second_peak_price, 'Second Peak', '#FF6B6B', 'diamond'),
#         ]
# 
#         if pat.confirmed_at != -1:
#             key_points.append(
#                 (idx[pat.confirmed_at], pat.confirmed_price, 'Breakout', '#FFA500', 'star')
#             )
# 
#         for x, y, label, color, symbol in key_points:
#             fig.add_trace(
#                 go.Scatter(
#                     x=[x], y=[y],
#                     mode='markers',
#                     marker=dict(
#                         color=color,
#                         size=12,
#                         symbol=symbol,
#                         line=dict(color='white', width=2)
#                     ),
#                     name=label,
#                     hovertemplate=f'<b>{label}</b><br>Price: %{{y:.4f}}<br>Time: %{{x}}<extra></extra>'
#                 )
#             )
# 
#         # 5. Thêm annotations
#         annotations = [
#             dict(x=idx[pat.first_peak], y=pat.first_peak_price, text="Peak 1",
#                  showarrow=True, arrowhead=2, arrowcolor='#FF6B6B', ay=-30),
#             dict(x=idx[pat.trough], y=pat.trough_price, text="Trough",
#                  showarrow=True, arrowhead=2, arrowcolor='#4ECDC4', ay=30),
#             dict(x=idx[pat.second_peak], y=pat.second_peak_price, text="Peak 2",
#                  showarrow=True, arrowhead=2, arrowcolor='#FF6B6B', ay=-30),
#         ]
# 
#         if pat.confirmed_at != -1:
#             annotations.append(
#                 dict(x=idx[pat.confirmed_at], y=pat.confirmed_price, text="Breakout!",
#                      showarrow=True, arrowhead=2, arrowcolor='#FFA500', ay=30)
#             )
# 
#         # 6. Layout cải thiện
#         fig.update_layout(
#             title=dict(
#                 text='📉 Double Top Pattern - Bearish Reversal Signal',
#                 x=0.5,
#                 font=dict(size=20, color='white')
#             ),
#             template='plotly_dark',
#             showlegend=True,
#             height=600,
#             width=1100,
#             dragmode='pan',
#             annotations=annotations,
#             legend=dict(
#                 yanchor="top",
#                 y=0.99,
#                 xanchor="left",
#                 x=0.01
#             )
#         )
# 
#         fig.update_xaxes(
#             title='Time Period',
#             gridcolor='rgba(128,128,128,0.2)',
#             showspikes=True
#         )
# 
#         fig.update_yaxes(
#             title='Price',
#             gridcolor='rgba(128,128,128,0.2)',
#             showspikes=True
#         )
# 
#         fig.show()
# 
#         # In thông tin pattern
#         print(f"\n{'=' * 50}")
#         print(f"DOUBLE TOP PATTERN DETECTED")
#         print(f"{'=' * 50}")
#         print(f"First Peak:  {pat.first_peak_price:.4f} at index {pat.first_peak}")
#         print(f"Trough:      {pat.trough_price:.4f} at index {pat.trough}")
#         print(f"Second Peak: {pat.second_peak_price:.4f} at index {pat.second_peak}")
#         print(f"Neckline:    {pat.neckline_price:.4f}")
# 
#         if pat.confirmed_at != -1:
#             print(f"Confirmed:   {pat.confirmed_price:.4f} at index {pat.confirmed_at}")
#             print(f"📉 BEARISH SIGNAL CONFIRMED!")
#         else:
#             print(f"⏳ Waiting for breakout confirmation...")
# 
#         # Tính toán các chỉ số kỹ thuật
#         price_similarity = abs(pat.first_peak_price - pat.second_peak_price) / pat.first_peak_price * 100
#         decline_from_peak1 = (pat.first_peak_price - pat.trough_price) / pat.first_peak_price * 100
#         decline_from_peak2 = (pat.second_peak_price - pat.trough_price) / pat.second_peak_price * 100
# 
#         print(f"\nPattern Statistics:")
#         print(f"Price Similarity: {price_similarity:.2f}% difference")
#         print(f"Decline from Peak 1: {decline_from_peak1:.2f}%")
#         print(f"Decline from Peak 2: {decline_from_peak2:.2f}%")
#         print(f"{'=' * 50}")