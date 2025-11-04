import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit



x=np.array([30.6,35.0,40.0,45.0,50.1,54.7])
t=np.array([1.794,2.035,2.301,2.559,2.860,3.153])
X=np.array([min(t-5),max(t-5)])
Y=np.array([0,0])
sigma_x = np.full(x.shape, 0.4)
sigma1 = 0.5*0.3/100
sigma2 = 0.2*0.3/100
sigma_t = np.array([sigma1,sigma1,sigma1,sigma1,sigma2, sigma1])
x = 2*x
def f(x,c):
    y = c*x
    return y

popt, pcov = curve_fit(f,t,x,sigma= sigma_x)
incertezze = np.sqrt(pcov.diagonal())

res = (x - f(t,popt))/sigma_x
xx = np.linspace(min(t), max(t), 500)
yy = f(xx,popt)

fig = plt.figure('velocità del suono')
ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)

ax1.plot(xx,yy, color='coral')
ax1.set_ylabel('distanza[cm]',fontsize= 17,labelpad = 25)
ax1.errorbar(t,x,yerr=0.8,xerr=0.008,color= 'royalblue',marker = '.', linestyle ='None' )

ax2.plot(t,res, color= 'royalblue', marker='.',linestyle ='None')
ax2.plot(X,Y, color= 'coral', linestyle='dashed')
ax2.set_xlim(min(t)-0.05, max(t)+0.05)
ax2.set_ylabel('residui', fontsize = 17, labelpad = 25)
ax2.set_xlabel('tempo[ms]', fontsize= 17, labelpad = 10)
ax1.grid(which = 'both', linestyle='dashed', color = 'gray')
ax2.grid(which = 'both', linestyle='dashed', color = 'gray')

plt.show()
print(popt*10)
print(incertezze*10)
##

#primo try
#t=np.array([2.580,2.572,2.572,2.599,2.596,2.576,2.577,2.556,2.553,2.573,2.549,2.579,2.597])
#T=np.array([21.88,23.12,23.93,19.05,17.56,18.01,18.84,20.21,21.50,21.20,21.23,21.56,22.45])

#
#secondo try
t=np.array([2.6084,2.6009,2.5913,2.5862,2.6083,2.6157,2.6401])
T=np.array([19.11,19.99,20.70,22.91,19.61,18.04,16.15])
x=0.445
X=np.array([min(T-5),max(T+5)])
Y=np.array([0,0])
x = 2*x
t= t*10**(-3)
V=(x/t)

sigma_V=np.full(len(V),2)
def f(T,c):
    v=c*( np.sqrt((T+273.15)/273.15))
    return v

popt, pcov = curve_fit(f,T,V,sigma=sigma_V)
incertezze = np.sqrt(pcov.diagonal())

res = (V - f(T,popt))/sigma_V
xx = np.linspace(min(T), max(T), 500)
yy = f(xx,popt)

fig = plt.figure('velocità da temperatura')
ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)

ax1.errorbar(xx,yy, color='coral')
ax1.set_ylabel('velocità[m/s]',fontsize= 17,labelpad = 25)
ax1.errorbar(T,V,yerr=2,xerr=0.4,color= 'royalblue',marker = '.', linestyle ='None' )
ax2.plot(T,res, color= 'royalblue', marker='.',linestyle ='None')
ax2.plot(X,Y, color= 'black', linestyle='none')
ax2.set_xlim(min(T)-0.05, max(T)+0.05)
ax2.set_ylabel('residui', fontsize = 17, labelpad = 25)
ax2.set_xlabel('temperatura[C°]', fontsize= 17, labelpad = 10)
ax1.grid(which = 'both', linestyle='dashed', color = 'gray')
ax2.grid(which = 'both', linestyle='dashed', color = 'gray')

plt.show()
print(popt)
print(incertezze)


