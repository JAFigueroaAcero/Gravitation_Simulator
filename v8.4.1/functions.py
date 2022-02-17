# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 22:11:22 2021

@author: Juan Antonio

Title: Funciones de Gravitación

Ver: 6.2
"""

import numpy as np
rev = 2 * np.pi      #revolution value
G = 6.67 * (10**-11) #Gravity constant

def positionrad_angular_rm(va,t):
    '''
    Works as a convertor of velocity * times.

    Parameters
    ----------
    va : velocity vector.
    t : time vector.

    Returns
    -------
    fix2radpi : uses the prad fix to convert the value of va * t.
    '''
    prad = va * t
    return fix2radpi(prad)

def magnitude(x1,y1,x2,y2):
    '''
    Takes the linear bidimensional position and calculates its magnitude

    Parameters
    ----------
    x1, y1, x2, y2

    Returns
    -------
    Magnitude : value of a bidimensional magnitude.

    '''
    return ((x2-x1)**2 + (y2-y1)**2)**0.5
    
def fix2radpi(prad):
    '''
    Reductor of a max of 1 revolution.

    Parameters
    ----------
    prad : radians value.

    Returns
    -------
    The max of 6.14... as a radians value.

    '''
    
    if prad >= rev:
        reduc = int(prad/rev)
        return prad - reduc * rev
    else:
        return prad

def positionxy_angle(positionrad,r):
    '''
    Data of x, y obtanied by the radians value and the radius

    Parameters
    ----------
    positionrad : radian circular positions of the vector.
    r : radius of magnitude of the object.

    Returns
    -------
    x : x axis of the circle.
    y : y axis of the circle.

    '''
    x = r * np.cos(positionrad)
    y = r * np.sin(positionrad)
    return (x,y)

def angle_frac2rad(x,y):
    '''
    Convertor to radians from x, y axis.

    Parameters
    ----------
    x : x axis of the circle.
    y : y axis of the circle.

    Returns
    -------
    radians value of the x,y axis.

    '''
    
    inc = np.arctan2(y,x)
    if inc >= 0:
        return inc
    else:
        return 2*np.pi+inc
ms = []
def masssum(a):
    '''
    gets the mass of all the posibles for masspoint function.

    Parameters
    ----------
    a : array set of values.

    Returns
    -------
    None
    '''
    global ms
    for n in range(len(a)):
        ac = a.copy()
        ac = np.delete(ac, n)
        val = 0
        for n in ac:
            val += n[1]
        ms.append(val)
GM = []
def gm(a,dt):
    '''
    gets the repeated operations for actvec2 function.

    Parameters
    ----------
    a : array set of values.
    dt : time to apply in the difference.

    Returns
    -------
    None
    '''
    global GM
    global DT
    DT = dt
    for n,m in enumerate(a):
        u = (G * ms[n] * DT**2)/2
        v = G * ms[n] * DT
        GM.append([u,v])
def masspoint(a, eje, passing):
    '''
    gets the masspoint of an axis from a array set.

    Parameters
    ----------
    a : array set of values.
    eje : selector of one of both axis (0-1).
    passing : vector thats going to be represented.

    Returns
    -------
    axis : coordinate that is represented.

    '''
    num = 0
    ac = a.copy()
    ac = np.delete(ac, passing)
    
    for n in ac:
        num += (n[1]*n[3+eje])
    return num/ms[passing]

def actvec2(ni,vi,r,sincos,using):
    '''
    Updates the vector with the initial data and a dt interval.

    Parameters
    ----------
    ni : linear initial position.
    vi : linear initial velocity.
    r : linear distance between values.
    sincos : bidemensional axis that is being applied as np.sin, np.cos.
    using : using data of matrices.

    Returns
    -------
    nf : linear final position.
    vf : linear final velocity.

    '''
    nf = ni + vi * DT + GM[using][0]/(r**2) * sincos
    vf = vi + (GM[using][1])/(r**2) * sincos
    return nf,vf

def actvecglob3(a, using):
    '''
    Updates an array of set of values of a a global data to apply the actvec2 inside.

    Parameters
    ----------
    a : array set of values.
    using : vector thats going to be represented.

    Returns
    -------
    The a[using] array to be updated

    '''
    ac = a.copy()
    ac = np.delete(ac, using)
    
    x = masspoint(a, 0, using)
    y = masspoint(a, 1, using)
    
    r = magnitude(x, y, a[using][3], a[using][4])
    x -= a[using][3]
    y -= a [using][4]
    prad = angle_frac2rad(x, y)
    
    xi, vx = actvec2(a[using][3], a[using][5], r, np.cos(prad),using)
    yi, vy = actvec2(a[using][4], a[using][6], r, np.sin(prad),using)
    
    return np.array([a[using][0],a[using][1],a[using][2],xi,yi,vx,vy])
    
def vtan(m,r):
    '''
    tangential velocity.

    Parameters
    ----------
    m : mass of origin.
    r : distance from origin.

    Returns
    -------
    the tangential velocity of (G * m / r)**0.5

    '''
    return (G * m / r)**0.5



