import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data import generate_sample_df_with_pattern
from pattern import detect_head_shoulder




def test_detect_head_shoulder():
    # Generate data with head and shoulder pattern
    df_head_shoulder = generate_sample_df_with_pattern("Head and Shoulder")
    df_inv_shoulder = generate_sample_df_with_pattern("Inverse Head and Shoulder")
    df_with_detection = detect_head_shoulder(df_head_shoulder)
    df_with_inv_detection = detect_head_shoulder(df_inv_shoulder)
    assert "Head and Shoulder" in df_with_detection['head_shoulder_pattern'].values
    assert "Inverse Head and Shoulder" in df_with_inv_detection['head_shoulder_pattern'].values


