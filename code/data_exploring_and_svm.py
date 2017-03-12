
# coding: utf-8

# In[214]:

import urllib
import random
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import defaultdict
from sklearn import svm


# In[4]:

get_ipython().magic('matplotlib inline')


# In[197]:

airlines = pd.read_csv('/Users/wangzongwei/Desktop/cse258/flight-delays/airlines.csv')
airports = pd.read_csv('/Users/wangzongwei/Desktop/cse258/flight-delays/airports.csv')
flights = pd.read_csv('/Users/wangzongwei/Desktop/cse258/flight-delays/flights.csv', low_memory=False)


# In[286]:

D = 60


# In[198]:

flights.head()


# In[60]:

scheduled_mon = [0]*12
for i in range(1,13):
    scheduled_mon[i-1] = flights[flights['MONTH']==i].count()['SCHEDULED_DEPARTURE']


# In[66]:

print 'Cancelled:'
operated_mon = [0]*12
cancelled_mon = [0]*12
n_cancelled = flights[(flights['CANCELLED']==1)].count()['CANCELLED']
for i in range(1,13):
    mon_n_cancelled = flights[(flights['CANCELLED']==1)&(flights['MONTH']==i)].count()['CANCELLED']
    cancelled_mon[i-1] = mon_n_cancelled
    operated_mon[i-1] = scheduled_mon[i-1]-mon_n_cancelled
    ratio1 = mon_n_cancelled*1.0/n_cancelled*100
    ratio2 = mon_n_cancelled*1.0/scheduled_mon[i-1]*100
    print 'Mon='+str(i)+' '+str(mon_n_cancelled)+' '+str(ratio1)+'%'+' '+str(scheduled_mon[i-1])+' '+str(ratio2)+'%'
ratio3 = n_cancelled*1.0/sum(scheduled_mon)*100
print 'Total: '+str(n_cancelled)+' '+str(sum(scheduled_mon))+' '+str(ratio3)+'%'


# In[87]:

cancelled_dow = [0]*7
for i in range(1,8):
    cancelled_dow[i-1] = flights[(flights['CANCELLED']==1)&(flights['DAY_OF_WEEK']==i)].count()['CANCELLED']
    ratio = cancelled_dow[i-1]*1.0/n_cancelled*100
    print 'day of week='+str(i)+' '+str(cancelled_dow[i-1])+' '+str(ratio)+'%'


# In[111]:

departure_delay = flights[(flights['DEPARTURE_DELAY']>D)].count()['DEPARTURE_DELAY']
arrival_delay = flights[(flights['ARRIVAL_DELAY']>D)].count()['ARRIVAL_DELAY']
duo_delay = flights[(flights['ARRIVAL_DELAY']>D)&(flights['DEPARTURE_DELAY']>D)].count()['ARRIVAL_DELAY']


# In[99]:

print 'Arrival Delay > '+str(D)+' min (Monthly):'
arr_delayed_mon = [0]*12
# dep_delayed_mon = [0]*12
month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
for i in range(1,13):
    mon_arrival_delay = flights[(flights['ARRIVAL_DELAY']>D)&(flights['MONTH']==i)].count()['ARRIVAL_DELAY']
#     mon_departure_delay = flights[(flights['DEPARTURE_DELAY']>5)&(flights['MONTH']==i)].count()['DEPARTURE_DELAY']
    arr_delayed_mon[i-1] = mon_arrival_delay
#     dep_delayed_mon[i-1] = mon_departure_delay
    ratio1 = mon_arrival_delay*1.0/arrival_delay*100
    ratio2 = mon_arrival_delay*1.0/operated_mon[i-1]*100
#     r = mon_departure_delay*1.0/departure_delay*100
    print str(month[i-1])+' '+str(mon_arrival_delay)+' '+str(ratio1)+'% '+str(operated_mon[i-1])+' '+str(ratio2)+'%'
ratio3 = arrival_delay*1.0/sum(operated_mon)*100
print 'Total: '+str(arrival_delay)+' '+str(sum(operated_mon))+' '+str(ratio3)+'%'


# In[103]:

print 'Arrival Delay > '+str(D)+' min (Seasonally):'
season = ['Spring', 'Summer', 'Fall', 'Winter']
arr_delayed_season = [0]*4
operated_season = [0]*4
j = 0
for i in range(12):
    arr_delayed_season[j] += arr_delayed_mon[(i+2)%12]
    operated_season[j] += operated_mon[(i+2)%12]
    if i == 2 or i == 5 or i == 8:
        j += 1
for i in range(4):
    ratio1 = arr_delayed_season[i]*1.0/operated_season[i]*100
    ratio2 = operated_season[i]*1.0/sum(operated_season)*100
    print season[i]+' '+str(arr_delayed_season[i])+' '+str(operated_season[i])+' '+str(ratio1)+'% '+str(ratio2)+'%'


# In[104]:

arr_delayed_dow = [0]*7
dow = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
for i in range(1,8):
    arr_delayed_dow[i-1] = flights[(flights['ARRIVAL_DELAY']>D)&(flights['DAY_OF_WEEK']==i)].count()['ARRIVAL_DELAY']
    ratio = arr_delayed_dow[i-1]*1.0/arrival_delay*100
    print str(dow[i-1])+' '+str(arr_delayed_dow[i-1])+' '+str(ratio)+'%'


# In[112]:

print 'departure delayed: '+str(departure_delay)
print 'arrival delayed: '+str(arrival_delay)
ratio1 = duo_delay*1.0/arrival_delay*100
print 'departure & arrival delayed: '+str(duo_delay)+' '+str(ratio1)+'%'
ratio2 = flights[(flights['ARRIVAL_DELAY']>D)&(flights['DEPARTURE_DELAY']<=D)].count()['ARRIVAL_DELAY']*1.0/arrival_delay*100
print 'departure on time & arrival delayed: '+str(flights[(flights['ARRIVAL_DELAY']>D)&(flights['DEPARTURE_DELAY']<=D)].count()['ARRIVAL_DELAY'])+' '+str(ratio2)+'%'


# In[ ]:




# In[174]:

airlines.head()


# In[126]:

airlines_code = {}
for i in range(airlines.shape[0]):
    airlines_code[airlines['IATA_CODE'][i]] = airlines['AIRLINE'][i]


# In[139]:

arr_delayed_airline = {}
scheduled_airline = {}
cancelled_airline = {}
operated_airline = {}
for key in airlines_code:
    arr_delayed_airline[key] = flights[(flights['ARRIVAL_DELAY']>D)&(flights['AIRLINE']==key)].count()['ARRIVAL_DELAY']
    scheduled_airline[key] = flights[flights['AIRLINE']==key].count()['SCHEDULED_DEPARTURE']
    cancelled_airline[key] = flights[(flights['AIRLINE']==key)&(flights['CANCELLED']==1)].count()['CANCELLED']
    operated_airline[key] = scheduled_airline[key] - cancelled_airline[key]


# In[159]:

delayed_airline = []
for key in arr_delayed_airline:
    delayed_airline.append((arr_delayed_airline[key], key))
delayed_airline.sort(reverse=True)
for t in delayed_airline:
    ratio1 = operated_airline[t[1]]*1.0/sum(operated_airline.values())*100
    ratio2 = t[0]*1.0/operated_airline[t[1]]*100
    print t[1]+': '+str(ratio1)+'% '+str(t[0])+' '+str(ratio2)+'% '+airlines_code[t[1]]


# In[ ]:




# In[176]:

airports.head()


# In[170]:

airports_name = {}
for i in range(airports.shape[0]):
    airports_name[airports['IATA_CODE'][i]] = (airports['AIRPORT'][i], airports['STATE'][i]) 


# In[161]:

arr_delayed_airport = {}
arr_flight_vol_airport = {}
for key in airports_name:
    arr_delayed_airport[key] = flights[(flights['ARRIVAL_DELAY']>D)&(flights['DESTINATION_AIRPORT']==key)].count()['ARRIVAL_DELAY']
    operated = flights[flights['DESTINATION_AIRPORT']==key].count()['SCHEDULED_DEPARTURE']-flights[(flights['DESTINATION_AIRPORT']==key)&(flights['CANCELLED']==1)].count()['CANCELLED']
    arr_flight_vol_airport[key] = operated


# In[173]:

delayed_airport1 = []
delayed_airport2 = []
delayed_airport3 = []
for key in arr_delayed_airport:
    ratio = arr_delayed_airport[key]*1.0/arr_flight_vol_airport[key]*100
    delayed_airport1.append((arr_delayed_airport[key], arr_flight_vol_airport[key], ratio, key))
    delayed_airport2.append((arr_flight_vol_airport[key], arr_delayed_airport[key], ratio, key))
    delayed_airport3.append((ratio, arr_flight_vol_airport[key], arr_delayed_airport[key], key))
delayed_airport1.sort(reverse=True)
delayed_airport2.sort(reverse=True)
delayed_airport3.sort(reverse=True)
i = 0
print 'Ordered by arrival delay:'
for t in delayed_airport1:
    print t[-1]+': '+str(t[0])+' '+str(t[1])+' '+str(t[2])+'% '+airports_name[t[-1]][0]+', '+airports_name[t[-1]][1]
    i += 1
    if i == 5:
        break
i = 0
print 'Ordered by flight volumn:'
for t in delayed_airport2:
    print t[-1]+': '+str(t[0])+' '+str(t[1])+' '+str(t[2])+'% '+airports_name[t[-1]][0]+', '+airports_name[t[-1]][1]
    i += 1
    if i == 5:
        break
i = 0
print 'Ordered by ratio:'
for t in delayed_airport3:
    print t[-1]+': '+str(t[0])+'% '+str(t[1])+' '+str(t[2])+' '+airports_name[t[-1]][0]+', '+airports_name[t[-1]][1]
    i += 1
    if i == 5:
        break


# In[ ]:




# In[182]:

# flight_route = {}
# for key in airports_name:
#     for k in airports_name.keys():
#         if key is not k:
#             flight_route[key+k] = flights[(flights['ARRIVAL_DELAY']>D)&(flights['DESTINATION_AIRPORT']==k)&(flights['ORIGIN_AIRPORT']==key)].count()['ARRIVAL_DELAY']


# In[188]:

sample_flights = pd.read_csv('/Users/wangzongwei/Desktop/cse258/flight-delays/sample_flights.csv', low_memory=False, header=None)


# In[202]:

sample_flights.columns = ['YEAR', 'MONTH', 'DAY', 'DAY_OF_WEEK', 'AIRLINE', 'FLIGHT_NUMBER', 'TAIL_NUMBER',                           'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT', 'SCHEDULED_DEPARTURE', 'DEPARTURE_TIME',                           'DEPARTURE_DELAY', 'TAXI_OUT', 'WHEELS_OFF', 'SCHEDULED_TIME', 'ELAPSED_TIME',                           'AIR_TIME', 'DISTANCE', 'WHEELS_ON', 'TAXI_IN', 'SCHEDULED_ARRIVAL', 'ARRIVAL_TIME',                           'ARRIVAL_DELAY', 'DIVERTED', 'CANCELLED', 'CANCELLATION_REASON', 'AIR_SYSTEM_DELAY',                           'SECURITY_DELAY', 'AIRLINE_DELAY', 'LATE_AIRCRAFT_DELAY', 'WEATHER_DELAY']


# In[255]:

sample_flights.tail()


# In[295]:

X = []
y = []
airlines_id = dict(zip(airlines_code.keys(),range(len(airlines_code))))
airports_id = dict(zip(airports_name.keys(),range(len(airports_name))))
for i in range(sample_flights.shape[0]):
    if sample_flights['CANCELLED'][i] or sample_flights['DIVERTED'][i]: 
        continue
    feat = [1]
    f_mon = [0]*12
    f_mon[sample_flights['MONTH'][i]-1] = 1
    feat += f_mon
    f_dow = [0]*7
    f_dow[sample_flights['DAY_OF_WEEK'][i]-1] = 1
    feat += f_dow
    f_airlines = [0]*len(airlines_code)
    f_airlines[airlines_id[sample_flights['AIRLINE'][i]]] = 1
    feat += f_airlines
    f_airports = [0]*len(airports_name)
    if sample_flights['DESTINATION_AIRPORT'][i] not in airports_id:
        continue
    f_airports[airports_id[sample_flights['DESTINATION_AIRPORT'][i]]] = 1
    feat += f_airports
    feat += sample_flights['DEPARTURE_DELAY'][i]>D
    X.append(feat)
    score = 0
    if sample_flights['ARRIVAL_DELAY'][i]>D:
        score = 1
    elif sample_flights['ARRIVAL_DELAY'][i]<D:
        score = -1
    y.append(score)


# In[297]:

X_train = X[:int(len(X)/2)]
X_test = X[int(len(X)/2):]
y_train = y[:int(len(y)/2)]
y_test = y[int(len(y)/2):]


# In[299]:

clf = svm.SVC(C=1.0)
clf.fit(X_train, y_train)
test_predictions = clf.predict(X_test)


# In[302]:

# # for binary classification 
# TP = sum([y_test[i] and test_predictions[i] for i in range(len(y_test))])
# TN = sum([not y_test[i] and not test_predictions[i] for i in range(len(y_test))])
# FN = sum([y_test[i] and not test_predictions[i] for i in range(len(y_test))])
# FP = sum([not y_test[i] and test_predictions[i] for i in range(len(y_test))])
# TPR = TP*1.0/(TP+FN)
# TNR = TN*1.0/(TN+FP)
# BER = 1-0.5*(TPR+TNR)
# print BER


# In[312]:

tri_accuracy = sum([y_test[i] == test_predictions[i] for i in range(len(y_test))])*1.0/len(y_test)


# In[316]:

bc = sum([y_test[i]==-1 and test_predictions[i]!=-1 for i in range(len(y_test))])
abc = sum([y_test[i]==-1 for i in range(len(y_test))])
df = sum([y_test[i]==0 and test_predictions[i]!=0 for i in range(len(y_test))])
ndef = sum([y_test[i]==0 for i in range(len(y_test))])
gh = sum([y_test[i]==1 and test_predictions[i]!=1 for i in range(len(y_test))])
ghi = sum([y_test[i]==1 for i in range(len(y_test))])
tri_ber = (bc*1.0/abc+df*1.0/ndef+gh*1.0/ghi)*1.0/3
print tri_ber


# In[ ]:



