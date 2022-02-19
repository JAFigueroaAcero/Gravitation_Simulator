# -*- coding: utf-8 -*-
"""
Created on Sun Nov 21 18:17:21 2021

@author: Juan Antonio

Title: Gravitación sim

ver: 9.0
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
                el.append([a[n][3]])
                list_ys[n].append([a[n][4]])
            t += dt

    list_g= [[list_xs[n],list_ys[n]] for n in range(len(list_xs))]
    list_f = list(map(lambda x: [list(map(lambda y: x[0][y], list_i)),list(map(lambda y: x[1][y], list_i))], list_g))

    plt.ioff()
    fig = plt.figure
    # Velocity graphs
    if dfl2[5] == 1:
        p2 = 'graphs//' + path.replace('//', '-').replace('.csv', '')
        try:
            mkdir('graphs')
        except:
            pass
        try: 
            mkdir(p2)
        except:
            rmtree(p2)
            mkdir(p2)
        for n,g in enumerate(list_f2):
            v = list(a)
            v = v[n]
            mkdir(f'{p2}//{v[0]}')

            fig = plt.figure()
            plt.figure()
            plt.plot([list_t[m] for m in range(len(list_t))], [list_f2[n][0][m] for m in range(len(list_t))])
            plt.ylabel('xvel(m/s)')
            plt.xlabel('time(s)')
            plt.title(f'{(v[0])} xvel.')
            plt.savefig(f'{p2}//{v[0]}//xvel.png')
            plt.close(fig)

            fig = plt.figure()
            plt.figure()
            plt.plot([list_t[m] for m in range(len(list_t))], [list_f2[n][1][m] for m in range(len(list_t))])
            plt.ylabel('yvel(m/s)')
            plt.xlabel('time(s)')
            plt.title(f'{v[0]} yvel.')
            plt.savefig(f'{p2}//{v[0]}//yvel.png')
            plt.close(fig)
        mkdir(f'{p2}//gen')

        fig2 = plt.figure()
        plt.figure()
        for n,g in enumerate(list_f2):
            plt.plot([list_t[m] for m in range(len(list_t))], [list_f2[n][0][m] for m in range(len(list_t))])
        plt.ylabel('xvel(m/s)')
        plt.xlabel('time(s)')
        plt.title('Gen xvel.')
        plt.savefig(f'{p2}//gen//xvel.png')
        plt.close(fig2)

        fig3 = plt.figure()
        plt.figure()
        for n,g in enumerate(list_f2):
            plt.plot([list_t[m] for m in range(len(list_t))],[list_f2[n][1][m] for m in range(len(list_t))])
        plt.ylabel('yvel(m/s)')
        plt.xlabel('time(s)')
        plt.title('Gen yvel.')
        plt.savefig(f'{p2}//gen//yvel.png')
        plt.close(fig3)
        fig4 = plt.figure()
        plt.figure()
        for n,g in enumerate(list_f2):
            plt.plot([list_f2[n][0][m] for m in range(len(list_t))], [list_f2[n][1][m] for m in range(len(list_t))])
        plt.ylabel('xvel(m/s)')
        plt.xlabel('yvel(m/s)')
        plt.title('Gen xvel/yvel.')
        plt.savefig(f'{p2}//gen//xyvel.png')
        plt.close(fig4)
    # Position graphs
        for n,g in enumerate(list_f):
            v = list(a)
            v = v[n]
            fig = plt.figure()
            plt.figure()
            plt.plot([list_t[m] for m in range(len(list_t))], [list_f[n][0][m] for m in range(len(list_t))])
            plt.ylabel('xpos(m/s)')
            plt.xlabel('time(s)')
            plt.title(f'{(v[0])} xpos.')
            plt.savefig(f'{p2}//{v[0]}//xpos.png')
            plt.close(fig)

            fig = plt.figure()
            plt.figure()
            plt.plot([list_t[m] for m in range(len(list_t))], [list_f[n][1][m] for m in range(len(list_t))])
            plt.ylabel('ypos(m/s)')
            plt.xlabel('time(s)')
            plt.title(f'{v[0]} ypos.')
            plt.savefig(f'{p2}//{v[0]}//ypos.png')
            plt.close(fig)
        fig5 = plt.figure()
        plt.figure()
        for n,g in enumerate(list_f):
            plt.plot([list_t[m] for m in range(len(list_t))], [list_f[n][0][m] for m in range(len(list_t))])
        plt.ylabel('xpos(m/s)')
        plt.xlabel('time(s)')
        plt.title('Gen xpos.')
        plt.savefig(f'{p2}//gen//xpos.png')
        plt.close(fig5)

        fig6 = plt.figure()
        plt.figure()
        for n,g in enumerate(list_f):
            plt.plot([list_t[m] for m in range(len(list_t))],[list_f[n][1][m] for m in range(len(list_t))])
        plt.ylabel('ypos(m/s)')
        plt.xlabel('time(s)')
        plt.title('Gen ypos.')
        plt.savefig(f'{p2}//gen//ypos.png')
        plt.close(fig6)

        fig7 = plt.figure()
        plt.figure()
        for n,g in enumerate(list_f):
            plt.plot([list_f[n][0][m] for m in range(len(list_t))], [list_f[n][1][m] for m in range(len(list_t))])
        plt.ylabel('xpos(m/s)')
        plt.xlabel('ypos(m/s)')
        plt.title('Gen xpos/ypos.')
        plt.savefig(f'{p2}//gen//xypos.png')
        plt.close(fig7)

    pathprov = 'assets//' + path.replace('//', '-').replace('.csv', '')
    try: 
        mkdir(pathprov)
    except:
        rmtree(pathprov)
        mkdir(pathprov)
    df = pd.DataFrame([pd.read_csv('assets//configs.csv').values.tolist()[0]], columns = ['rtps','dt','tst','ips', 'il','sgraphs','pos','vel','x','y'])
    df.to_csv(f'{pathprov}//configs.csv', index=False)
    
    df = pd.DataFrame(pd.read_csv(path).values.tolist(), columns = ['Name','mass','radio','x','y','vel','prad'])
    df.to_csv(f'{pathprov}//data.csv', index=False)
    
    dfv = pd.read_csv(path)
    dfvl = dfv.values.tolist()
    if dfl2[6] == 1:
        if dfl2[8] + dfl2[9] == 2:
            for n, el in enumerate(list_f):
                df = pd.DataFrame([el[0],el[1]])
                df.to_csv(f'{pathprov}//{dfvl[n][0]}.csv', index=False)
        elif dfl2[8] == 1:
            for n, el in enumerate(list_f):
                df = pd.DataFrame([list_t,el[0]])
                df.to_csv(f'{pathprov}//{dfvl[n][0]}.csv', index=False)
        else:
            for n, el in enumerate(list_f):
                df = pd.DataFrame([list_t,el[1]])
                df.to_csv(f'{pathprov}//{dfvl[n][0]}.csv', index=False)
    else:
        if dfl2[8] + dfl2[9] == 2:
            for n, el in enumerate(list_f2):
                df = pd.DataFrame([el[0],el[1]])
                df.to_csv(f'{pathprov}//{dfvl[n][0]}.csv', index=False)
        elif dfl2[8] == 1:
            for n, el in enumerate(list_f2):
                df = pd.DataFrame([list_t,el[0]])
                df.to_csv(f'{pathprov}//{dfvl[n][0]}.csv', index=False)
        else:
            for n, el in enumerate(list_f2):
                df = pd.DataFrame([list_t,el[1]])
                df.to_csv(f'{pathprov}//{dfvl[n][0]}.csv', index=False)
    if dfl2[6] == 1:
        if dfl2[8] == 1 and dfl2[9] == 1:
            return {
                'xs': [list_f[n][0] for n, el in enumerate(list_f)],
                'ys': [list_f[n][1] for n, el in enumerate(list_f)]
                }
        elif dfl2[8] == 1:
            return {
                'ys': [list_f[n][0] for n, el in enumerate(list_f)],
                'xs': [list_t for t in enumerate(list_f2)]
                }
        else:
            return {
                'ys': [list_f[n][1] for n, el in enumerate(list_f)],
                'xs': [list_t for t in enumerate(list_f2)]
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
