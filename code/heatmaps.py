import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import datetime, os
import seaborn as sns
import pdb

dat_dir = 'local_data/'
raw_fil = dat_dir + 'flights.csv'
shuf_fil = dat_dir + 'shuf_flights.csv'

# In[3]:

airlines = pd.read_csv(dat_dir + 'airlines.csv')
airports = pd.read_csv(dat_dir + 'airports.csv')

print('Shuffling and reading')
num_flights = 100000
with open(raw_fil, 'r') as file:
    header = file.readline()
with open(shuf_fil, 'w') as file:
    file.write(header)
os.system('shuf -n {0} {1} >> {2}'.format(num_flights, raw_fil, shuf_fil))
flights = pd.read_csv(shuf_fil, low_memory=False)
os.remove(dat_dir + 'shuf_flights.csv')

airlines_dict = dict(zip(airlines['IATA_CODE'],airlines['AIRLINE']))

flights['DATE'] = pd.to_datetime(flights[['YEAR','MONTH','DAY']], yearfirst=True)
flights['AIRLINE_desc'] = flights['AIRLINE'].apply(lambda a: airlines_dict[a])

flights = flights[flights['DEPARTURE_DELAY'].notnull() & flights['ARRIVAL_DELAY'].notnull()]

delays = flights['ARRIVAL_DELAY']

print('Getting bins')
# 4 quartiles of delays, used to show color-coded hist of aggregated
# delay data
q_labels, bins = pd.qcut(delays, 4, retbins=True)
hbins = list(bins) + list(np.linspace(delays.min(), delays.max(), 200))
hbins.sort()
quarts = delays.groupby(q_labels)

# Time bins, what time did flights occur.  Used to identify traffic jams
t_midnight = 2400
t_step = 300
t_bins = np.arange(0, t_midnight + t_step, t_step)
t_labels = pd.cut(flights['SCHEDULED_DEPARTURE'], t_bins)

# Delay bins, used to visualize what effect other variables may have
h_labels = pd.qcut(delays, 10)

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

fig = plt.figure()
hmap_del_time = pd.crosstab(index=h_labels,
                            columns=t_labels,
                            normalize='columns')
ax = sns.heatmap(hmap_del_time, linewidths=0.5)
plt.setp(ax.get_yticklabels(), rotation=0)
fig.show()
