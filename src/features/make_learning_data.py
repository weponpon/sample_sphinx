import pandas as pd

def make_date_hour(date: int):
    """入力されたdateについて、24時間分のhour列を作成したデータを作成する.

    Args:
        date (int): 日付

    Returns:
        pd.DataFrame: 日付(date)と時間(hour)をカラムに持つデータ
    """
    date_hour = []

    for h in range(0, 24):
        date_hour.append({
            "date": int(date),
            "hour": int(h),
        })
    date_hour_df = pd.DataFrame(date_hour)
    return date_hour_df


def make_learning_data(df: pd.DataFrame, expl_cols:list, obj_cols: list):
    """データを説明変数と目的変数に分割し、辞書型で返す関数.

    Args:
        df (pd.DataFrame): 対象のデータ
        expl_cols (list): 説明変数のリスト
        obj_cols (list): 目的変数のリスト

    Returns:
        dict: 説明変数"X"と目的変数"y"とする辞書
    """
    X = df.loc[:, expl_cols].copy()
    y = df.loc[:, obj_cols].copy()
    return {
        "X": X,
        "y": y
    }