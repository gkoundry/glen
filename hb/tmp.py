from GLM import GLM
from scipy.optimize import fmin,fmin_powell,fmin_cobyla,anneal,basinhopping
import pandas
import random
import copy
import math
import numpy as np
import sys
from itertools import product

def AMS(s, b):
    """ Approximate Median Significance defined as:
        AMS = sqrt(
                2 { (s + b + b_r) log[1 + (s/(b+b_r))] - s}
              )
    where b_r = 10, b = background, s = signal, log is natural logarithm """

    br = 10.0
    radicand = 2 *( (s+b+br) * math.log (1.0 + s/(b+br)) -s)
    if radicand < 0:
        print 'radicand is negative. Exiting'
        exit()
    else:
        return math.sqrt(radicand)

print AMS(230,4000)
print AMS(230,4008)
for s in (100,200,300):
    for b in (4000,6000,8000):
        print '%s %s' % (AMS(s,b),s/math.sqrt(b))
