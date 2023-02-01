import pandas as pd
import numpy as np

def value_to_float(df: pd.DataFrame, col: str):
    """データのcolについて数字でないものをnp.nanに置き換える関数.

    Args:
        df (pd.DataFrame): 対象のデータ
        col (str): 対象のカラム

    Returns:
        pd.DataFrame: colについて数字のみに修正したデータ
    """
    df_ = df.copy()
    not_numeric_list = df_[
        pd.to_numeric(df[col], errors='coerce').notna()==False
        ][col].unique().tolist()
    df_[col] = df_[col].replace(
        dict(zip(not_numeric_list, [np.nan for _ in range(len(not_numeric_list))]))
    ).astype(float)
    return df_


def missing_value_handling(df: pd.DataFrame, expl_cols: list, obj_col: str, contains_null_rate: float =0.1):
    """欠損値処理の関数.

    目的変数にある欠損を削除し、残ったデータについて欠損数を調べる。欠損数の割合が、(残った目的変数の長さ)×(contains_null_rate)以下のカラムのみ使用する。使用するカラムについて、列毎に平均値を計算し欠損補完を行う。

    Args:
        df (pd.DataFrame): 対象のデータ
        expl_cols (list): 説明変数リスト
        obj_col (str): 目的変数
        contains_null_rate (float): 目的変数に含まれる欠損数を許容する割合. Defaults to 0.1.

    Returns:
        dict: 欠損値処理結果の辞書

        - processed_df: 処理済のデータ
        - use_cols: 欠損補完を行った際に使用したカラム
    """
    # 目的変数の欠損値をドロップ
    obj_notnull_index = df.loc[:, [obj_col]].dropna().index
    # 目的変数のインデックスで説明変数データを抽出
    expl_notnull_df = df.loc[obj_notnull_index, expl_cols].copy()
    # 欠損値が目的変数の長さ×contains_null_rateの数以下の説明変数を取得
    use_cols = expl_notnull_df.columns[expl_notnull_df.isna().sum() <= len(obj_notnull_index) * contains_null_rate].to_list()
    # 欠損値を平均で補完
    use_df = df.loc[obj_notnull_index, [obj_col]+use_cols]
    use_df.fillna(use_df.mean(), inplace=True)
    return {"processed_df": use_df, "use_cols": use_cols}
