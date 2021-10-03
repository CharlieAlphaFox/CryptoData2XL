#!/usr/bin/python3
from pyti.smoothed_moving_average import smoothed_moving_average as sma
from binance.client import Client
import pandas_ta as ta
from time import sleep
import pandas as pd
import numpy as np
import time
import keys

client = Client(api_key=keys.Pkey, api_secret=keys.Skey)

pairs = ['BTC/USD', 'ETH/USD', 'LINK/USD', 'LTC/USD', 'BCH/USD', 'LINA/USD', 'BNB/USD', 'MKR/USD', 'SOL/USD',
'OCEAN/USD', 'UNI/USD', 'KNC/USD', 'DOT/USD', 'COMP/USD', 'TOMO/USD', 'SUSHI/USD', 'ZIL/USD', 'MATIC/USD',
# ADA, ORN, GRT, CAKE, 1NCH, AAVE, YFI, REEF, COTI, etc? 
]

def Trend(pair):
    global pairsmas
    altc = pair[:-4]
    ppair = str(f'{altc}USDT')
    ticker = client.get_symbol_ticker(symbol=ppair)
    price = ticker['price']
    print(f'\nStart________Gathering Close prices of {altc}______\n')
    candle_no = 336 # 7 days back for a weekly VWAP Pivot
    interval = Client.KLINE_INTERVAL_30MINUTE
    candles = client.get_klines(symbol=ppair, interval=interval, limit=candle_no)
    df = pd.DataFrame(data=candles)
    # New lists of data
    open = df.iloc[:,1].astype(float)
    high = df.iloc[:,2].astype(float)
    low = df.iloc[:,3].astype(float)
    close = df.iloc[:,4].astype(float)
    volume = df.iloc[:,5].astype(float)
    no_ofTrades = df.iloc[0:100,[8]]  #This returns as an integer from the API and the last value is incomplete per interval as is ongoing
    # Removes the columns to not use here:
    # df.pop(0)  # Open time
    df.pop(6)  # Close time
    df.pop(7)  # Quote asset volume
    df.pop(9)  # Taker buy base asset volume
    df.pop(10) # Taker buy quote asset volume
    df.pop(11) # Can be ignored
    df.columns = ['Time','Open','High','Low','Close','Volume','Trades'] #Titles the colms
    df['Time'] = pd.to_datetime(df['Time'] * 1000000, infer_datetime_format=True)

    # Calculates Smoothed moving avgs

    pairsmas = sma(close,30)
    sleep(2.3)
    return pairsmas


pcount = 0
closes = []
dfr = pd.DataFrame([])
for pair in pairs:
    pcount +=1
    pairsmas = Trend(pair)
    closes.append(pairsmas)
    # smaslist.append(pairsmas)
    # pairsmas = np.array(pairsmas)

# dfr = dfr.append(pd.DataFrame(pairsmas), ignore_index=True)
for close, pair in zip(closes, pairs):
    dfr = dfr.append(pd.DataFrame({f'{pair}': close}), ignore_index=True)
# dfr.dropna()
file = dfr.to_csv('allcloses.csv')
