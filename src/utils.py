##low-level functions

#here comes all the external libraries imports of opytics
from scipy.optimize import fsolve
import numpy as np
import matplotlib.pyplot as plt
from math import *


def straight(x0,y0,i): #parametric straight line with an angle i with the axis Ox
    return parametric(lambda t: x0 + cos(i)*t, lambda t: y0 + sin(i)*t)

def flat_surface(i): #make a parametric flat surface that has an angle i with the axis Ox
    return parametric(lambda t : cos(i)*t, lambda t : sin(i)*t)

def aspheric_surface(R, k = 0, a4 = 0, a6 = 0, a8 = 0, a10 = 0): #make the sfc equation for aspheric lenses
    def z(y):
        return y**2/(R*(1+sqrt(1-(1+k)*y**2/R**2))) + a4*y**4 + a6*y**6 + a8*y**8 + a10*y**10
    return z

def refraction(i1, n1, n2): #computes descartes refraction law
    try:
        return asin(n1/n2*sin(i1))
    except:
        return 0

def derivative(f,x,h = 10**(-6)): #compute f derivatives on x, with a h step (10**(-6) is usually the best precision)
    return (f(x+h) - f(x-h))/(2*h)

def natural_angle(i): #makes the 2 pi modulus to get the angle such as -pi<=angle<pi
    return (i+pi)%(2*pi)-pi

class parametric: #define parametric equations
    def __init__(self, xfunc, yfunc):
        self.x = xfunc
        self.y = yfunc
    def __call__(self, t):
        return np.array([self.x(t), self.y(t)])
    def __add__(self, obj):
        xtemp = lambda t: self.x(t) + obj.x(t)
        ytemp = lambda t: self.y(t) + obj.y(t)
        return parametric(xtemp,ytemp)
    def __sub__(self, obj):
        xtemp = lambda t: self.x(t) - obj.x(t)
        ytemp = lambda t: self.y(t) - obj.y(t)
        return parametric(xtemp,ytemp)
    def xysample(self, tmin, tmax, nbpts=30): #returns a sample (for plotting the surface)
        x = []
        y = []
        for t in np.linspace(tmin, tmax, nbpts):
            x.append(self.x(t))
            y.append(self.y(t))
        return x,y

def intersection(c1,c2): #return the point of intersection between the curves c1 and c2
    t1 = fsolve(lambda t: c1(t[0])-c2(t[1]), [0,0])[0]
    x1,y1 = c1(t1)
    return x1,y1,t1

def angle(c,t):
    return atan(derivative(c.x,t)/derivative(c.y,t))
