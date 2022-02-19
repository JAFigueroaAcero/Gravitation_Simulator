# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 19:50:20 2021

@author: Juan Antonio

Title: Interfaz tkinter Gravitación sim

ver: 2.8
"""



from os.path import isfile, isdir
import pandas as pd
import os.path

def proute(pr):
    global path
    df = pd.DataFrame([pr], columns = ['path'])
    df.to_csv(os.path.join('assets', 'path.csv'), index=False)
    path = pr

if isfile(os.path.join('assets', 'path.csv')):
        df = pd.read_csv(os.path.join('assets', 'path.csv')

)
        dfl = df.values.tolist()[0]
        path = dfl[0]
else:    
        proute(os.path.join('assets', 'data.csv'))


import tkinter as tk
import myapp as m

from tkinter import Tk
from tkinter import ttk


defaultconfigs = [60*60*24,60*10,60*60*24*365*2,20,500]




def order(parent):
    list_c = parent.list_val
    list_a = parent.list_index
    len_a = len(list_a)
    list_b = []
    while len_a != len(list_b):
        a = min(list_a)
        ind = list_a.index(a)
        list_b.append([list_a.pop(ind),list_c.pop(ind)])
    parent.list_val = [n[1] for n in list_b]
    parent.list_index = [n[0] for n in list_b]

def cbu(text):
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(text)
    r.update()
    r.destroy()

def conv(n):    
        while '/' in n:
            ind_a = n.index('/')
            loc = n[ind_a+1::]
            ind_b = len(loc)
            for m,e in enumerate(loc):
                if e in '+*-' and loc[m-1] != 'e':
                    ind_b = m
                    break
            n = n[0:ind_a] + '*' + str(1/float(loc[0:ind_b])) + n[ind_a+ind_b+1::]
        n = n.replace('-', '+-').replace('*+-', '*-').replace('e+-', 'e-').replace('e+','e').split('+')
        if n[0] == '':
            n = n[1::]
        for j,e in enumerate(n):
            loc2 = 1
            for el in e.split('*'):
                if '^' in el:
                    el = el.split('^')
                    loc2 *= float(el[0])**float(el[1])
                else:
                    el = el.split('e')
                    loc2 *= float(el[0]) if len(el) == 1 else float(el[0])*(10**float(el[1]))
            n[j] = loc2
        return sum(n)

def calc_min(var):
    sindex = 0
    findex = 0
    value = var
    if '(' in var:
        sindex = var.index('(')
        findex = var.index(')')
        if '(' in var[sindex+1: findex + 1]:
            value = calc_min(var[sindex + 1: findex + 1])
        else:
            value = var[sindex: findex + 1]
    else:
        return value
    return value

def calcp(v):
    nums = '1234567890'
    for n in nums:
        if n+'(' in v:
            v = v.replace(n+'(', f'{n}*(')
        if ')'+n in v:
            v = v.replace(')'+n, f')*{n}')
    while '(' in v:
        r = calc_min(v)
        v = v.replace(r, str(conv(r[1:len(r)-1])))
    return conv(v) 

def calc(parent,v):
    try:
        v = v.replace(' ', '').replace(')(', ')*(')
        v2 = v.split(',')
        eq = v2[0]
        l = 'abcdfghijklmnopqrstuvxyz'
        if len(eq) > 1:
            for var in v2[1::]:
                var = var.split('=')
                eq = eq.replace(var[0],str(calcp(var[1])))
        flag = True
        for c in eq:
            if c in l:
                flag = False
                break
        if flag:
            return calcp(eq) 
        else:
            ad(parent,'Undefined', 'A variable might not be defined')
            return None
    except:
        ad(parent, 'Wrong format', 'The format of the operation \n is incorrect.')
        return None

def clear(list_a):
    for v in list_a:
        v.delete(0,"end")
        v.insert(0,'')
        
def empty(val):
    loc = False
    for v in val:
        if v.get() == '':
            loc = True
            break
    return loc
def num(val):
    loc = True
    for v in val:
        try:
            float(v.get())
        except:
            loc = False
            break
    return loc


class ad():
    def __init__(self,parent,title,text):
        self.root= tk.Toplevel(parent.root)
        self.root.resizable(0,0)
        self.root.geometry('240x100')
        self.root.title(title)
        self.root.iconbitmap('assets//logo.ico')
        
        self.a1 = tk.Frame(self.root, width=200, height=100)
        self.a1l = tk.Label(self.a1, text=text, anchor="center")
        self.a1l.grid(row=1,column=0, pady=10)
        self.b1 = tk.Button(self.a1, width=3, height=1 ,text='Ok', command= self.root.destroy)
        self.b1.grid(row=3,column=0, sticky='nsew')
        self.a1.pack()
        self.root.transient(parent.root)
        self.root.mainloop()

class conversion():
    def __init__(self,parent):
        self.list_help = [
            ['SYMBOLS', None],
            ['\'+, -\' symbols','Symbols equivalent to sum.'],
            ['\'*\' symbol','Symbol equivalent to multiply.'],
            ['\'/ \' symbol', 'Symbol equivalent to division.'],
            ['\'e\' symbol', 'Symbol equivalent to x * 10 ** n.'],
            ['\'^\' symbol', 'Symbol equivalent to x up to the n.'],
            ['\'(\',\')\' symbols', 'Symbols to separate operations.'],
            ['VARIABLES', None],
            ['Variables', 'Any character can be used as a variable.'],
            ['Set var', 'To set a value to a var user might separate \n base equation and variables with a comma, \n define a variable with \'Vname = Vvalue\' format.'],
            ['Note 1', 'Operations can be done in variable definitions \n but variables inside a variable definiton \n can not be defined.'],
            ['Note 2', 'For practical reasons it is recommended \n to avoid using symbols as variables.'],
            ['BUTTONS', None],
            ['Conv to cboard', 'Copies the operation to the clipboard.'],
            ['Conv to empty', 'Copies the operation to the next empty \n field of the converter opener.'],
            ['Op', 'Do the operation in the converter field.'],
            ['Clear', 'Clears the operation field.']
            ]
        
        self.root = tk.Toplevel(parent.root)
        self.root.resizable(0,0)
        self.root.title('Converter')
        self.root.iconbitmap('assets//logo.ico')
        
        self.a1 = tk.Frame(self.root, width = 220, height = 200)
        self.a1.grid(row=1, column=0, sticky='nsew', pady=10)
        
        self.a2 = tk.Frame(self.root)
        self.a2.grid(row=0, column=0, sticky='nsew', pady=0)
        
        self.a3 = tk.Frame(self.root)
        self.a3.grid(row=2, column=0, sticky='nsew', pady=0)
        
        self.op = tk.Entry(self.a1,  width=30)
        self.op.grid(row=2, column=1, padx=5, pady=0)
        self.list_a = parent.list_entry
        
        
        def convloc():
            d = calc(self, self.op.get())
            if d != None:
                self.op.delete(0,"end")
                self.op.insert(0,d) 
        def copy():
            d = calc(self, self.op.get())
            if d != None:
                self.op.delete(0,"end")
                self.op.insert(0,d) 
                loc = True
                for el in self.list_a:
                    if el.get() == '':
                        el.insert(0,self.op.get())
                        loc = False
                        break
                if loc:
                    ad(self,'No empty fields', 'There is no empty entry to copy.')
        def cbuloc():
            convloc()
            cbu(self.op.get())
            
        self.b1 = tk.Button(self.a2, text = 'Conv to cboard', width=10, padx=5, pady=0, command = lambda: cbuloc())
        self.b1.grid(row=0, column=1,padx=5, pady=5)
        
        
        self.b2 = tk.Button(self.a2, text = '?', width=2, padx=5, pady=0, command = lambda: helpd(self,self.list_help))
        self.b2.grid(row=0, column=0,padx=5, pady=5)
        
        self.b3 = tk.Button(self.a3, text = 'Conv to empty', width=10, padx=5, pady=0, command = lambda: copy())
        self.b3.grid(row=0, column=0,padx=5, pady=5)
        
        self.b4 = tk.Button(self.a3, text = 'Clear', width=10, padx=5, pady=0, command = lambda: clear([self.op]))
        self.b4.grid(row=0, column=1,padx=5, pady=5)
        
        self.b5 = tk.Button(self.a2, text = 'Op', width=2, padx=5, pady=0, command = lambda: convloc())
        self.b5.grid(row=0, column=2,padx=5, pady=5)
        self.root.transient(parent.root)
        self.root.mainloop()
        
def show(parent, list_a = None):
    if list_a == None:
        if isfile(path):
            df = pd.read_csv(path)
            df = df.values.tolist()
            t = 'Last data'
        else: 
            ad(parent, 'Not found', 'There is not last data source.')
            
    else:
        df = list_a
        t = 'Current data'
    list_a = []
    relative = ['mass','radio','x','y','vel','prad']
    if list_a == None and not isfile(path):
        pass
    else:
        if df == []:
            ad(parent, 'No data yet', 'Fill the data to see the current.')
        else:
            sep = 2
            for el in df:
                loc = ''
                for n,e in enumerate(el[1::]):
                    loc += f'{relative[n]}: {str(e)} \n'
                if sep == 2:
                    list_a.append(['VALUES', None])
                    sep = 0
                else:
                    sep += 1
                list_a.append([el[0], loc])

            helpd(parent,list_a, name = t)
             
class helpd():
    def __init__(self,parent,helps,name = None):
        if name == None:
            name = 'Help'
        self.root = tk.Toplevel(parent.root)
        self.root.resizable(0,0)
        self.root.title(name)
        self.root.iconbitmap('assets//logo.ico')
        
        self.alist = [tk.Frame(self.root)]
        loc = 0
        setv = 0
        list_c = 0
        for n,h in enumerate(helps):
            if h[1] == None:
                setv = 2
                loc += 1
                list_c += 1
                ttk.Separator(self.root, orient=tk.VERTICAL).grid(row = 0, column = loc, rowspan=20, sticky='ns')
                loc += 1
                self.alist.append(tk.Frame(self.root))
                self.alist[list_c].grid(row = 0, column = loc, sticky='nsew', pady=5)
                tk.Label(self.alist[list_c], text = f'{h[0]}').grid(row = 0, column = 0,columnspan = 2, padx=5, pady=5)
                ttk.Separator(self.alist[list_c], orient=tk.HORIZONTAL).grid(row = 1, column = 0, columnspan=2, sticky='we')
            else:
                tk.Label(self.alist[list_c], text = f'{h[0]}:').grid(row = setv, column = 0, padx=5, pady=5)
                tk.Label(self.alist[list_c], text = h[1]).grid(row = setv, column = 1, padx=5, pady=5)
                setv += 1
class config():
    def __init__(self,parent):
        self.list_a = [
            ['VARIABLES', None],
            ['Real ex time per sec','It expresses how much time of simulation is going to be represented \n as a second in real time. \n 60*60*24 is the default.'],
            ['Integral sums interval', 'It expresses the time of simulation that passes between an update of data. \n 60*10 seconds is the default.'],
            ['Total simulation time', 'It expresses the total time that passes in a simulation. \n 60*60*24*365*2 seconds is the default.'],
            ['Iterations per second', 'It expresses the speed of update of the simulation per seconds. \n 20 i/s is the default and the max value accepted.'],
            ['Interval length', 'It expresses how many iterations are going to be shown at the same time. \n  500 is the default, the interval is 1 <= x <= 1000.'],
            ['Data path', 'The path to follow to save and get the objects data.'],
            ['Conversions', 'To see the conversion operators go to \'?\' \n in the section of \'converter\'.'],
            ['Note', 'The user can use conversion operators directly \n inside the main fields.'],
            ['BUTTONS', None],
            ['Converter', 'Opens a sum, multiplication, exponential \n and variable calculator.'],
            ['Save', 'Updates the global database of configs \n with the current entries. \n Double save to save current data into new path.'],
            ['Reset', 'Set the configurations to it default value.'],
            ['Clear', 'Clears the entry sets.'],
            ['Save graphs', 'Activate to save graphs of simulation.'],
            ['Pos', 'Select position moving graph and save its data.'],
            ['Vel', 'Select velocity moving graph and save its data.'],
            ['x', 'Moving graph and save of x axis of position or velocity.'],
            ['y', 'Moving graph and save of y axis of position or velocity.']
            ]
        self.root = tk.Toplevel(parent.root)
        self.root.resizable(0,0)
        self.root.title('config')
        self.root.iconbitmap('assets//logo.ico')
        
        self.a1 = tk.Frame(self.root, width = 220, height = 200)
        self.a1.grid(row=1, column=0, sticky='nsew', pady=10)
        
        self.a2 = tk.Frame(self.root)
        self.a2.grid(row=0, column=0, sticky='nsew', pady=0)
        
        self.a3 = tk.Frame(self.root)
        self.a3.grid(row=2, column=0, sticky='nsew', pady=0)
        
        tk.Label(self.a1, text = 'Real ex time per sec:').grid(row=0,column=0, padx=5, pady=5)
        self.rtps = tk.Entry(self.a1,  width=30)
        self.rtps.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(self.a1, text = 'Integral sums interval:').grid(row=1,column=0, padx=5, pady=5)
        self.dt = tk.Entry(self.a1,  width=30)
        self.dt.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(self.a1, text = 'Total simulation time:').grid(row=2,column=0, padx=5, pady=5)
        self.tst = tk.Entry(self.a1,  width=30)
        self.tst.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(self.a1, text = 'Iterations per second:').grid(row=3,column=0, padx=5, pady=5)
        self.ips = tk.Entry(self.a1,  width=30)
        self.ips.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(self.a1, text = 'Interval length:').grid(row=4,column=0, padx=5, pady=5)
        self.il = tk.Entry(self.a1,  width=30)
        self.il.grid(row=4, column=1, padx=5, pady=5)
        
        tk.Label(self.a1, text = 'Data path:').grid(row=5,column=0, padx=5, pady=5)
        self.path = tk.Entry(self.a1,  width=30)
        self.path.grid(row=5, column=1, padx=5, pady=5)
        self.path.insert(0,path)
        self.list_entry = [self.rtps, self.dt, self.tst, self.ips, self.il, self.path]


        self.graphs = tk.BooleanVar(self.root)
        self.pos = tk.BooleanVar(self.root)
        self.vel = tk.BooleanVar(self.root)
        self.x = tk.BooleanVar(self.root)
        self.y = tk.BooleanVar(self.root)

        self.list_bool = [self.graphs, self.pos, self.vel, self.x, self.y]
        def poschange():
            if self.pos.get():
                self.vel.set(False)
            else:
                self.vel.set(True)
        def velchange():
            if self.vel.get():
                self.pos.set(False)
            else:
                self.pos.set(True)
        def xchange():
            loc1 = self.x.get()
            loc2 = self.y.get()
            if not loc1 and not loc2:
                self.x.set(True)
        def ychange():
            loc1 = self.x.get()
            loc2 = self.y.get()
            if not loc1 and not loc2:
                self.y.set(True)
        if isfile('assets//configs.csv'):
            df = pd.read_csv('assets//configs.csv')
            dfl = df.values.tolist()[0]
            for n,el in enumerate(dfl[0:5]):
                self.list_entry[n].insert(0,el)
            for n,el in enumerate(dfl[5:]):
                self.list_bool[n].set(el)
        
        def save():
            global path
            l = self.list_entry[-1].get()
            if l != '':
                df = pd.DataFrame(parent.list_val, columns = ['Name','mass','radio','x','y','vel','prad'])
                df.to_csv(path, index=False)
                proute(l)
            else:
                df = pd.DataFrame(parent.list_val, columns = ['Name','mass','radio','x','y','vel','prad'])
                df.to_csv(path, index=False)
            if not empty(self.list_entry):
                updatelist = []
                if not int(float(self.ips.get())) < 20 and int(float(self.ips.get())) - float(self.ips.get()) == 0:
                    for n in self.list_entry[0:-1]:
                        updatelist.append(int(calc(self,n.get())))
                    for n in self.list_bool:
                        updatelist.append(int(n.get()))
                    if not None in updatelist:
                        for n,u in enumerate(updatelist[0:5]):
                            self.list_entry[n].delete(0, 'end')
                            self.list_entry[n].insert(0, u)
                        df = pd.DataFrame([updatelist], columns = ['rtps','dt','tst','ips', 'il','sgraphs','pos','vel','x','y'])
                        df.to_csv('assets//configs.csv', index=False)
                        
                        ad(self, 'Config updated', 'The configurations have been updated. \n data assets updated')
                else:
                    ad(self, 'min value passed', 'The data of ips must be higher than 20. \n data assets updated')
            else:
                ad(self, 'Wrong data', 'Fill data correctly to be able to save. \n data assets updated')
        def defset():
            global defaultconfigs
            df = pd.DataFrame([defaultconfigs], columns = ['rtps','dt','tst','ips','il'])
            df.to_csv('assets//configs.csv', index=False)
            ad(self, 'Config updated', 'The configurations have been \n set to default')
        
        self.cbgrpahs = ttk.Checkbutton(self.a2,
            text='Save graphs',
            variable=self.graphs)
        self.cbgrpahs.grid(row=0, column=3,rowspan=2,padx=5, pady=5)

        self.cbpos = ttk.Checkbutton(self.a2,
            text='pos',
            variable=self.pos,
            command=poschange)
        self.cbpos.grid(row=0, column=5,padx=5, pady=1)

        self.cbvel = ttk.Checkbutton(self.a2,
            text='vel',
            variable=self.vel,
            command=velchange)
        self.cbvel.grid(row=1, column=5,padx=5, pady=1)

        self.cbx = ttk.Checkbutton(self.a2,
            text='x',
            variable=self.x,
            command=xchange)
        self.cbx.grid(row=0, column=4,padx=5, pady=1)

        self.cby = ttk.Checkbutton(self.a2,
            text='y',
            variable=self.y,
            command=ychange)
        self.cby.grid(row=1, column=4,padx=5, pady=1)

        self.b1 = tk.Button(self.a2, text = '?', width=2, padx=5, pady=0, command = lambda: helpd(self,self.list_a))
        self.b1.grid(row=0, column=0,rowspan = 2,padx=5, pady=5)
        
        self.b2 = tk.Button(self.a3, text = 'Save', width=6, padx=5, pady=0, command = lambda: save())
        self.b2.grid(row=0, column=0,padx=5, pady=5)
        
        self.b3 = tk.Button(self.a3, text = 'Reset', width=6, padx=5, pady=0, command = lambda: defset())
        self.b3.grid(row=0, column=1,padx=5, pady=5)
        
        self.b4 = tk.Button(self.a2, text = 'Converter', width=6, padx=5, pady=0, command = lambda: conversion(self))
        self.b4.grid(row=0, column=2, rowspan= 2,padx=5, pady=5)
        
        self.b5 = tk.Button(self.a3, text = 'Clear', width=6, padx=5, pady=0, command = lambda: clear(self.list_entry))
        self.b5.grid(row=0, column=2,padx=5, pady=5)
        
        self.root.transient(parent.root)
        self.root.mainloop()
class main():
    def __init__(self):
        self.list_a = [
            ['VARIABLES', None],
            ['Name','It reffers to the numeric index of the object.'],
            ['Mass', 'Mass in kg for the gravitational object.'],
            ['Radio', 'Radio in meters of the object.'],
            ['x,y', 'Positional coordinates from origin in meters.'],
            ['Vel', 'Velocity of the object in m/s.'],
            ['Angle', 'Angle of the vector velocity in radians.'],
            ['Conversions', 'To see the conversion operators go to \'?\' \n in the section of \'converter\'.'],
            ['Note 1', 'The user can use conversion operators directly \n inside the main fields.'],
            ['Note 2', 'When saved and reopen the index Name will have a .0 \n no matter that there was not before.'],
            ['BUTTONS', None],
            ['C', 'Opens the initial configs modifier.'],
            ['Converter', 'Opens a sum, multiplication, exponential \n and variable calculator.'],
            ['Last', 'Opens a view of the data of the current.'],
            ['Load last', 'Updates the local database with the values of \n the current path.'],
            ['Run last', 'Runs a simulations with the last values used in the current path.'],
            ['Save', 'Updates the local database with the current entries.'],
            ['Delete', 'Erases, if exists, the values of the data base \n with the index of \'Name\'.\n With command \'delall\' clear the current  local data base.'],
            ['Clear', 'Clears the entry sets.'],
            ['Current', 'Opens a view of the current local database. if \'l<object index>\' \n in the name field the data of the name will load.'],
            ['Run', 'Runs a simulation with the current values of the local \n database.'],
            ['Note', 'To save data in global data base you might close the simulator \n or run the simulation.']
            ]
        self.list_val = []
        self.list_index = []
        self.root = tk.Tk()
        self.root.resizable(0,0)
        self.root.title('Gravity simulator')
        self.root.iconbitmap('assets//logo.ico')
        
        self.a1 = tk.Frame(self.root)
        self.a1.grid(row=1, column=0, sticky='nsew', pady=10)
        
        self.a2= tk.Frame(self.root)
        self.a2.grid(row=2, column=0, columnspan = 2, sticky='nsew')
        
        
        self.a3 = tk.Frame(self.root)
        self.a3.grid(row=0, column=0, sticky='nsew', pady=0)
        
        tk.Label(self.a1, text = 'Name: ').grid(row=0,column=0, padx=5, pady=5)
        self.name = tk.Entry(self.a1,  width=40)
        self.name.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(self.a1, text = 'Mass: ').grid(row=1,column=0, padx=5, pady=5)
        self.mass = tk.Entry(self.a1,  width=40)
        self.mass.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(self.a1, text = 'Radio: ').grid(row=2,column=0, padx=5, pady=5)
        self.radio = tk.Entry(self.a1,  width=40)
        self.radio.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(self.a1, text = 'x: ').grid(row=3,column=0, padx=5, pady=5)
        self.x = tk.Entry(self.a1,  width=40)
        self.x.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(self.a1, text = 'y: ').grid(row=4,column=0, padx=5, pady=5)
        self.y = tk.Entry(self.a1,  width=40)
        self.y.grid(row=4, column=1, padx=5, pady=5)
        
        tk.Label(self.a1, text = 'Velocity: ').grid(row=5,column=0, padx=5, pady=5)
        self.vel = tk.Entry(self.a1,  width=40)
        self.vel.grid(row=5, column=1, padx=5, pady=5)
        
        tk.Label(self.a1, text = 'Angle: ').grid(row=6,column=0, padx=5, pady=5)
        self.angle = tk.Entry(self.a1,  width=40)
        self.angle.grid(row=6, column=1, padx=5, pady=5)
        
        self.list_entry = [self.name,self.mass,
                           self.radio,self.x,self.y,
                           self.vel,self.angle]           
        def run():
            loclen = len(self.list_index)
            if  loclen < 2:
                ad(self,'No data', 'There must be at least \n 2 objects to graph')
            else:
                df = pd.DataFrame(self.list_val, columns = ['Name','mass','radio','x','y','vel','prad'])
                df.to_csv(path, index=False)
                m.main()
        def runlast():
            pathprov = 'assets//' + path.replace('//', '-').replace('.csv', '')
            if isdir(pathprov):
                    m.main(l_data = True, route = pathprov)
            else:
                ad(self,'Not found', 'There is not last data source')
        def save(self):
            if not empty(self.list_entry):
                locname = str(calc(self,self.name.get()))
                if  locname in self.list_index:
                    self.list_val.pop(self.list_index.index(locname))
                    self.list_index.pop(self.list_index.index(locname))  
                updatelist = []
                for n in self.list_entry[1::]:
                    updatelist.append(calc(self,n.get()))
                if not None in updatelist:
                    for n,u in enumerate([locname] + updatelist):
                            self.list_entry[n].delete(0, 'end')
                            self.list_entry[n].insert(0, u)
                    self.list_val.append(list(v for v in [float(locname)] + updatelist))
                    self.list_index.append(locname)
                    order(self)
                    ad(self,'Saved', f'"{locname}" saved correctly')
            else:
                ad(self, 'Wrong data', 'Fill data correctly to be able to save')
                
        def loadlast():
            if isfile(path):
                df = pd.read_csv(path)
                df = df.values.tolist()
                self.list_val = df
                self.list_index = []
                for el in self.list_val:
                    self.list_index.append(str(el[0]))
                ad(self,'Data loaded', 'The last data source has been set \n as current.')
            else:
                ad(self,'Not found', 'There is not last data source')
            
        def delete():
            if self.name.get() == 'delall':
                self.list_val = []
                self.list_index = []
                self.name.delete(0, 'end')
                self.name.insert(0, '')
                ad(self, 'Data cleared', 'The current data has been cleared')
            else:
                locname = self.name.get()
                if  locname in self.list_index:
                    self.list_val.pop(self.list_index.index(locname))
                    self.list_index.pop(self.list_index.index(locname)) 
                    ad(self, 'Deleted', f'The data of "{locname}" has been deleted')
                else:
                    ad(self, 'Not found', f'The name "{locname}" does not exist')
        def current():
            loc = self.name.get()
            if 'l' in loc:
                loc = loc.split('l')
                if len(loc) == 2:
                    loc = loc[1]
                    if loc in self.list_index:
                        loc2 = self.list_val[self.list_index.index(loc)]
                        for n,e in enumerate(self.list_entry):
                            e.delete(0,"end")
                            e.insert(0,loc2[n])
                    else:
                        ad(self, 'Not found', f'The name "{loc}" does not exist')
            else:
                show(self, list_a = self.list_val)
        self.b1 = tk.Button(self.a2, text = 'Run', width=6,padx=5,pady=0, command = lambda: run())
        self.b1.grid(row=0, column = 4, sticky = 'E',padx=5, pady=5)
        tk.Frame(self.a2, width = 20).grid(row=0, column = 0)
        self.b2 = tk.Button(self.a2, text = 'Save', width=6,padx=5,pady=0, command = lambda: save(self))
        self.b2.grid(row=0, column=0,padx=5, pady=5)
        
        self.b3 = tk.Button(self.a2, text = 'Delete', width=6,padx=5,pady=0, command = lambda: delete())
        self.b3.grid(row=0, column=1,padx=5, pady=5)
        
        self.b4 = tk.Button(self.a2, text = 'Clear', width=6,padx=5,pady=0, command = lambda: clear(self.list_entry))
        self.b4.grid(row=0, column=2,padx=5, pady=5)
        
        self.b5 = tk.Button(self.a3, text = 'C', width=2, padx=5, pady=0, command = lambda: config(self))
        self.b5.grid(row=0, column=0,padx=5, pady=5)
        
        self.b6 = tk.Button(self.a3, text = '?', width=2, padx=5, pady=0, command = lambda: helpd(self,self.list_a))
        self.b6.grid(row=0, column=1,padx=5, pady=5)
        
        self.b7 = tk.Button(self.a3, text = 'Last', width=2, padx=5, pady=0, command = lambda: show(self))
        self.b7.grid(row=0, column=3,padx=5, pady=5)
        
        self.b8 = tk.Button(self.a3, text = 'Converter', width=6, padx=5, pady=0, command = lambda: conversion(self))
        self.b8.grid(row=0, column=2,padx=5, pady=5)
        
        self.b9 = tk.Button(self.a3, text = 'Run last', width=6, padx=5, pady=0, command = lambda: runlast())
        self.b9.grid(row=0, column=5,padx=5, pady=5)
        
        self.b10 = tk.Button(self.a3, text = 'Load last', width=6, padx=5, pady=0, command = lambda: loadlast())
        self.b10.grid(row=0, column=4,padx=5, pady=5)
        
        self.b11 = tk.Button(self.a2, text = 'Current', width=6, padx=5, pady=0, command = lambda: current())
        self.b11.grid(row=0, column=3,padx=5, pady=5)
        loadlast()
        self.root.mainloop()
        df = pd.DataFrame(self.list_val, columns = ['Name','mass','radio','x','y','vel','prad'])
        df.to_csv(path, index=False)


if __name__ == "__main__":
    main()
