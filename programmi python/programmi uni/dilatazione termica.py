import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.optimize import least_squares


#lunghezza d'onda in nanometri
lam =532

#lunghezza barra in cm
L_0=9

#numero di frange contate
N=np.array([38,73,119,69])
sigma_N=np.array([2,3,4,3])



#variazione di temperatura osservata
dT=np.array([5.2,10.2,15.8,9.3])
#funzione di fit
def F(dT,al):
    N=(2*al*dT*L_0)/lam
    return N

#stima valori ottimali
popt,pcov = curve_fit(F,dT,N,sigma=sigma_N,absolute_sigma=True)

err = np.sqrt(pcov.diagonal())

#chi quadro
chi=np.sum(((N-F(dT,popt))/sigma_N)**2)

#print dei dati
print(popt)
print(err)
print(chi/3)
#plot dati
plt.errorbar(dT,N,sigma_N,fmt='.')
x=np.linspace(min(dT),max(dT),10)
plt.plot(x,F(x,popt))
plt.show()
##Fit alternativo

#lunghezza d'onda in nanometri
lam =532

#lunghezza barra in cm
L_0=9

#numero di frange contate
N=np.array([31,73,112,67])


#variazione di temperatura osservata
dT=np.array([4.2,10.2,14.8,9])
sigma_dT=np.array([0.14,0.14,0.14,0.14])
#funzione di fit
def F(N,al):
    dT=N*lam/(2*al*L_0)
    return dT

#stima valori ottimali
popt,pcov = curve_fit(F,N,dT,sigma=sigma_dT,absolute_sigma=False)

err = np.sqrt(pcov.diagonal())

#chi quadro
chi=np.sum(((dT-F(N,popt))/sigma_dT)**2)

#print dei dati
print(popt)
print(err)
print(chi)
#plot dati
plt.errorbar(N,dT,sigma_dT,fmt='.')
x=np.linspace(min(N),max(N),10)
plt.plot(x,F(x,popt))
plt.show()





