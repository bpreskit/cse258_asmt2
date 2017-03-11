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
flights = pd.read_csv(dat_dir + '/shuf_flights.csv', low_memory=False)
os.remove(dat_dir + 'shuf_flights.csv')

airlines_dict = dict(zip(airlines['IATA_CODE'],airlines['AIRLINE']))

flights['DATE'] = pd.to_datetime(flights[['YEAR','MONTH','DAY']], yearfirst=True)
flights['AIRLINE_desc'] = flights['AIRLINE'].apply(lambda a: airlines_dict[a])

flights = flights[flights['DEPARTURE_DELAY'].notnull() & flights['ARRIVAL_DELAY'].notnull()]

