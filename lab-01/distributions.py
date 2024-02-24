import random
import math
import numpy.random as nr
def uniform_t(params):
    mx = params[0]
    dx = params[1]
    
    apb = 2 * mx
    bma = 12 * dx / apb
    b = apb + bma
    a = apb - b
    
    #a, b = params[0], params[1]
    return a + (b - a) * random.random()

def exp_t(params):
    lamb = params[0]
    return -1 / lamb * math.log(1 - random.random())

def gauss_t(params):
    mx = params[0]
    dx = params[1]
    
    return nr.normal(mx, dx)
