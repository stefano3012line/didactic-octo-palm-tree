import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import math

def G(x,sigma,mu):
    return np.exp(-1/2*(x-mu)**2/(sigma)**2)/(sigma*np.sqrt(np.pi*2))

sigma=10
mu=0
x=np.linspace(-50,50,1000)
plt.errorbar(x,np.full(len(x),0))
plt.errorbar(x,G(x,sigma,mu))
plt.show()