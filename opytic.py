#here comes all the external libraries imports of opytics
from scipy.optimize import fsolve
import numpy as np
import matplotlib.pyplot as plt
from math import *

##low-level functions
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







## Optical object and beams definition

class optical_object():
    def __init__(self):
        pass
    def draw(self): #calls a plt.plot function to draw the object on the graph. Can get some arguments
        pass
    def simulate_beam(self, ray): #takes a beam as input and outputs the new object beam at the output
        return ray


class lens(optical_object):
    def __init__(self,s1,s2,radius,middle_thickness,effective_focal_length,back_focal_length,index=1.52, x_lens = 0,reversed = False):
        optical_object.__init__(self)
        self.radius = radius #radius of the lens
        self.mthick = middle_thickness #thickness of the middle layer, between the two suurfaces
        self.efl = effective_focal_length
        self.bfl = back_focal_length
        self.index = index #refractive index of the lens material
        if not reversed:
            self.s1 = parametric(lambda y: s1(y) - s1(self.radius) + effective_focal_length-back_focal_length-middle_thickness - s2(0) + s2(self.radius), lambda y: y) #reposition these function such as the optical center is at (0,0)
            self.s2 = parametric(lambda y: s2(y) - s2(0) + effective_focal_length-back_focal_length, lambda y: y) #ok
        else:
            self.s1 = parametric(lambda y: -s2(y) + s2(0)-effective_focal_length+back_focal_length, lambda y: y) #reposition these function such as the optical center is at (0,0)
            self.s2 = parametric(lambda y: -s1(y) + s1(self.radius)-effective_focal_length+back_focal_length+middle_thickness + s2(0) - s2(self.radius), lambda y: y)

    def draw(self, npts = 30):
        x1,y1 = self.s1.xysample(-self.radius,self.radius,npts)
        x2,y2 = self.s2.xysample(-self.radius,self.radius,npts)
        closed_y = y1 + y2[::-1] + [y1[0]]
        closed_x = x1 + x2[::-1] + [x1[0]]
        plt.plot(closed_x,closed_y, color='black')

    def simulate_beam(self,ray): #y0 is the intersection height of the non diffracted beam with the y_axis
        #find y1 the intersection with s1
        x0,y0,i0 = ray.state()
        ray_curve = parametric(lambda t: t*cos(i0)+x0, lambda t: t*sin(i0)+y0)
        x1,y1,t1 = intersection(self.s1, ray_curve)
        angle_s1 = angle(self.s1,t1) #angle de la surface avec la verticale

        a1 = angle_s1 + i0 #angle d'incidence sur s1
        a2 = refraction(a1, 1, self.index) #angle réfracté sur s2
        i1 = a2 - angle_s1 #angle dans le verre avec l'horizontale
        new_ray = beam(x1,y1,i1)

        #find y2 the intersection with s2
        ray_curve = parametric(lambda t: t*cos(i1)+x1, lambda t: t*sin(i1)+y1)
        x2,y2,t2 = intersection(self.s2, ray_curve)
        angle_s2 = angle(self.s2, t2)

        b1 = angle_s2 + i1
        b2 = refraction(b1, self.index, 1)
        i2 = b2 - angle_s2
        new_ray.become(beam(x2,y2,i2))
        return new_ray


class interface(optical_object):
    def __init__(self, n1,n2, x_medium):
        optical_object.__init__(self)
        interface.x = x_medium
        interface.n1 = n1
        interface.n2 = n2
        self.drawn = False

    def simulate_beam(self,ray):
        x,y,i = ray.state()
        x1,y1,i1 = interface.x, (interface.x-x)*tan(i) + y, refraction(i, interface.n1, interface.n2)
        return beam(x1,y1,i1)

    def draw(self,length):
        plt.plot([interface.x]*2, [-length,length], color='black')


class mirror(optical_object):
    def __init__(self, s, x0 = 0, y0 = 0):
        optical_object.__init__(self)
        self.s = s + parametric(lambda t: x0, lambda t: y0) #surface of the mirror

    def simulate_beam(self, ray):
        x0,y0,i0 = ray.state()
        ray_curve = parametric(lambda t: t*cos(i0)+x0, lambda t: t*sin(i0)+y0)
        x1,y1,t = intersection(self.s, ray_curve)
        i1 = -i0-2*atan(derivative(self.s.x,t)/derivative(self.s.y,t))+pi
        return beam(x1,y1,i1)

    def draw(self, tmin, tmax, npts=30):
        x_vals,y_vals = self.s.xysample(tmin,tmax)
        plt.plot(x_vals,y_vals, color='black')


class beam_state: #a class that builds objects that stores a beam's state
    def __init__(self,x,y,i,n=1):
        self.x = x #initial point x
        self.y = y #initial point y
        self.i = natural_angle(i) #initial angle i

class beam: #class that handle beam propagation
    def __init__(self,x0,y0,i0):
        self.cur_state = beam_state(x0,y0,i0)
        self.path = [beam_state(x0,y0,i0)]

    def go_through(self, obj):
        self.become(obj.simulate_beam(self))

    def become(self,new_ray):
        for step in new_ray.path:
            self.path.append(step)
        self.cur_state = new_ray.cur_state

    def state(self):
        return self.cur_state.x,self.cur_state.y,self.cur_state.i

    def draw(self, lmax):
        x,y,i = self.state()
        plt.plot([step.x for step in self.path] + [x + lmax*cos(i)], [step.y for step in self.path] + [y + lmax*sin(i)], color='green')


def show(even_axis = True):
    if even_axis: plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
