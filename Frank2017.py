#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 15:45:48 2018

@author: forrest
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime

frank = pd.read_excel("/Users/forrest/Desktop/Data/FrankNtilikina.xlsx")

date = frank.Date
games = frank.G
points = frank.PTS
assists = frank.AST
orebs, drebs = frank.ORB, frank.DRB
TOs = frank.TOV
steals = frank.STL
blocks = frank.BLK
mins = frank.MP
shots_2, makes_2 = frank.FGA, frank.FGA
shots_3, makes_3 = frank.three_PA, frank.three_P
FG_perc = frank.FG_perc

i1 = points[points=="Inactive"].index
i2 = points[points=="Did Not Dress"].index
i = i1.append(i2)


def SMA(X, n=6):
    new_X = list([])
    for i in range(len(X)):
        sma = np.mean(X[i-n:i])
        new_X += [sma]
    return new_X
    
def correlation(A, B):
    nom = np.dot(A,B)
    den = np.sqrt(np.sum(np.square(A)+np.sum(np.square(B))))
    return nom/den

minutes = []
for j in range(len(mins.drop(i))):
    if type(mins[j])==datetime.time:
        minutes += [float(str(mins[j].hour)+'.'+str(mins[j].minute))]
    elif type(mins[j])==datetime.datetime:
        minutes += [float(str(int(mins[6].day*24)+int(mins[6].hour))
                    +'.'+str(mins[6].minute))]
    else:
        minutes += [0]        
minutes = pd.Series(minutes)

n = 10
fig, (ax1,ax2,ax3,ax4,ax5) = plt.subplots(5, 1, sharex = True, figsize=(15,10))
ax1.plot(games.drop(i), SMA(minutes,n)), ax1.set_ylabel("minutes")
ax1.scatter(games.drop(i), SMA(minutes,n),c='r')
ax2.plot(games.drop(i), SMA(points.drop(i),n)), ax2.set_ylabel("points")
ax2.scatter(games.drop(i), SMA(points.drop(i),n),c='r')
ax3.plot(games.drop(i), SMA(assists.drop(i),n)), ax3.set_ylabel("assists")
ax3.scatter(games.drop(i), SMA(assists.drop(i),n),c='r')
ax4.plot(games.drop(i), SMA(makes_3.drop(i),n)), ax4.set_ylabel("3 Pointers")
ax4.scatter(games.drop(i), SMA(makes_3.drop(i),n),c='r')
ax5.plot(games.drop(i), SMA(FG_perc.drop(i),n)), ax5.set_ylabel("FG%")
ax5.scatter(games.drop(i), SMA(FG_perc.drop(i),n),c='r')


