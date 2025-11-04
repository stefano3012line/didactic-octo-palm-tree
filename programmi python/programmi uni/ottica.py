import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import math
def N2(theta_i,theta_r):
    return  N1*np.sin(theta_i)/np.sin(theta_r)
N1=1
Ri,Rr=np.loadtxt(r"C:\Users\Dell\Desktop\Uni_lab\dati ottica\ottica.txt",unpack=True)

def f(m,x):
    return m*x

sigma_Ri = np.full(Ri.shape,1)
#plot principale
#print(N2(theta_i,theta_r,N1))
popt,pcov=curve_fit(f,Rr,Ri,sigma=sigma_Ri)
m_hat=popt

x=np.linspace(0,60,1000)
fig=plt.figure("rifrazione plexiglass")
fig.add_axes((0.1, 0.37, 0.8, 0.6))
plt.plot(f(m_hat,x),x,color='r')
plt.errorbar(Ri,Rr,xerr=1,yerr=1,fmt='.')
plt.ylabel('corda in uscita')



plt.grid(which='both',ls='dashed',color='gray')
fig.add_axes((0.1, 0.1, 0.8, 0.2))
plt.grid(which='both', ls='dashed', color='gray')
plt.xlabel('corda in ingresso')
plt.errorbar(Rr,f(m_hat,Rr)-Ri,yerr=1,fmt=".")
plt.savefig('indice di rifrazione.pdf')
plt.show()
print(m_hat)
print((np.sqrt(pcov.diagonal())))
chi2=np.sum(((f(m_hat,Rr)-Ri)**2)/(2))
print(chi2/10, "+-",np.sqrt(2/10) )

##

p,qi=np.loadtxt(r"C:\Users\Dell\Desktop\Uni_lab\dati ottica\lente divergente ottica.txt", unpack=True)
#print(p,qi)


p=-10/p
qi=10/qi
#passaggio a metri


def f(x,q):
    return -x+q


c=0
sqi=np.full(len(qi),0.)
while c<len(qi):
    sqi[c]=.5*(qi[c]**2)
    #print(sqi[c])
    c=c+1


c=0
sp=np.full(len(p),0.)
while c<len(p):
    sp[c]=.5*(p[c]**2)
   # print(sp[c])
    c=c+1



#caricamento vettore degli errori



popt,pcov=curve_fit(f,p,qi,sigma=np.sqrt(sqi**2 +sp**2))
q_hat=popt
sigma_q=np.sqrt(pcov.diagonal())

#plot principale
fig=plt.figure('Distanza focale')
fig.add_axes((0.11,0.38,0.8,0.6))

plt.plot(p,f(p,q_hat))
plt.errorbar(p,qi,yerr=sqi,xerr=sp,fmt='.')
plt.grid(which='both',ls='dashed',color='gray')
plt.ylabel('q[cm]')

fig.add_axes((0.11, 0.1, 0.8, 0.2))
plt.grid(which='both', ls='dashed', color='gray')
plt.errorbar(p,qi-f(p,q_hat),fmt=".",yerr=np.sqrt(sqi**2 +sp**2))

plt.xlabel('p[cm]')

print(1/q_hat)
print(sigma_q*(1/(q_hat**2)))
chi2=np.sum(((qi-f(p,q_hat))/np.sqrt(sqi**2 +sp**2))**2)
print(chi2/8)
#sigma chi2 = radice di 2 fratto ddof
print(np.sqrt(2/8))
plt.savefig('Distanza focale.pdf')
plt.show()




