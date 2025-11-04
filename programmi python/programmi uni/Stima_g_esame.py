import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
mm=6.903
m_pe=7.813
s_m=0.001
l_0=19.0
l_i=np.array([20.9,22.6,22.6,25.9,36.5,53.6])
m_i=np.array([5.006,10.007,10.009,20.019,50.024,100.030])
#per 30 periodi
t_i=np.array([13.54,15.58,15.53,18.87,26.63,35.97])
t_i=t_i/30
print(np.std(t_i))
s_t_i=0.1/30
M_i=m_i+np.full(len(m_i),m_pe)
M_tot=M_i+(mm/3)

def T(M_tot,k):
    return 2*np.pi*np.sqrt(M_tot/k)
popt,pcov=curve_fit(T,M_tot,t_i,absolute_sigma=True,sigma=np.full(len(t_i),s_t_i))

fig=plt.figure("Grafico periodo-massa")
fig.add_axes((0.1, 0.37, 0.8, 0.6))
plt.grid(which='both', ls='dashed', color='gray')
k_hat=popt
n=np.linspace(min(M_tot),max(M_tot),1000)
plt.plot(n,T(n,k_hat))
plt.ylabel('Periodi[s]')
plt.xlabel('Masse[g]')
plt.errorbar(M_tot,t_i,fmt='.',yerr=s_t_i)

fig.add_axes((0.1, 0.07, 0.8, 0.2))
plt.grid(which='both', ls='dashed', color='gray')
plt.errorbar(M_tot,t_i-T(M_tot,k_hat),yerr=s_t_i,fmt='.')
plt.savefig('grafico_periodo-massa.pdf')

chi2_k=np.sum(((T(M_tot,k_hat)-t_i)/s_t_i)**2)
print(chi2_k/5,'+-',np.sqrt(2/5))

plt.show()
s_k=np.sqrt(pcov.diagonal())
k=k_hat
print('k_hat=',k_hat/1000,'+-',s_k/1000)

d_l=-np.full(len(l_i),l_0)+l_i
#a è il coeff.angolare della retta e 7.813 la massa della pedana e quindi l'offset della misura
def D_l(m,a):
    return (m-7.813)*a

s_l=np.full(len(d_l),0.1)
s_lp=np.sqrt(2*(s_l**2))
s_eff=np.sqrt(s_lp**2+s_k**2)

popt,pcov=curve_fit(D_l,M_i,d_l,absolute_sigma=True,sigma=s_eff)

s_m=np.full(len(m_i),0.001)
#a e g_hat si riferiscono al coeff.angolAre
g_hat=popt
g_eff=g_hat*k_hat

#s_g=np.sqrt(np.sum(s_lp/(s_m)))
s_a=np.sqrt(pcov.diagonal())





fig=plt.figure("Grafico allungamento-massa")
fig.add_axes((0.1, 0.37, 0.8, 0.6))
plt.grid(which='both', ls='dashed', color='gray')
x=np.linspace(np.min(M_i),np.max(M_i),1000)
plt.plot(x,D_l(x,g_hat))
plt.errorbar(M_i,d_l,fmt='.',yerr=s_lp)
plt.ylabel('allungamento molla[cm]')
plt.xlabel('Massa totale[g]')

fig.add_axes((0.1, 0.07, 0.8, 0.2))
plt.grid(which='both', ls='dashed', color='gray')
plt.errorbar(M_i,d_l-D_l(M_i,g_hat),yerr=s_lp,fmt='.')
s_g=np.sqrt((k_hat*s_a)**2+(g_hat*s_k)**2)
plt.savefig('grafico_allungamento-massa.pdf')
plt.show()
print(g_hat)
print('g=',g_eff/100,'+-',s_g/100)




chi2=np.sum(((d_l-D_l(M_i,g_hat))/(s_lp))**2)
print(chi2/5,'+-',np.sqrt(2/5))





