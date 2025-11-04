import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import math
def T(l,g):
    return 2*np.pi*np.sqrt(l/g)
g=9.806
l=np.linspace(0.1,200,2000)

fig=plt.figure("Grafico periodo lunghezza")

plt.grid(which='both', ls='dashed', color='gray')
plt.xlabel('l[m]')
plt.ylabel('T[s]')
plt.plot(l,T(l,g))

plt.show()