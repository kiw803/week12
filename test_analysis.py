import pandas as pd

from analysis import 정제, 반별평균


scores = 정제(pd.read_csv("scores_2026.csv"))
mini = 정제(pd.read_csv("mini.csv"))


def test_scores_2026_cleaned_row_count():
    assert len(scores) == 100


def test_scores_2026_cleaned_classes():
    assert set(scores["반"].unique()) == {"1반", "2반"}


def test_class_score_sum_equals_total_score_sum():
    assert scores.groupby("반")["점수"].sum().sum() == scores["점수"].sum()


def test_mini_class_1_average():
    assert 반별평균(mini)["1반"] == 80.0