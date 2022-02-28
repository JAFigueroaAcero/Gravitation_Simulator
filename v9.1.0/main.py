# -*- coding: utf-8 -*-
"""
Created on Sun Nov 21 18:17:21 2021

@author: Juan Antonio

Title: Gravitación sim

ver: 9.1
"""
import matplotlib
matplotlib.use('Agg')

import functions as f
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})

import time
from os import mkdir
from shutil import rmtree
import os.path

def graph(x,y,yt,xt,title,p,el):
    fig = plt.figure()
    plt.figure()
    x = list(x[m] for m in range(len(x)))
    y = list(y[m] for m in range(len(x)))
    plt.plot(x,y)
    plt.ylabel(yt)
    plt.xlabel(xt)
    plt.title(f'{el} {title}.')
    
    plt.savefig(os.path.join(os.path.join(p,str(el)),f'{title}.png'))
    plt.close(fig)

def grapht(x,y,yt,xt,title,p,time = True,axis = 0):
    fig2 = plt.figure()
    plt.figure()
    if time:
        l = len(x)
    else:
        l = len(x[0][0])
    l2 = len(y[0][0])
    for n in range(len(y)):
        if time:
            xs = list(x[m] for m in range(l))
        else:
            xs = list(x[n][0][m] for m in range(l))
        if axis == 0:
            ys = list(y[n][0][m] for m in range(l2))
        elif axis == 1:
            ys = list(y[n][1][m] for m in range(l2))
        plt.plot(xs, ys)
    plt.ylabel(yt)
    plt.xlabel(xt)
    plt.title(f'Gen {title}.')
    plt.savefig(os.path.join(os.path.join(p,'gen'),f'{title}.png'))
    plt.close(fig2)

def main():
    df = pd.read_csv(os.path.join('assets', 'path.csv'))
    dfl = df.values.tolist()[0]
    path = dfl[0]
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
    
    df2 = pd.read_csv(os.path.join('assets','configs.csv'))
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
    
    f.masssum(a)
    f.gm(a,dt)
    list_i = list(map(lambda x: int(x),rel * np.arange(0,itf,1)))

    list_xs = [[] for n in range(len(dfl))]
    list_ys = [[] for n in range(len(dfl))]

    list_xv = [[] for n in range(len(dfl))]
    list_yv = [[] for n in range(len(dfl))]
    list_t = []
    if dfl2[5] == 1 or dfl2[7] == 1:
        while t < tts:
            ac = a.copy()
            for n,el in enumerate(a):
                a[n] = f.actvecglob3(ac, n)
            for n, el in enumerate(list_xs):
                el.append(a[n][3])
                list_ys[n].append(a[n][4])
                list_xv[n].append(a[n][5])
                list_yv[n].append(a[n][6])
            list_t.append(t)
            t += dt
        list_g2= [[list_xv[n],list_yv[n]] for n in range(len(list_xs))]
        list_f2 = list(map(lambda x: [list(map(lambda y: x[0][y], list_i)),list(map(lambda y: x[1][y], list_i))], list_g2))
        list_t = list((map(lambda y: list_t[y], list_i)))

    else:
        while t < tts:
            ac = a.copy()
            for n,el in enumerate(a):
                a[n] = f.actvecglob3(ac, n)
            for n, el in enumerate(list_xs):
                el.append(a[n][3])
                list_ys[n].append(a[n][4])
            list_t.append(t)
            t += dt
        list_t = list((map(lambda y: list_t[y], list_i)))


    list_g= [[list_xs[n],list_ys[n]] for n in range(len(list_xs))]
    list_f = list(map(lambda x: [list(map(lambda y: x[0][y], list_i)),list(map(lambda y: x[1][y], list_i))], list_g))
    plt.ioff()
    fig = plt.figure
    pvalue = path.replace('/', '-').replace('.csv', '')

    if dfl2[5] == 1:
        
        p2 = os.path.join('graphs', pvalue)

        try:
            mkdir('graphs')
        except:
            pass
        try: 
            mkdir(p2)
        except:
            rmtree(p2)
            mkdir(p2)
        try:
            mkdir(os.path.join(p2,'gen'))
        except:
            rmtree(os.path.join(p2,'gen'))
            mkdir(os.path.join(p2,'gen'))
        ax = ['pos(m)','vel(ms)']
        for rep,val in enumerate(ax):
            if rep == 0:
                list_n = list_f
            else:
                list_n = list_f2
            for n,g in enumerate(list_n):
                v = list(a)
                v = v[n]
                try:
                    mkdir(os.path.join(p2,str(v[0])))
                except:
                    pass
                graph(list_t,list_n[n][0],'time(s)',f'x{val}',f'x{val}',p2,v[0])
                graph(list_t,list_n[n][1],'time(s)',f'y{val}',f'y{val}',p2,v[0])
            grapht(list_t,list_n,f'x{val}', 'time(s)',f'x{val}',p2)
            grapht(list_t,list_n,f'y{val}', 'time(s)',f'y{val}',p2, axis = 1)
            grapht(list_n,list_n,f'x{val}', f'y{val}',f'xy{val}',p2, time = False, axis = 1)
    
    pathprov = os.path.join('assets', pvalue)
    try: 
        mkdir(pathprov)
    except:
        rmtree(pathprov)
        mkdir(pathprov)
    
    df = pd.DataFrame([pd.read_csv(os.path.join('assets','configs.csv')).values.tolist()[0]], columns = ['rtps','dt','tst','ips', 'il','sgraphs','pos','vel','x','y'])
    df.to_csv(os.path.join(pathprov,'configs.csv'), index=False)
    
    df = pd.DataFrame(pd.read_csv(path).values.tolist(), columns = ['Name','mass','radio','x','y','vel','prad'])
    df.to_csv(os.path.join(pathprov,'configs.csv'), index=False)
    
    dfv = pd.read_csv(path)
    dfvl = dfv.values.tolist()
    if dfl2[6] == 1:
        if dfl2[8] + dfl2[9] == 2:
            for n, el in enumerate(list_f):
                df = pd.DataFrame([el[0],el[1]])
                df.to_csv(os.path.join(pathprov,f'{dfvl[n][0]}.csv'), index=False)
        elif dfl2[8] == 1:
            for n, el in enumerate(list_f):
                df = pd.DataFrame([list_t,el[0]])
                df.to_csv(os.path.join(pathprov,f'{dfvl[n][0]}.csv'), index=False)
        else:
            for n, el in enumerate(list_f):
                df = pd.DataFrame([list_t,el[1]])
                df.to_csv(os.path.join(pathprov,f'{dfvl[n][0]}.csv'), index=False)
    else:
        if dfl2[8] + dfl2[9] == 2:
            for n, el in enumerate(list_f2):
                df = pd.DataFrame([el[0],el[1]])
                df.to_csv(os.path.join(pathprov,f'{dfvl[n][0]}.csv'), index=False)
        elif dfl2[8] == 1:
            for n, el in enumerate(list_f2):
                df = pd.DataFrame([list_t,el[0]])
                df.to_csv(os.path.join(pathprov,f'{dfvl[n][0]}.csv'), index=False)
        else:
            for n, el in enumerate(list_f2):
                df = pd.DataFrame([list_t,el[1]])
                df.to_csv(os.path.join(pathprov,f'{dfvl[n][0]}.csv'), index=False)
    if dfl2[6] == 1:
        if dfl2[8] == 1 and dfl2[9] == 1:
            return {
                'xs': [list_f[n][0] for n, el in enumerate(list_f)],
                'ys': [list_f[n][1] for n, el in enumerate(list_f)]
                }
        elif dfl2[8] == 1:
            return {
                'ys': [list_f[n][0] for n, el in enumerate(list_f)],
                'xs': [list_t for t in enumerate(list_f)]
                }
        else:
            return {
                'ys': [list_f[n][1] for n, el in enumerate(list_f)],
                'xs': [list_t for t in enumerate(list_f)]
                }
    else:
        if dfl2[8] == 1 and dfl2[9] == 1:
            return {
                'xs': [list_f2[n][0] for n, el in enumerate(list_f2)],
                'ys': [list_f2[n][1] for n, el in enumerate(list_f2)]
                }
        elif dfl2[8] == 1:
            return {
                'ys': [list_f2[n][0] for n, el in enumerate(list_f2)],
                'xs': [list_t for t in enumerate(list_f2)]
                }
        else:
            return {
                'ys': [list_f2[n][1] for n, el in enumerate(list_f2)],
                'xs': [list_t for t in enumerate(list_f2)]
                }

if __name__ == "__main__":
    main()
