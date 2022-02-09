# -*- coding: utf-8 -*-
"""
Created on Sun Nov 21 18:17:21 2021

@author: Juan Antonio

Title: Gravitación sim

ver: 8.4
"""

import functions as f
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from os import mkdir
from shutil import rmtree


def main():
    df = pd.read_csv('assets//path.csv')
    dfl = df.values.tolist()[0]
    path = dfl[0]
    itime = time.time()
    df = pd.read_csv(path)
    dfl = df.values.tolist()
    a = np.array([None for n in range(len(dfl))])
    for n,e in enumerate(dfl):
        dfl[n] = dfl[n][:-2] + list(f.positionxy_angle(dfl[n][-1], dfl[n][-2]))
        a[n] = np.array([float(a) for a in dfl[n]])
    
    '''
    name
    mass
    radio
    x
    y
    xvel
    yvel
    '''

    df2 = pd.read_csv('assets//configs.csv')
    dfl2 = df2.values.tolist()[0]
    # variables in seconds
    trps = dfl2[0] # real time per second
    dt = dfl2[1]     # interval number between sums
    t = 0           # initial time
    tts = dfl2[2] # total system time
    frec = dfl2[3]       # frequency in iterations/seconds
    it = tts / dt   # total iterations
    itf = frec * tts / trps # total final iterations
    rel = it / itf  # relation of total iterations over total final iterations
    
    
    
    list_xs = [[] for n in range(len(dfl))]
    list_ys = [[] for n in range(len(dfl))]
    
    while t < tts:
        ac = a.copy()
        for n,el in enumerate(a):
            a[n] = f.actvecglob3(ac, dt, n)
        for n, el in enumerate(list_xs):
            el.append(a[n][3])
            list_ys[n].append(a[n][4])
        t += dt


    list_g= [[list_xs[n],list_ys[n]] for n in range(len(list_xs))]
    

    list_i = list(map(lambda x: int(x),rel * np.arange(0,itf,1)))
    list_f = list(map(lambda x: [list(map(lambda y: x[0][y], list_i)),list(map(lambda y: x[1][y], list_i))], list_g))

    for el in list_f:
        plt.plot(el[0],el[1])
    plt.show() 
    pathprov = 'assets//' + path.replace('//', '-').replace('.csv', '')
    try: 
        mkdir(pathprov)
    except:
        rmtree(pathprov)
        mkdir(pathprov)
        pass
    df = pd.DataFrame([pd.read_csv('assets//configs.csv').values.tolist()[0]], columns = ['rtps','dt','tst','ips', 'il'])
    df.to_csv(f'{pathprov}//configs.csv', index=False)
    
    df = pd.DataFrame(pd.read_csv(path).values.tolist(), columns = ['Name','mass','radio','x','y','vel','prad'])
    df.to_csv(f'{pathprov}//data.csv', index=False)
    
    dfv = pd.read_csv(path)
    dfvl = dfv.values.tolist()
    for n, el in enumerate(list_f):
        df = pd.DataFrame([el[0],el[1]])
        df.to_csv(f'{pathprov}//{dfvl[n][0]}.csv', index=False)
    
    return {
        'xs': [list_f[n][0] for n, el in enumerate(list_f)],
        'ys': [list_f[n][1] for n, el in enumerate(list_f)]
        }

if __name__ == "__main__":
    main()
