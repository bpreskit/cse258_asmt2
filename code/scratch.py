import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import datetime

dat_dir = 'local_data/'

# In[3]:

num_flights = 10000
airlines = pd.read_csv(dat_dir + 'airlines.csv')
airports = pd.read_csv(dat_dir + 'airports.csv')
flights = pd.read_csv(dat_dir + '/flights.csv',
                      low_memory=False, nrows=num_flights)

airlines_dict = dict(zip(airlines['IATA_CODE'],airlines['AIRLINE']))

flights['DATE'] = pd.to_datetime(flights[['YEAR','MONTH','DAY']], yearfirst=True)
flights['AIRLINE_desc'] = flights['AIRLINE'].apply(lambda a: airlines_dict[a])

print('Trying to plot')
flights.groupby('DEPARTURE_DELAY')['DEPARTURE_DELAY'].hist()
