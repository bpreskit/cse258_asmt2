import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
import pdb

dat_dir = 'local_data/'

# In[3]:

num_flights = 100000
airlines = pd.read_csv(dat_dir + 'airlines.csv')
airports = pd.read_csv(dat_dir + 'airports.csv')
flights = pd.read_csv(dat_dir + '/flights.csv',
                      low_memory=False, nrows=num_flights)

airlines_dict = dict(zip(airlines['IATA_CODE'],airlines['AIRLINE']))

flights['DATE'] = pd.to_datetime(flights[['YEAR','MONTH','DAY']], yearfirst=True)
flights['AIRLINE_desc'] = flights['AIRLINE'].apply(lambda a: airlines_dict[a])

delays = flights['DEPARTURE_DELAY'].dropna()

print('Getting bins')
q_labels, bins = pd.qcut(delays, 4, retbins=True)
hbins = list(bins) + list(np.linspace(delays.min(), delays.max(), 200))
hbins.sort()

#pdb.set_trace()
quarts = delays.groupby(q_labels)

print('Trying to plot')
fig = plt.figure()
for (i, q) in enumerate(quarts):
    print(len(q[1]))
    sns.distplot(q[1],
                 bins=hbins[hbins.index(bins[i]):hbins.index(bins[i+1]) + 1],
                 kde=False)

plt.title('Quartiles of Departure Delay Times')
fig.show()

fig = plt.figure()
sns.distplot((flights['ARRIVAL_DELAY'] - flights['DEPARTURE_DELAY']).dropna(), kde=False)
plt.title('Histogram of Arr. Delay - Dep. Delay')
fig.show()
