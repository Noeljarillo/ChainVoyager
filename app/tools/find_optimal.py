import sqlite3
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

def get_optimal_pools(
    db_path,
    exposure=None,
    stablecoin=None,
    chain=None,
    ilRisk=None,
    project=None,
    symbol=None,
    top_n=5
):
    """
    Retrieves and processes pool data, trains a Random Forest model to predict APY,
    and returns the top N pools based on predicted APY.
    """

    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM pools"

    conditions = []
    params = []

    if exposure:
        conditions.append("exposure = ?")
        params.append(exposure)
    if stablecoin is not None:
        conditions.append("stablecoin = ?")
        params.append('True' if stablecoin else 'False')
    if chain:
        conditions.append("chain = ?")
        params.append(chain)
    if ilRisk:
        conditions.append("ilRisk = ?")
        params.append(ilRisk)
    if project:
        conditions.append("project = ?")
        params.append(project)
    if symbol:
        conditions.append("symbol = ?")
        params.append(symbol)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    df = pd.read_sql_query(query, conn, params=params)
    conn.close()

    if df.empty:
        print("No data found for the given filters.")
        return pd.DataFrame()

    print(f"Retrieved {len(df)} pools with the applied filters.")

    numerical_cols = [
        'apyBase', 'apyBase7d', 'apyBaseInception',
        'apyMean30d', 'apyPct1D', 'apyPct7D', 'apyPct30D',
        'apyReward', 'apy',
        'count', 'mu', 'sigma'
    ]

    for col in numerical_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.dropna(subset=['apy'])

    categorical_cols = [
        'chain', 'project', 'symbol', 'exposure',
        'ilRisk', 'predictions_predictedClass'
    ]
    binary_cols = ['stablecoin', 'outlier']

    reward_tokens_cols = [col for col in df.columns if col.startswith('rewardTokens_')]
    underlying_tokens_cols = [col for col in df.columns if col.startswith('underlyingTokens_')]

    df['num_rewardTokens'] = df[reward_tokens_cols].notnull().sum(axis=1)
    df['num_underlyingTokens'] = df[underlying_tokens_cols].notnull().sum(axis=1)

    for col in binary_cols:
        df[col] = df[col].replace({'True': 1, 'False': 0}).astype(int)

    feature_cols = numerical_cols + categorical_cols + ['num_rewardTokens', 'num_underlyingTokens'] + binary_cols

    df_features = df[feature_cols].copy()

    y = df_features['apy']
    X = df_features.drop('apy', axis=1)

    numerical_features = [
        'apyBase', 'apyBase7d', 'apyBaseInception',
        'apyMean30d', 'apyPct1D', 'apyPct7D', 'apyPct30D',
        'apyReward', 'count', 'mu', 'sigma',
        'num_rewardTokens', 'num_underlyingTokens'
    ]
    categorical_features = [
        'chain', 'project', 'symbol', 'exposure',
        'ilRisk', 'predictions_predictedClass'
    ]
    binary_features = ['stablecoin', 'outlier']

    numerical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median'))
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    binary_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value=0)),
        ('to_numeric', FunctionTransformer(lambda x: x.astype(int)))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features),
            ('bin', binary_transformer, binary_features)
        ]
    )

    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    model.fit(X, y)
    y_pred = model.predict(X)
    df['predicted_apy'] = y_pred
    df_sorted = df.sort_values(by='predicted_apy', ascending=False)
    top_pools = df_sorted.head(top_n)
    relevant_columns = [
        'pool', 'chain', 'project', 'symbol', 'apy', 'predicted_apy',
        'exposure', 'stablecoin', 'tvlUsd', 'mu', 'sigma',
        'num_rewardTokens', 'num_underlyingTokens', 'count'
    ]
    relevant_columns = [col for col in relevant_columns if col in top_pools.columns]

    return top_pools[relevant_columns]
