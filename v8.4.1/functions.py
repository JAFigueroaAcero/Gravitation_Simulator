# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 22:11:22 2021

@author: Juan Antonio

Title: Funciones de Gravitación

Ver: 6.1
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
    axis: coordinate that is represented.
    den : sum of the masses of the array set excpeting the passing value.

    '''
    num = 0
    den = 0
    ac = a.copy()
    ac = np.delete(ac, passing)
    
    for n in ac:
        num += (n[1]*n[3+eje])
        den += n[1]
    return num/den, den

def actvec2(ni,vi,m,r,dt,sincos):
    '''
    Updates the vector with the initial data and a dt interval.

    Parameters
    ----------
    ni : linear initial position.
    vi : linear initial velocity.
    m : mass of the gravitation.
    r : linear distance between values.
    dt : time to apply in the difference.
    sincos : bidemensional axis that is being applied as np.sin, np.cos.

    Returns
    -------
    ni : linear final position.
    vf : linear final velocity.

    '''
    nf = ni + vi * dt + (G * m * dt**2)/(2 * r**2) * sincos
    vf = vi + (G * m * dt)/(r**2) * sincos
    return nf,vf

def actvecglob3(a, dt, using):
    '''
    Updates an array of set of values of a a global data to apply the actvec2 inside.

    Parameters
    ----------
    a : array set of values.
    dt : time to apply in the difference.
    using : vector thats going to be represented.

    Returns
    -------
    The a[using] array to be updated

    '''
    ac = a.copy()
    ac = np.delete(ac, using)
    
    x,den = masspoint(a, 0, using)
    y, _ = masspoint(a, 1, using)
    
    r = magnitude(x, y, a[using][3], a[using][4])
    x -= a[using][3]
    y -= a [using][4]
    prad = angle_frac2rad(x, y)
    
    xi, vx = actvec2(a[using][3], a[using][5], den, r, dt, np.cos(prad))
    yi, vy = actvec2(a[using][4], a[using][6], den, r, dt, np.sin(prad))
    
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



