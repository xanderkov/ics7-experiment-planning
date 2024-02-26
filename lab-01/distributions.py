import random
import math
import numpy.random as nr


def gauss_t(params):
    mx = params[0]
    dx = params[1]
    
    return nr.normal(mx, dx)
