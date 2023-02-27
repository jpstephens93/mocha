import pandas as pd 
import matplotlib.pyplot as plt 
import math
from termcolor import colored as cl 
import numpy as np


def sma(data, window):
    sma = data.rolling(window=window).mean()
    return sma


def bb(data, sma, window):
    std = data.rolling(window=window).std()
    upper_bb = sma + std * 2
    lower_bb = sma - std * 2
    return upper_bb, lower_bb


df = pd.read_csv('london_cocoa.csv', parse_dates=True, dayfirst=True, index_col='date').sort_index()

for col in df.columns:
    df[col] = df[col].fillna(method='ffill')

df['close'].plot()
plt.show()

# SMA
df['sma_20'] = sma(df['close'], 20)
df.tail()

# BB
df['upper_bb'], df['lower_bb'] = bb(df['close'], df['sma_20'], 20)
df.tail()

df['close'].plot(label='CLOSE PRICES', color='skyblue')
df['upper_bb'].plot(label='UPPER BB 20', linestyle='--', linewidth=1, color='black')
df['sma_20'].plot(label='MIDDLE BB 20', linestyle = '--', linewidth=1.2, color='grey')
df['lower_bb'].plot(label='LOWER BB 20', linestyle = '--', linewidth=1, color='black')

plt.legend(loc='upper left')
plt.title('Cocoa Bollinger Bands')
plt.show()


def implement_bb_strategy(data, lower_bb, upper_bb):
    buy_price = []
    sell_price = []
    bb_signal = []
    signal = 0
    
    for i in range(1, len(data)):
        if data[i-1] > lower_bb[i-1] and data[i] < lower_bb[i]:
            if signal!=1:
                buy_price.append(data[i])
                sell_price.append(np.nan)
                signal=1
                bb_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                bb_signal.append(0)
        elif data[i-1] < upper_bb[i-1] and data[i] > upper_bb[i]:
            if signal!=-1:
                buy_price.append(np.nan)
                sell_price.append(data[i])
                signal=-1
                bb_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                bb_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            bb_signal.append(0)
            
    return buy_price, sell_price, bb_signal


buy_price, sell_price, bb_signal = implement_bb_strategy(data=df['close'], lower_bb=df['lower_bb'], upper_bb=df['upper_bb'])

df['close'].plot(label='Close Prices', alpha=0.3)
df['upper_bb'].plot(label='Upper BB', linestyle='--', linewidth=1, color='black')
df['sma_20'].plot(label='Middle BB', linestyle='--', linewidth=1.2, color='grey')
df['lower_bb'].plot(label='Lower BB', linestyle='--', linewidth=1, color='black')
plt.scatter(df.index, buy_price, marker='^', color='green', label='Buy', s=200)
plt.scatter(df.index, sell_price, marker='v', color='red', label='Sell', s=200)
plt.title('Cocoa Trading Signals')
plt.legend(loc='upper left')
plt.show()

position = []
for i in range(len(bb_signal)):
    if bb_signal[i] > 1:
        position.append(0)
    else:
        position.append(1)

for i in range(len(df['close'])-1):
    if bb_signal[i] == 1:
        position[i] = 1
    elif bb_signal[i] == -1:
        position[i] = 0
    else:
        position[i] = position[i-1]

upper_bb = df['upper_bb']
lower_bb = df['lower_bb']
close_price = df['close']
bb_signal = pd.DataFrame(bb_signal).rename(columns={0: 'bb_signal'}).set_index(df.index[1:])
position = pd.DataFrame(position).rename(columns={0: 'bb_position'}).set_index(df.index[1:])

frames = [close_price, upper_bb, lower_bb, bb_signal, position]
strategy = pd.concat(frames, join = 'inner', axis = 1)
strategy = strategy.reset_index().drop('date', axis = 1)

print(strategy.tail(7))

df_ret = pd.DataFrame(np.diff(df['close'])).rename(columns = {0:'returns'})
bb_strategy_ret = []

for i in range(len(df_ret)):
    try:
        returns = df_ret['returns'][i] * strategy['bb_position'][i]
        bb_strategy_ret.append(returns)
    except:
        pass

bb_strategy_ret_df = pd.DataFrame(bb_strategy_ret).rename(columns = {0:'bb_returns'})

investment_value = 100000
number_of_stocks = math.floor(investment_value / df['close'][-1])
bb_investment_ret = []

for i in range(len(bb_strategy_ret_df['bb_returns'])):
    returns = number_of_stocks * bb_strategy_ret_df['bb_returns'][i]
    bb_investment_ret.append(returns)

bb_investment_ret_df = pd.DataFrame(bb_investment_ret).rename(columns = {0:'investment_returns'})
total_investment_ret = round(sum(bb_investment_ret_df['investment_returns']), 2)
profit_percentage = math.floor((total_investment_ret / investment_value) * 100)

print(cl('Profit gained from the BB strategy by investing $100k in df : {}'.format(total_investment_ret), attrs = ['bold']))
print(cl('Profit percentage of the BB strategy : {}%'.format(profit_percentage), attrs = ['bold']))
