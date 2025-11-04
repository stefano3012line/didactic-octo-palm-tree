#ingrandimento di uno specchio in funzione della posizione
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import math



def G(p,f):
    return f/(p-f)
f=-20
fig=plt.figure('ingrandimento')
#fig.add_axes((0.1, 0.37, 0.8, 0.6))
p=np.linspace(-200,200,10000)
plt.plot(p,G(p,f))
plt.savefig('ingrandimento ottica')
plt.show()
