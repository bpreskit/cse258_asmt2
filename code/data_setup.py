import numpy as np
import os
import pickle
from csv import DictReader

dat_dir = 'local_data/'
dat_fil = dat_dir + 'flights.csv'

with open(dat_fil, 'r') as file:
    reader = DictReader(file)
    
