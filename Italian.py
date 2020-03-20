#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 10:24:30 2020

@author: rappasta
"""
import Utils as utils
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
data = utils.getData()

#fig, ax = plt.subplots()

regioni=[]
for val in data.itertuples():
    regioni.append(val.denominazione_regione)
regioni=list(set(regioni))


for regione in regioni:
    utils.TotaleValori(regione,data,'totale_casi')

