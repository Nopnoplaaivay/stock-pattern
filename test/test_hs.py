import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data import generate_sample_df_with_pattern
from src.patterns import detect_head_shoulder
from plot import plot_head_shoulder


# Example usage
# Assuming `df` is the DataFrame with the detected patterns
df = generate_sample_df_with_pattern("Head and Shoulder")
df = detect_head_shoulder(df)
plot_head_shoulder(df)
