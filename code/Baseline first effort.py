
# coding: utf-8

# In[ ]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn.linear_model
import sklearn.svm
from sys import getsizeof
import sklearn.utils
import random
import sklearn.metrics


# In[ ]:

get_ipython().run_cell_magic('time', '', '#Sample ~s values from flights\nn = 5800000\ns = 500009\nskip = np.random.choice(np.arange(1, n), n-s, replace = False)\nflights = pd.read_csv(r"C:\\Users\\Garrett Williams\\Desktop\\flights.csv", skiprows = skip)\n#airports = pd.read_csv(r"C:\\Users\\Garrett\\Desktop\\airports.csv")\n#airlines = pd.read_csv(r"C:\\Users\\Garrett\\Desktop\\airlines.csv")')


# In[ ]:

get_ipython().run_cell_magic('time', '', "#Feature preparation\n\n#1hot encoding of airline\nI = np.identity(14)\nairlines_dict = dict(zip(flights['AIRLINE'].unique(), I) )\nflights['airlines'] = flights['AIRLINE'].map(airlines_dict).astype(list)\n#temp_airlines = np.array(flights['AIRLINE'].map(airlines_dict).astype(list))\n\n#1hot encoding of Day of week\nI = np.identity(7)\ndaysofweek = dict(zip(flights['DAY_OF_WEEK'].unique(), I) )\nflights['daysofweek'] = flights['DAY_OF_WEEK'].map(daysofweek).astype(list)\n#temp_dayofweek = np.array(flights['DAY_OF_WEEK'].map(daysofweek).astype(list))\n\n#1hot encoding of Month\nI = np.identity(12)\nmonths = dict(zip(flights['MONTH'].unique(), I) )\nflights['months'] = flights['MONTH'].map(months).astype(list)\n#temp_months = np.array(flights['MONTH'].map(months).astype(list))\n\n\n#1hot encoding of airports\nI = np.identity(len(flights['ORIGIN_AIRPORT'].unique()))\norigin = dict(zip(flights['ORIGIN_AIRPORT'].unique(), I))\nflights['origin'] = flights['ORIGIN_AIRPORT'].map(origin).astype(list)\n#temp_origin = np.array(flights['ORIGIN_AIRPORT'].map(origin).astype(list))\n\n#1hot encoding of airports\nI = np.identity(len(flights['DESTINATION_AIRPORT'].unique()))\ndepart = dict(zip(flights['DESTINATION_AIRPORT'].unique(), I))\nflights['destination'] = flights['DESTINATION_AIRPORT'].map(depart).astype(list)\n#temp_depart = np.array(flights['DESTINATION_AIRPORT'].map(depart).astype(list))")


# In[ ]:

get_ipython().run_cell_magic('time', '', "#Map arrival delays onto 3 categories: early, 0 - 60 minutes late, greater than 60 minutes\narrival = []\ndelay_time = 60\nfor i in range(len(flights['ARRIVAL_DELAY'])):\n    if flights['ARRIVAL_DELAY'][i] < 0:\n        arrival.append(0)\n    elif flights['ARRIVAL_DELAY'][i] >= 0 and flights['ARRIVAL_DELAY'][i] < delay_time:\n        arrival.append(1)\n    else:\n        arrival.append(2)\n\narrival = np.array(arrival)")

%%time
#Map arrival delays onto 2 categories: early, 0 - 60 minutes late, greater than 60 minutes
arrival = []
delay_time = 60
for i in range(len(flights['ARRIVAL_DELAY'])):
    if flights['ARRIVAL_DELAY'][i] < delay_time:
        arrival.append(0)
    else:
        arrival.append(1)

arrival = np.array(arrival)
# In[ ]:

get_ipython().run_cell_magic('time', '', "#cancelled = np.array(flights['CANCELLED'])\nlabels_to_drop = ['origin', 'destination', 'SCHEDULED_DEPARTURE', 'SCHEDULED_TIME', 'DAY', 'YEAR','ORIGIN_AIRPORT', 'DESTINATION_AIRPORT', 'ELAPSED_TIME', 'MONTH', 'DAY_OF_WEEK', 'AIRLINE', 'SCHEDULED_ARRIVAL', 'DEPARTURE_DELAY', 'DEPARTURE_TIME', 'TAXI_OUT','FLIGHT_NUMBER', 'TAIL_NUMBER', 'WHEELS_OFF', 'AIR_TIME', 'DISTANCE', 'WHEELS_ON', 'TAXI_IN', 'CANCELLED', 'CANCELLATION_REASON', 'AIR_SYSTEM_DELAY', 'SECURITY_DELAY', 'AIRLINE_DELAY', 'LATE_AIRCRAFT_DELAY', 'WEATHER_DELAY', 'ARRIVAL_TIME', 'ARRIVAL_DELAY', 'DIVERTED']")


# In[ ]:

get_ipython().run_cell_magic('time', '', '#Remove all NaN\nflight = flights.drop(labels_to_drop, axis=1)\nDATA = flight.dropna()')


# In[ ]:

flight.dtypes


# In[ ]:

#Clears memory
flights = None 


# In[ ]:

get_ipython().run_cell_magic('time', '', '#Format data so its easier to handle with machine learning algorithms\nN = np.round(len(DATA)/2)\nX_train = np.array(DATA)[0:N]\nX_test = np.array(DATA)[N:]\n\ny = arrival[0:N]\n\n\nX = []\nfor i in range(len(X_train)):\n    X.append([x for y in X_train[i] for x in y]) \nX = np.array(X)\n\n\nX2 = []\nfor i in range(len(X_test)):\n    X2.append([x for y in X_test[i] for x in y]) \nX2= np.array(X2)\n\nData = None \nX_test = None\nX_train = None')


# In[ ]:



ModelsRidge Regression
# In[ ]:

get_ipython().run_cell_magic('time', '', 'for param in [1]:\n    model = sklearn.linear_model.Ridge(alpha = param, fit_intercept=True)\n    model = model.fit(X,y)\n    values = model.predict(X2)\n    print(sklearn.metrics.mean_squared_error(y, values))')


# In[ ]:



Logistic Regression
# In[ ]:

get_ipython().run_cell_magic('time', '', "model = sklearn.linear_model.LogisticRegression(fit_intercept=True, solver = 'newton-cg', multi_class = 'multinomial')\nmodel = model.fit(X,y)")


# In[ ]:

values = model.predict(X2)
sklearn.metrics.mean_squared_error(y, values)


# In[ ]:

sklearn.metrics.confusion_matrix(y, values)


# In[ ]:

sklearn.metrics.mean_squared_error(y, [0]*len(y))


# In[ ]:



