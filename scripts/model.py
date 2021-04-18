import numpy as np
import pandas as pd
import pickle
import logging
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

def m_pipeline(matrix):

    """To train isolation model
    Input: a matrix of numerical data
    Output: trained model"""

    if_value = 0.01
    feature_col = list(matrix.columns)
    feature_col.remove("post_timestamp")
    feature_col.remove("period")
    dict_k = dict.fromkeys(feature_col, 'mean')
    df_ = matrix.groupby(by='period').agg(dict_k)

    # StandardScaler
    logging.info("StandardScaler")
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df_)

    # Isolation Forest
    logging.info("Isolation Forest")
    model = IsolationForest(contamination = if_value)
    model.fit(scaled_data)

    # prediction
    logging.info("prediction")
    pred = model.predict(scaled_data)
    df_['pred'] = pred
    df_['pred'] = df_['pred'].map({1:0, -1:1})
    df_out = df_.loc[df_.pred == 1]

    return df_out

