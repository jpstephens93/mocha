import pandas as pd
import json

f = open('api.json')
data = json.load(f)

timestamps = []
bids = []
asks = []
volume = []

i = 0
while i >= 0:
    try:
        for x in data['intervalsDataPoints'][i]['dataPoints']:
            print(x)
            try:
                if x['tickPrice']['bid'] != "":
                    timestamps.append(x['timestamp'])
                    bids.append(x['tickPrice']['bid'])
                    asks.append(x['tickPrice']['ask'])
                    volume.append(x['lastTradedVolume'])
            except KeyError:
                pass
            i += 1
    except IndexError:
        i = -1

len_ts = len(timestamps)
len_bid = len(bids)
len_ask = len(asks)
len_vol = len(volume)

assert (len_ts == len_ask) and (len_ts == len_bid) and (len_ts == len_vol) and (len_bid == len_ask) and (len_bid == len_vol) and (len_ask == len_vol), "Check list lengths"

df = pd.DataFrame(
    {
        'timestamp': timestamps,
        'bid': bids,
        'ask': asks,
        'volume': volume
    }
)
