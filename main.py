import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('london_cocoa.csv')

print(df.head())

df[['date', 'close']].plot()
df.plot()
plt.show()
