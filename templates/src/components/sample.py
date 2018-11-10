# -*- coding: utf-8 -*-
#

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from original_tools import plot

if __name__ == "__main__":
    # データ読み込み部分
    # データの形状は、以下の通り(" | "は実際はタブ)
    # user_id | store_id | user_feature1 | user_feature2 | store_feature1 | store_feature2 | num_bought | spent_total
    # 1234 | 1111 | 50 | 3.8 | 1300 | 4.8 | 1 | 1031
    # 2345 | 2222 | 30 | 1.1 | 670 | 10.2 | 2 | 8820
    # ...
    df = pd.read_csv("foo_bar.tsv", sep="\t")

    # 購入金額(spent_total)の分布を可視化
    # 実装済みのplot関数で描画し、ファイルに出力
    # plot(data_list, graph_title, file_name)
    plot(df.spent_total.values, "購入金額の分布", "histgram_of_spent_total.html")

    # 可視化した分布から決めた閾値100,000円以下に絞ったデータを利用
    df_without_outliers = df[df.spent_total <= 1000000]

    # 上記条件に絞って購入商品数(num_bought)のHistogramを可視化
    plot(df_without_outliers.num_bought.values, "購入金額500,000円以下のときの購入商品数分布",
         "num_bought_distribution_whose_total_spent_leq_100000.html")

    # ユーザーの特徴量と店の特徴量から購入金額を学習したいので特徴量行列を作成
    # 目的変数である購入金額のカラムを除去
    raw_features = df_without_outliers.drop(["spent_total"], axis=1)

    # 特徴量の標準化
    ss = StandardScaler()
    standardized = ss.fit_transform(raw_features.values)

    # Training dataとTest dataに分離
    X_train, X_test, y_train, y_test = train_test_split(standardized, df_without_outliers.spent_total.values)

    # 購入金額(spent_total)の学習と予測
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    prediction = lr.predict(X_test)

    # 精度評価
    print(f"MSE: {mean_squared_error(y_test, prediction)}")

    # 各特徴量の影響度を表示
    for n, c in zip(raw_features.columns, lr.coef_):
        print(f"{n} : {c}")
