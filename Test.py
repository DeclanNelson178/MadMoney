# API KEY: 86UKVGO0J2S8VMBN
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
ticker = 'MSFT'

ts = TimeSeries(key='YOUR_API_KEY', output_format='pandas')
data = pd.DataFrame()
data, meta_data = ts.get_daily(symbol=ticker, outputsize='compact')


print("----Yesterday's close price----")
print(data['4. close'][-2])