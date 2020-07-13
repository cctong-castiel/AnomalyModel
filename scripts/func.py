import numpy as np 
import pandas as pd

def df_preprocess(df, t_period, comment_f):

    # pandas datetime
    date_col = 'post_timestamp'
    df[date_col] = pd.to_datetime(df[date_col])
    df['period'] = df[date_col].dt.to_period(t_period)

    # select is comment
    if comment_f != None:
        df = df.loc[df.is_comment == comment_f]

    return df
