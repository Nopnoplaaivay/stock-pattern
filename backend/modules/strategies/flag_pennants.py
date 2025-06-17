import pandas as pd
import numpy as np
import plotly.graph_objects as go

from backend.modules.patterns import FlagPennantPattern
from backend.modules.base_strategies import BasePatternStrategy
from backend.utils.rolling_window import rw_top, rw_bottom
from backend.utils.fp_utils import check_bear_pattern_pips, check_bull_pattern_pips


class FlagPennantsStrategy(BasePatternStrategy):
    def __init__(self, order=12):
        self.order = order

    @property
    def name(self) -> str:
        return "Flag Pennants"

    def transform_data(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        data = raw_data.copy()
        data['date'] = data['date'].astype('datetime64[s]')
        data = data.set_index('date')
        data = np.log(data)
        return data

    def find_patterns(self, data: pd.DataFrame):
        transformed_data = self.transform_data(raw_data=data)
        data_slice = transformed_data['close'].to_numpy()
        bull_flags, bear_flags, bull_pennants, bear_pennants = self._find_fp_logic(data=data_slice)
        return bull_flags + bear_flags + bull_pennants + bear_pennants

    def plot_pattern(self, candle_data: pd.DataFrame, pat: FlagPennantPattern):
        self._plot_fp_logic(candle_data=candle_data, pattern=pat)

    def _find_fp_logic(self, data):
        assert (self.order >= 3)
        pending_bull = None  # Pending pattern
        pending_bear = None  # Pending pattern

        bull_pennants = []
        bear_pennants = []
        bull_flags = []
        bear_flags = []
        for i in range(len(data)):

            # Pattern data is organized like so:
            if rw_top(data, i, self.order):
                pending_bear = FlagPennantPattern(i - self.order, data[i - self.order])

            if rw_bottom(data, i, self.order):
                pending_bull = FlagPennantPattern(i - self.order, data[i - self.order])

            if pending_bear is not None:
                if check_bear_pattern_pips(pending_bear, data, i, self.order):
                    if pending_bear.pennant:
                        bear_pennants.append(pending_bear)
                    else:
                        bear_flags.append(pending_bear)
                    pending_bear = None

            if pending_bull is not None:
                if check_bull_pattern_pips(pending_bull, data, i, self.order):
                    if pending_bull.pennant:
                        bull_pennants.append(pending_bull)
                    else:
                        bull_flags.append(pending_bull)
                    pending_bull = None

        return bull_flags, bear_flags, bull_pennants, bear_pennants


    def _plot_fp_logic(self, candle_data: pd.DataFrame, pattern: FlagPennantPattern, pad=2):
        if pad < 0:
            pad = 0

        # Transform data nếu cần thiết (ví dụ log-scale)
        candle_data = self.transform_data(candle_data)

        idx = candle_data.index
        start_i = pattern.base_x - pad
        end_i = pattern.conf_x + 1 + pad
        dat = candle_data.iloc[start_i:end_i]

        fig = go.Figure()

        # === Vẽ nến chính ===
        fig.add_trace(
            go.Candlestick(
                x=dat.index,
                open=dat['open'],
                high=dat['high'],
                low=dat['low'],
                close=dat['close'],
                name='Price',
                increasing_line_color='#26C281',
                decreasing_line_color='#E74C3C',
                increasing_fillcolor='rgba(38, 194, 129, 0.6)',
                decreasing_fillcolor='rgba(231, 76, 60, 0.6)',
                line=dict(width=1.2)
            )
        )

        # === Xác định các đoạn trendline ===
        base_idx = idx[pattern.base_x]  # Gốc cây cột
        tip_idx = idx[pattern.tip_x]    # Ngọn cây cột
        conf_idx = idx[pattern.conf_x]  # Điểm xác nhận mẫu

        pole_line = [(base_idx, pattern.base_y), (tip_idx, pattern.tip_y)]
        upper_line = [(tip_idx, pattern.resist_intercept),
                      (conf_idx, pattern.resist_intercept + pattern.resist_slope * pattern.flag_width)]
        lower_line = [(tip_idx, pattern.support_intercept),
                      (conf_idx, pattern.support_intercept + pattern.support_slope * pattern.flag_width)]

        lines = [pole_line, upper_line, lower_line]
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        names = ['Pole Line', 'Resistance Trendline', 'Support Trendline']

        # === Vẽ các đường trendline ===
        for line, color, name in zip(lines, colors, names):
            fig.add_trace(
                go.Scatter(
                    x=[line[0][0], line[1][0]],
                    y=[line[0][1], line[1][1]],
                    mode='lines',
                    line=dict(color=color, width=2.5, dash='solid'),
                    name=name,
                    hovertemplate=f'<b>{name}</b><br>Price: %{{y:.4f}}<br>Time: %{{x}}<extra></extra>'
                )
            )

        # === Đánh dấu các điểm quan trọng ===
        key_points_x = [base_idx, tip_idx, conf_idx]
        key_points_y = [pattern.base_y, pattern.tip_y, pattern.conf_y]
        key_labels = ['Base of Pole', 'Tip of Pole', 'Confirmation']
        key_colors = ['#FF6B6B', '#4ECDC4', '#FFA500']

        for x, y, label, color in zip(key_points_x, key_points_y, key_labels, key_colors):
            fig.add_trace(
                go.Scatter(
                    x=[x],
                    y=[y],
                    mode='markers',
                    marker=dict(
                        color=color,
                        size=12,
                        symbol='circle',
                        line=dict(color='white', width=1.5)
                    ),
                    name=label,
                    showlegend=False,
                    hovertemplate=f'<b>{label}</b><br>Price: %{{y:.4f}}<br>Time: %{{x}}<extra></extra>'
                )
            )

            fig.add_annotation(
                x=x,
                y=y,
                text=label,
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=1.5,
                arrowcolor=color,
                ax=0,
                ay=-30,
                bgcolor=color,
                bordercolor='white',
                borderwidth=1,
                font=dict(color='white', size=10)
            )

        # === Cập nhật layout ===
        title_text = "🚩 Bullish Flag Pattern" if pattern.tip_y > pattern.base_y else "🔻 Bearish Flag Pattern"
        if pattern.pennant:
            title_text = title_text.replace("Flag", "Pennant")

        fig.update_layout(
            title=dict(
                text=title_text,
                x=0.5,
                font=dict(size=24, family='Arial Black', color='white')
            ),
            template='plotly_dark',
            showlegend=True,
            legend=dict(
                x=0.02,
                y=0.98,
                bgcolor='rgba(0,0,0,0.8)',
                bordercolor='rgba(255,255,255,0.3)',
                borderwidth=1,
                font=dict(size=11)
            ),
            margin=dict(l=80, r=80, t=100, b=80),
            height=650,
            width=1050,
            font=dict(color='white', size=12),
            plot_bgcolor='rgba(15,15,23,0.95)',
            paper_bgcolor='rgba(10,10,15,0.98)',
            dragmode='pan',
            hovermode='x unified'
        )

        # === Trục X/Y ===
        fig.update_xaxes(
            title='Time Period',
            gridcolor='rgba(128,128,128,0.15)',
            showgrid=True,
            zeroline=False,
            rangeslider_visible=False,
            showspikes=True,
            spikesnap='cursor',
            spikemode='across',
            spikethickness=1,
            spikecolor='rgba(255,255,255,0.5)',
            title_font=dict(size=14),
            tickfont=dict(size=11)
        )

        fig.update_yaxes(
            title='Price (Log Scale)' if hasattr(self, 'log_scale') and self.log_scale else 'Price',
            gridcolor='rgba(128,128,128,0.15)',
            showgrid=True,
            zeroline=False,
            showspikes=True,
            spikesnap='cursor',
            spikemode='across',
            spikethickness=1,
            spikecolor='rgba(255,255,255,0.5)',
            title_font=dict(size=14),
            tickfont=dict(size=11),
            tickformat='.4f'
        )

        # Watermark
        fig.add_annotation(
            text="Technical Analysis Dashboard",
            xref="paper", yref="paper",
            x=0.5, y=0.02,
            showarrow=False,
            font=dict(size=10, color="rgba(255,255,255,0.3)")
        )

        fig.show()