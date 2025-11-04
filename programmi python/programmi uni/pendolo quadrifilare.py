import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
t,T,tT=np.loadtxt(r"C:\Users\Dell\Desktop\Uni_lab\Dati pendolo quadrifilare\pendoloquadr3.txt", unpack=True)


w=19.8
sw=0.05
l=1121.78
sl=0.05
D=1150.00
sD=1
stT=0.0001
j=0

def v_0(w,tT,l,D):
    return (w/tT)*(l/D)

#plot dei dati

V_0=v_0(w,tT,l,D)

sV0=np.zeros(len(V_0))

for j in range(len(tT)):
    sV0[j]=np.sqrt(((l/(tT[j]*D))*sw)**2 + (w/tT[j])**2*sl**2+(w/(D*tT[j]**2))**2*stT**2+(w*l/(tT[j]*D**2))**2*sD**2)/12



fig=plt.figure("velocità tempo")
fig.add_axes((0.1, 0.37, 0.8, 0.6))
plt.ylabel('velocity[mm/s]')
plt.grid(which='both',ls='dashed',color='gray')
plt.errorbar(t[::10],v_0(w,tT,l,D)[::10],yerr=sV0[::10],fmt=".")



p0=(802,400)
def V_t(t,V_0,tau):
    return V_0*np.exp(-t/tau)

#fit dati
popt,pcov=curve_fit(V_t,t,V_0,p0=p0,sigma=sV0,absolute_sigma=True)
V_hat,tau_hat=popt
plt.plot(t,V_t(t,V_hat,tau_hat))


#grafico resudui
fig.add_axes((0.1, 0.1, 0.8, 0.2))
plt.xlabel('time[t]')
plt.grid(which='both', ls='dashed', color='gray')
plt.errorbar(t[::10],(v_0(w,tT,l,D)- V_t(t,V_hat,tau_hat))[::10],yerr=sV0[::10],fmt=".")
plt.savefig('Velocità-Tempo')
plt.show()

##

def theta_0(V_0,l):
    return np.arccos(1-(V_0**2)/(2*9817*l))

theta=theta_0(V_0,l)


'''
a=(((V_0/(9817*l)*1/(np.sqrt((-(V_0**4))/(4*(9817**2)*(l**2))+((V_0**2)/(9817*l)))))**2)) * (sV0**2)
b=1/((np.sqrt(-(V_0**4)/(4*(9817**2)*(l**2))+(V_0**2)/(9817*l))*(V_0**2)/(2*9817)*1/(-l**2))**2)*(sl**2)
stheta=np.sqrt(a**2+b**2)/10000000000000'''



a=(V_0/(9817*l))/(((V_0**2)/(9817*l)-((V_0**4)/((2*9817*l)**2)))**(1/2))*(sV0)
b=((V_0**2)/(2*9817*(l**2)))/(((V_0**2)/(l*9817)-((V_0**4)/((2*9817*l)**2)))**(1/2))*sl
stheta=np.sqrt((a**2)+(b**2))


#print(stheta)
#print(theta)
#fit principale
def fp(theta,l):
    return 2*np.pi*np.sqrt((l/9817))*(1+((theta**2)/16)+(theta**4)*11/3072)
popt,pcov=curve_fit(fp,theta[::],T[::])
'''absolute_sigma=True,sigma=stheta[::]'''
l_hat=popt

fig=plt.figure("periodo angolo[s]")
fig.add_axes((0.1, 0.37, 0.8, 0.6))
plt.ylabel('angolo[rad]')
plt.grid(which='both',ls='dashed',color='gray')
plt.errorbar(theta[:500:5],T[:500:5],stT,stheta[:500:5],fmt=".")

plt.plot(theta[:500:],fp(theta[:500:],l_hat))



#residui
fig.add_axes((0.1, 0.1, 0.8, 0.2))
plt.grid(which='both', ls='dashed', color='gray')
plt.xlabel('periodo[s]')
plt.errorbar(theta[:500:5],fp(theta[:500:5],l_hat)-T[:500:5],xerr=stheta[:500:5],yerr=stT,fmt=".")
plt.savefig('Periodo-Angolo')
plt.show()
chi2=np.sum(((fp(theta[:500:],l_hat)-T[:500:])/stheta[:500:])**2)/(len(theta)-1)
print('chi quadro ridotto=',chi2,'+-',np.sqrt(2/(len(T)-1)))





