import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import datetime, os
import seaborn as sns
import pdb

def window_fun(data, func, wnd_feat, fun_feat, val_lo, val_hi):
    ser = data[fun_feat][(data[wnd_feat] >= val_lo) &
                         (data[wnd_feat] <= val_hi)]
    return func(ser)

def roll_fun(data, func, wnd_feat, fun_feat, del_lo, del_hi):
    f = lambda x: window_fun(data, func, wnd_feat, fun_feat,
                             x - del_lo, x - del_hi)
    return data[wnd_feat].apply(f)

dat_dir = 'local_data/'
raw_fil = dat_dir + 'flights.csv'
shuf_fil = dat_dir + 'shuf_flights.csv'

# In[3]:

airlines = pd.read_csv(dat_dir + 'airlines.csv')
airports = pd.read_csv(dat_dir + 'airports.csv')

print('Shuffling and reading')
num_flights = 100000
shuffle = False
if shuffle:
    with open(raw_fil, 'r') as file:
        header = file.readline()
    with open(shuf_fil, 'w') as file:
        file.write(header)
    os.system('shuf -n {0} {1} >> {2}'.format(num_flights, raw_fil, shuf_fil))
    flights = pd.read_csv(shuf_fil, low_memory=False)
    os.remove(dat_dir + 'shuf_flights.csv')
else:
    flights = pd.read_csv(raw_fil, low_memory=False, nrows=num_flights)

airlines_dict = dict(zip(airlines['IATA_CODE'],airlines['AIRLINE']))

flights['DATE'] = pd.to_datetime(flights[['YEAR','MONTH','DAY']], yearfirst=True)
flights['AIRLINE_desc'] = flights['AIRLINE'].apply(lambda a: airlines_dict[a])

flights = flights[flights['DEPARTURE_DELAY'].notnull() & flights['ARRIVAL_DELAY'].notnull()]

ohare = flights[flights['ORIGIN_AIRPORT'] == 'ORD']

drop_feats = ['DEPARTURE_TIME', 'DEPARTURE_DELAY', 'TAXI_OUT', 'WHEELS_OFF', 'WHEELS_ON', 'AIR_TIME', 'TAXI_IN', 'DIVERTED', 'CANCELLED', 'CANCELLATION_REASON', 'AIR_SYSTEM_DELAY', 'SECURITY_DELAY', 'AIRLINE_DELAY', 'LATE_AIRCRAFT_DELAY', 'WEATHER_DELAY']
ohare = ohare.drop(drop_feats, axis=1)

janfirst = datetime.datetime(2015, 1, 1)
ohare['DEP_TIME'] = ohare.apply(lambda x: (datetime.datetime(
    x['YEAR'],
    x['MONTH'],
    x['DAY'],
    int(x['SCHEDULED_DEPARTURE'] / 100),
    x['SCHEDULED_DEPARTURE'] % 100) - janfirst) /
                                datetime.timedelta(minutes=1),
                                axis = 1)

# Time bins, what time did flights occur.  Used to identify traffic jams
t_midnight = 2400
t_step = 300
t_bins = np.arange(0, t_midnight + t_step, t_step)
t_labels = pd.cut(flights['SCHEDULED_DEPARTURE'], t_bins)

# Delay bins, used to visualize what effect other variables may have
h_labels = pd.qcut(delays, 10)

# traffic_rates = dict()

# for date_key, day in ohare.groupby(ohare['DATE']):
#     for time_key, hour in day.groupby(
#             np.round(day['SCHEDULED_DEPARTURE'], -2)):
#         traffic_rates[(date_key, time_key)] = np.median(hour['ARRIVAL_DELAY'])
# ohare['HOURLY_JAM'] = ohare.apply(lambda x : traffic_rates[(x['DATE'], np.round(x['SCHEDULED_DEPARTURE'], -2))], axis=1)

