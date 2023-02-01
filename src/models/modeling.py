import os
from typing import Union
import pickle

import pandas as pd
import numpy as np

import lightgbm as lgb
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error


def modeling_lightgbm(X_train: pd.DataFrame, y_train: pd.DataFrame, params: dict):
    """lightgbmモデルを使用して予測モデルを作成する関数.

    評価指標は二乗平均兵香港誤差(RMSE)を使用している

    Args:
        X_train (pd.DataFrame): 説明変数データ
        y_train (pd.DataFrame): 目的変数データ
        params (dict): 学習に使用するパラメータ

    Returns:
        dict: 学習の結果

        - X_train: 説明変数データ
        - y_train: 目的変数データ
        - model: 説明変数データ
        - lgb_results: 学習ログ
        - loss_train: 学習ロス
    """
    X_train = X_train.copy()
    y_train = y_train.copy()
    # データセットを登録
    lgb_train = lgb.Dataset(X_train, y_train, free_raw_data=False)
    lgb_results = {}                                    # 学習の履歴を入れる入物
    model = lgb.train(
            params=params,
            train_set=lgb_train,
            valid_sets=[lgb_train],
            valid_names=['Train'],
            verbose_eval=-1,
            evals_result=lgb_results,
            callbacks=[
                lgb.early_stopping(stopping_rounds=30, verbose=False), 
                lgb.log_evaluation(0)
                ]
        )
    loss_train = lgb_results['Train']['rmse']
    return {
        "X_train": X_train,
        "y_train": y_train,
        "model": model,
        "lgb_results": lgb_results,
        "loss_train": loss_train
    }


def save_model(model: lgb.basic.Booster, save_file_name: Union[str, os.PathLike]):
    """学習済モデルをpickleで保存する関数.

    Args:
        model (lgb.basic.Booster): 学習済モデル
        save_file_name (Union[str, os.pathlike]): 保存するファイルpath

    Returns:
        str: "model saved"
    """
    print("SAVE_MODEL: {}".format(save_file_name))
    pickle.dump(model, open(save_file_name, 'wb'))
    return "model saved"


def modeling_lightgbm_with_cv(X: pd.DataFrame, y: pd.DataFrame, params: dict):
    """クロスバリデーションを使用したlightgbmでの学習を行う.

    Args:
        X (pd.DataFrame): 説明変数データ
        y (pd.DataFrame): 目的変数データ
        params (dict): 学習パラメータ

    Returns:
        dict: _description_

        - params: 学習に使用したパラメータ
        - cv_score: cvスコア。各学習で算出したスコアの平均値
        - models: 各学習で作成したモデルのリスト
    """
    FOLD = 3
    VERBOSE_EVAL = -1

    valid_scores = []
    models = []

    kf = KFold(n_splits=FOLD, shuffle=False)

    X = X.to_numpy()
    y = y.to_numpy()

    for _, (train_indices, valid_indices) in enumerate(kf.split(X)):
        X_train, X_valid = X[train_indices], X[valid_indices]
        y_train, y_valid = y[train_indices], y[valid_indices]
        lgb_train = lgb.Dataset(X_train, y_train)
        lgb_eval = lgb.Dataset(X_valid, y_valid)

        model = lgb.train(
            params,
            lgb_train,
            valid_sets=[lgb_train, lgb_eval],
            verbose_eval=VERBOSE_EVAL,
            callbacks=[
                lgb.early_stopping(stopping_rounds=30, verbose=False), 
                lgb.log_evaluation(0)
                ]
        )

        y_valid_pred = model.predict(X_valid)
        score = mean_squared_error(y_valid, y_valid_pred)
        valid_scores.append(score)

        models.append(model)

    cv_score = np.mean(valid_scores)
    return {
        "params": params,
        "cv_score": cv_score,
        "models": models
    }


def make_params_list():
    """lightgbmで使用するパラメータの候補をリストで出力する関数.

    Returns:
        list: lightgbmのパラメータの候補リスト
    """
    learning_rate_list = [x * 0.01 for x in [1,5,10]]
    num_iteration_list = [3000]
    max_depth_list = [3, 5, 7]
    
    params_list = []
    for lr in learning_rate_list:
        for ni in num_iteration_list:
            for ml in max_depth_list:
                params = {
                    'verbose': -1,
                    'task': 'train',              
                    'boosting_type': 'gbdt',      
                    'objective': 'regression',    
                    'metric': 'rmse',             
                    'learning_rate': lr,
                    'num_iteration': ni,
                    "max_depth": ml,
                }
                params_list.append(params)
    return params_list