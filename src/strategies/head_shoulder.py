import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
from collections import deque


from src.patterns import HSPattern
from src.base_strategies import BasePatternStrategy
from src.utils.rolling_window import rw_top, rw_bottom
from src.utils.hs_utils import check_hs_pattern, check_ihs_pattern


class HeadAndShouldersStrategy(BasePatternStrategy):
    def __init__(self, order=6, early_find=False):
        self.order = order
        self.early_find = early_find

    @property
    def name(self) -> str:
        return "Head and Shoulders"

    def transform_data(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        data = raw_data.copy()
        data['date'] = data['date'].astype('datetime64[s]')
        data = data.set_index('date')
        data = np.log(data)
        return data

    def find_patterns(self, data: pd.DataFrame):
        transformed_data = self.transform_data(raw_data=data)
        data_slice = transformed_data['close'].to_numpy()
        hs_patterns, ihs_patterns = self._find_hs_logic(data=data_slice, order=self.order, early_find=self.early_find)
        return hs_patterns + ihs_patterns

    def plot_pattern(self, candle_data: pd.DataFrame, pat: HSPattern):
        self._plot_hs_logic(candle_data=candle_data, pat=pat)

    def _find_hs_logic(self, data: np.array, order: int, early_find: bool = False):
        assert (order >= 1)

        last_is_top = False
        recent_extrema = deque(maxlen=5)
        recent_types = deque(maxlen=5)

        hs_lock = False
        ihs_lock = False

        ihs_patterns = []  # Inverted (bullish)
        hs_patterns = []  # Regular (bearish)
        for i in range(len(data)):
            if rw_top(data, i, order):
                recent_extrema.append(i - order)
                recent_types.append(1)
                ihs_lock = False
                last_is_top = True

            if rw_bottom(data, i, order):
                recent_extrema.append(i - order)
                recent_types.append(-1)
                hs_lock = False
                last_is_top = False

            if len(recent_extrema) < 5:
                continue

            hs_alternating = True
            ihs_alternating = True

            if last_is_top:
                for j in range(2, 5):
                    if recent_types[j] == recent_types[j - 1]:
                        ihs_alternating = False

                for j in range(1, 4):
                    if recent_types[j] == recent_types[j - 1]:
                        hs_alternating = False

                ihs_extrema = list(recent_extrema)[1:5]
                hs_extrema = list(recent_extrema)[0:4]
            else:

                for j in range(2, 5):
                    if recent_types[j] == recent_types[j - 1]:
                        hs_alternating = False

                for j in range(1, 4):
                    if recent_types[j] == recent_types[j - 1]:
                        ihs_alternating = False

                ihs_extrema = list(recent_extrema)[0:4]
                hs_extrema = list(recent_extrema)[1:5]

            if ihs_lock or not ihs_alternating:
                ihs_pat = None
            else:
                ihs_pat = check_ihs_pattern(ihs_extrema, data, i, early_find)

            if hs_lock or not hs_alternating:
                hs_pat = None
            else:
                hs_pat = check_hs_pattern(hs_extrema, data, i, early_find)

            if hs_pat is not None:
                hs_lock = True
                hs_patterns.append(hs_pat)

            if ihs_pat is not None:
                ihs_lock = True
                ihs_patterns.append(ihs_pat)

        return hs_patterns, ihs_patterns

    def _plot_hs_logic(self, candle_data: pd.DataFrame, pat: HSPattern, pad: int = 2):
        if pad < 0:
            pad = 0

        candle_data = self.transform_data(candle_data)

        idx = candle_data.index
        data = candle_data.iloc[pat.start_i:pat.break_i + 1 + pad]

        plt.style.use('dark_background')
        fig = plt.gcf()
        ax = fig.gca()

        l0 = [(idx[pat.start_i], pat.neck_start), (idx[pat.l_shoulder], pat.l_shoulder_p)]
        l1 = [(idx[pat.l_shoulder], pat.l_shoulder_p), (idx[pat.l_armpit], pat.l_armpit_p)]
        l2 = [(idx[pat.l_armpit], pat.l_armpit_p), (idx[pat.head], pat.head_p)]
        l3 = [(idx[pat.head], pat.head_p), (idx[pat.r_armpit], pat.r_armpit_p)]
        l4 = [(idx[pat.r_armpit], pat.r_armpit_p), (idx[pat.r_shoulder], pat.r_shoulder_p)]
        l5 = [(idx[pat.r_shoulder], pat.r_shoulder_p), (idx[pat.break_i], pat.neck_end)]
        neck = [(idx[pat.start_i], pat.neck_start), (idx[pat.break_i], pat.neck_end)]

        mpf.plot(data, alines=dict(alines=[l0, l1, l2, l3, l4, l5, neck], colors=['w', 'w', 'w', 'w', 'w', 'w', 'r']),
                 type='candle', style='charles', ax=ax)
        x = len(data) // 2 - len(data) * 0.1
        if pat.inverted:
            y = pat.head_p + pat.head_height * 1.25
        else:
            y = pat.head_p - pat.head_height * 1.25

        plt.show()

