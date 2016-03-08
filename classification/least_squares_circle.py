import numpy as np
from scipy import optimize

# Adapted from the SciPy Cookbook

def calc_R(x,y, xc, yc):
    """ calculate the distance of each 2D points from the center (xc, yc) """
    return np.sqrt((x-xc)**2 + (y-yc)**2)

def f(c, x, y):
    """ calculate the algebraic distance between the data points and the mean circle centered at c=(xc, yc) """
    Ri = calc_R(x, y, *c)
    return Ri - Ri.mean()

def leastsq_circle(x,y, centre_estimate):
    centre, ier = optimize.leastsq(f, centre_estimate, args=(x,y))
    xc, yc = centre
    Ri       = calc_R(x, y, *centre)
    R        = Ri.mean()
    residu   = np.sum((Ri - R)**2)
    return xc, yc, R, residu
