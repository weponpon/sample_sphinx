from typing import Union
import pandas as pd


def extract_cols(df: pd.DataFrame, c: Union[str, list]):
    """データからカラムを指定して取り出す関数.

    Args:
        df (pd.DataFrame): 対象のデータ
        c (Union[str, list]): 抽出したいカラム

    Returns:
        pd.DataFrame: 対象のデータから指定したカラムで抽出したデータ
    """
    df_ = df.copy()
    if type(c)==list:
        c_df = df_.loc[:, c].copy()
    elif type(c)==str:
        c_df = df_.loc[:, [c]].copy()
    else:
        c_df = df_.copy()
        print("カラムを確認してください")
    return c_df