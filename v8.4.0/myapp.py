# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 08:02:06 2021

@author: Juan Antonio

title: graficacion de gravitacion

ver: 2.2
"""

from tornado.ioloop import IOLoop

import main as m
from bokeh.layouts import column
from bokeh.models.widgets import Button
from bokeh.plotting import figure
import sys
from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application
from bokeh.server.server import Server
import pandas as pd
from os import listdir



def md(doc):
    global lenbase
    global i
    global inter
    global ds
    global df
    global obj
    global list_dsc
    if not last:
        df = m.main()
        df2 = pd.read_csv('assets//configs.csv')
        dfl2 = df2.values.tolist()[0]  
    else:
        pathprov = 'assets//' + path.replace('//', '-').replace('.csv', '')
        l_dir = listdir(pathprov)
        l_dir.pop(l_dir.index('configs.csv'))
        df2 = pd.read_csv(f'{pathprov}//configs.csv')
        dfl2 = df2.values.tolist()[0]
        xs = []
        ys = []
        for d in l_dir:
            loc = pd.read_csv(f'{pathprov}//{d}')
            loc = loc.values.tolist()
            xs.append(loc[0])
            ys.append(loc[1])
        df = {
        'xs': xs,
        'ys': ys
        }

    df3 = pd.read_csv(path)
    dfl3 = df3.values.tolist()
        
    lenbase = len(df['xs'][0])
    i = 0
    inter = dfl2[4]
    itime = 1000/dfl2[3]

    obj = len(df['xs'])
    x = []
    y = []

    for n in range(obj):
        x += df['xs'][n]
        y += df['ys'][n]
    
    vals = (max(x), min(x), max(y), min(y))
    vals = tuple(1.1*v for v in vals)
    v = max(vals)


    p = figure(x_range = (-v, v), y_range = (-v, v))
    
    
    r = p.multi_line(xs=[[0] for n in range(obj)], ys=[[0] for n in range(obj)], color=['blue' for n in range(obj)],line_color ='blue')
    
    list_cir = []
    for n in dfl3:
        list_cir.append(p.circle(x = [0], y= [0], radius= n[2], color = 'red' ))
    
    list_dsc = [cir.data_source for cir in list_cir]
    ds = r.data_source
    
    doc.add_root(column([p, button]))
    doc.add_periodic_callback(callback, itime)

def button_callback():
    sys.exit()

button = Button(label="Stop", button_type="success")
button.on_click(button_callback)


def callback():
    global df
    global i
    global lenbase
    global inter
    global ds
    global list_dsc
    
    for n,dsc in enumerate(list_dsc):
        dsc.data = {
            'x': [float(df['xs'][n][i+inter])],
            'y': [float(df['ys'][n][i+inter])]
            }
    
    ds.data = {
        'xs': [list(df['xs'][n][i:i+inter]) for n in range(obj)],
        'ys': [list(df['ys'][n][i:i+inter]) for n in range(obj)]
        }
    if i >= lenbase - inter - 1:
        i = 0
    i += 1

def main(l_data = False, route = None):
    global last
    global path2
    global path
    df = pd.read_csv('assets//path.csv')
    dfl = df.values.tolist()[0]
    path = dfl[0]

    last = l_data
    path2 = route
    """Launch the server and connect to it.
    """
    
    print("Preparing a bokeh application.")
    io_loop = IOLoop.current()
    bokeh_app = Application(FunctionHandler(md))

    server = Server({"/": bokeh_app}, io_loop=io_loop)
    server.start()
    print("Opening Bokeh application on http://localhost:5006/")

    io_loop.add_callback(server.show, "/")
    io_loop.start()

if __name__ == "__main__":
    main()
