import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import datetime, os
import seaborn as sns
import pdb

dat_dir = 'local_data/'

# In[3]:

airlines = pd.read_csv(dat_dir + 'airlines.csv')
airports = pd.read_csv(dat_dir + 'airports.csv')

num_flights = 100000
os.system('shuf -n {0} {1}flights.csv > '
          '{2}shuf_flights.csv'.format(num_flights, dat_dir, dat_dir))
flights = pd.read_csv(dat_dir + '/shuf_flights.csv', low_memory=False)
os.remove(dat_dir + 'shuf_flights.csv')

airlines_dict = dict(zip(airlines['IATA_CODE'],airlines['AIRLINE']))

flights['DATE'] = pd.to_datetime(flights[['YEAR','MONTH','DAY']], yearfirst=True)
flights['AIRLINE_desc'] = flights['AIRLINE'].apply(lambda a: airlines_dict[a])

flights = flights[flights['DEPARTURE_DELAY'].notnull() & flights['ARRIVAL_DELAY'].notnull()]

delays = flights['ARRIVAL_DELAY'].dropna()

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

plt.title('Quartiles of Arrival Delay Times')
fig.show()

fig = plt.figure()
sns.distplot((flights['ARRIVAL_DELAY'] - flights['DEPARTURE_DELAY']).dropna(), kde=False)
plt.title('Histogram of Arr. Delay - Dep. Delay')
fig.show()

h_labels = pd.qcut(delays, 10)
hmap_delay_airline = flights.pivot_table(values=h_labels, index=h_labels, columns=['AIRLINE'], aggfunc=lambda x: x.count())

fig = plt.figure()
hmap_del_airline = pd.crosstab(index=h_labels,
                               columns=flights['AIRLINE'],
                               normalize='columns')
ax = sns.heatmap(hmap_del_airline, linewidths=0.5)
plt.setp(ax.get_yticklabels(), rotation=0)
fig.show()

# fig = plt.figure()
# hmap_del_month = pd.crosstab(index=h_labels,
#                              columns=flights['AIRLINES'],
#                              normalize='columns')
# ax = sns.heatmap(hmap_del_month, linewidths=0.5)
# plt.setp(ax.get_yticklabels(), rotation=0)
# fig.show()

fig = plt.figure()
hmap_del_dow = pd.crosstab(index=h_labels,
                           columns=flights['DAY_OF_WEEK'],
                           normalize='columns')
ax = sns.heatmap(hmap_del_dow, linewidths=0.5)
plt.setp(ax.get_yticklabels(), rotation=0)
fig.show()
