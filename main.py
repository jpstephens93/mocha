import pandas as pd


def sma(data, window):
    sma = data.rolling(window = window).mean()
    return sma


df = pd.read_csv('london_cocoa.csv', parse_dates=True, dayfirst=True, index_col='date').sort_index()

for col in df.columns:
    df[col] = df[col].fillna(method='ffill')

df.reset_index(inplace=True)

df['sma_20'] = sma(df['close'], 20)
df.tail()
