import os

import pandas as pd
import numpy as np
import re
import plotly.graph_objects as go
import plotly.io as pio
from collections import deque

from backend.common.consts import Consts
from backend.modules.patterns import TripleTopPattern
from backend.modules.base_strategies import BasePatternStrategy
from backend.utils.rolling_window import rw_top, rw_bottom
from backend.utils.tt_utils import check_tt_pattern, check_tb_pattern


class TripleTopStrategy(BasePatternStrategy):
    def __init__(self, order=6, early_find=False):
        self.order = order
        self.early_find = early_find

    @property
    def name(self) -> str:
        return "Triple Top"

    def find_patterns(self, data: pd.DataFrame):
        # transformed_data = self.transform_data(raw_data=data)
        data_slice = data['close'].to_numpy()
        tt_patterns, tb_patterns = self._find_tt_logic(data=data_slice, order=self.order, early_find=self.early_find)
        return tt_patterns + tb_patterns

    def plot_pattern(self, price_df: pd.DataFrame, pat: TripleTopPattern):
        self._plot_tt_logic(price_df=price_df, pat=pat)

    def _find_tt_logic(self, data: np.array, order: int, early_find: bool = False):
        assert (order >= 1)

        last_is_top = False
        recent_extrema = deque(maxlen=5)
        recent_types = deque(maxlen=5)

        tt_lock = False
        tb_lock = False

        tb_patterns = []
        tt_patterns = []
        for i in range(len(data)):
            if rw_top(data, i, order):
                recent_extrema.append(i - order)
                recent_types.append(1)
                tb_lock = False
                last_is_top = True

            if rw_bottom(data, i, order):
                recent_extrema.append(i - order)
                recent_types.append(-1)
                tt_lock = False
                last_is_top = False

            if len(recent_extrema) < 5:
                continue

            tt_alternating = True
            tb_alternating = True

            if last_is_top:
                for j in range(2, 5):
                    if recent_types[j] == recent_types[j - 1]:
                        tb_alternating = False

                for j in range(1, 4):
                    if recent_types[j] == recent_types[j - 1]:
                        tt_alternating = False

                tb_extrema = list(recent_extrema)[1:5]
                tt_extrema = list(recent_extrema)[0:4]
            else:
                for j in range(2, 5):
                    if recent_types[j] == recent_types[j - 1]:
                        tt_alternating = False

                for j in range(1, 4):
                    if recent_types[j] == recent_types[j - 1]:
                        tb_alternating = False

                tb_extrema = list(recent_extrema)[0:4]
                tt_extrema = list(recent_extrema)[1:5]

            if tb_lock or not tb_alternating:
                tb_pat = None
            else:
                tb_pat = check_tb_pattern(tb_extrema, data, i, early_find)

            if tt_lock or not tt_alternating:
                tt_pat = None
            else:
                tt_pat = check_tt_pattern(tt_extrema, data, i, early_find)

            if tt_pat is not None:
                tt_lock = True
                tt_patterns.append(tt_pat)

            if tb_pat is not None:
                tb_lock = True
                tb_patterns.append(tb_pat)

        return tt_patterns, tb_patterns

    def _plot_tt_logic(self, price_df: pd.DataFrame, pat: TripleTopPattern, pad: int = 2):
        if pad < 0:
            pad = 0

        candle_data = price_df.copy()
        ticker = candle_data['ticker'].iloc[0]
        idx = candle_data.index
        candle_data = candle_data.iloc[pat.start_i - 20:pat.break_i + 1 + pad]
        neck_end_date = idx[pat.break_i]

        """Update df's label and sessions_num columns."""
        price_df.loc[neck_end_date, "label"] = 1 if pat.inverted else -1
        price_df.loc[neck_end_date, "sessions_num"] = pat.break_i - pat.start_i + 1


        fig = go.Figure()
        fig.add_trace(
            go.Candlestick(
                x=candle_data.index,
                open=candle_data['open'],
                high=candle_data['high'],
                low=candle_data['low'],
                close=candle_data['close'],
                name='Price',
                increasing_line_color='#26C281',
                decreasing_line_color='#E74C3C',
                increasing_fillcolor='rgba(38, 194, 129, 0.6)',
                decreasing_fillcolor='rgba(231, 76, 60, 0.6)',
                line=dict(width=1.2)
            )
        )

        l0 = [(idx[pat.start_i], pat.neck_start), (idx[pat.l_peak], pat.l_peak_p)]
        l1 = [(idx[pat.l_peak], pat.l_peak_p), (idx[pat.l_trough], pat.r_trough_p)]
        l2 = [(idx[pat.l_trough], pat.r_trough_p), (idx[pat.m_peak], pat.m_peak_p)]
        l3 = [(idx[pat.m_peak], pat.m_peak_p), (idx[pat.r_trough], pat.r_trough_p)]
        l4 = [(idx[pat.r_trough], pat.r_trough_p), (idx[pat.r_peak], pat.r_peak_p)]
        l5 = [(idx[pat.r_peak], pat.r_peak_p), (idx[pat.break_i], pat.neck_end)]
        neck = [(idx[pat.start_i], pat.neck_start), (idx[pat.break_i], pat.neck_end)]

        lines = [l0, l1, l2, l3, l4, l5, neck]
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#FF7675']
        line_names = ['Start→L.Shoulder', 'L.Shoulder→L.Armpit', 'L.Armpit→Head',
                      'Head→R.Armpit', 'R.Armpit→R.Shoulder', 'R.Shoulder→End', 'Neckline']

        for i, (line, color, name) in enumerate(zip(lines, colors, line_names)):
            fig.add_trace(
                go.Scatter(
                    x=[line[0][0], line[1][0]],
                    y=[line[0][1], line[1][1]],
                    mode='lines',
                    line=dict(
                        color=color,
                        width=3 if i != 6 else 2.5,
                        dash='solid' if i != 6 else 'dash'
                    ),
                    name=name,
                    showlegend=False,
                    hovertemplate=f'<b>{name}</b><br>Price: %{{y:.4f}}<br>Time: %{{x}}<extra></extra>'
                )
            )

        key_points_x = [idx[pat.l_peak], idx[pat.m_peak], idx[pat.r_peak]]
        key_points_y = [pat.l_peak_p, pat.m_peak_p, pat.r_peak_p]
        key_labels = ['Left Top', 'Middle Top', 'Right Top']
        key_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']

        for x, y, label, color in zip(key_points_x, key_points_y, key_labels, key_colors):
            # Điểm đánh dấu
            fig.add_trace(
                go.Scatter(
                    x=[x],
                    y=[y],
                    mode='markers',
                    marker=dict(
                        color=color,
                        size=15,
                        symbol='diamond',
                        line=dict(color='white', width=2)
                    ),
                    name=label,
                    showlegend=False,
                    hovertemplate=f'<b>{label}</b><br>Price: %{{y:.4f}}<br>Time: %{{x}}<extra></extra>'
                )
            )

            # Text annotation
            fig.add_annotation(
                x=x,
                y=y,
                text=label,
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor=color,
                ax=0,
                ay=-40,
                bgcolor=color,
                bordercolor='white',
                borderwidth=1,
                font=dict(color='white', size=10)
            )

        fig.update_layout(
            title=dict(
                text=f'{ticker} Triple Tops Pattern - {neck_end_date}',
                x=0.5,
                font=dict(size=24, color='white', family='Arial Black')
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
            height=650,  # Tỷ lệ vàng: 1.618
            width=1050,  # 650 * 1.618 ≈ 1050
            font=dict(color='white', size=12),
            plot_bgcolor='rgba(15,15,23,0.95)',
            paper_bgcolor='rgba(10,10,15,0.98)',
            dragmode='pan',
            hovermode='x unified'
        )

        # Cải thiện axes
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
            title='Price (Log Scale)',
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

        # Thêm watermark
        fig.add_annotation(
            text="Technical Analysis Dashboard",
            xref="paper", yref="paper",
            x=0.5, y=0.02,
            showarrow=False,
            font=dict(size=10, color="rgba(255,255,255,0.3)")
        )

        fig.show()
        # plot_dir = f"{Consts.TMP_DIR}/{ticker}"
        # os.makedirs(plot_dir, exist_ok=True)
        # fig.write_image(f"{plot_dir}/HS_{neck_end_date}.png")