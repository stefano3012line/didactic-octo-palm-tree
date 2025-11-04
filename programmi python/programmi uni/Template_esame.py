import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import math

Ri=np.array([0,6,10,14,18,24,30,36,40,50])
Rr=np.array([0,4,6,8,12,16,20,24,28,30])

def f(m,x):
    return m*x

sigma_Ri = np.full(Ri.shape,2)
#plot principale
#print(N2(theta_i,theta_r,N1))
popt,pcov=curve_fit(f,Rr,Ri,sigma=sigma_Ri,absolute_sigma=True)
m_hat=popt


fig=plt.figure("rifrazione plexiglass")
fig.add_axes((0.1, 0.37, 0.8, 0.6))
plt.plot(f(m_hat,Rr),Rr,color='r')
plt.errorbar(Ri,Rr,xerr=2,yerr=2,fmt='.')
plt.ylabel('corda in uscita[mm]')





plt.grid(which='both',ls='dashed',color='gray')
fig.add_axes((0.1, 0.1, 0.8, 0.2))
plt.grid(which='both', ls='dashed', color='gray')
plt.xlabel('corda in ingresso[mm]')
plt.plot(-2,0,color="gray")
plt.plot(52,0,color="gray")
plt.errorbar(Ri,f(m_hat,Rr)-Ri,yerr=2*np.sqrt(2.5),fmt=".")


plt.savefig('indice di rifrazione.pdf')
plt.show()
print(m_hat)
print((np.sqrt(pcov.diagonal())))
chi2=np.sum(((f(m_hat,Rr)-Ri)**2)/(2*np.sqrt(2.5))**2)
print(chi2/9, "+-",np.sqrt(2/9) )