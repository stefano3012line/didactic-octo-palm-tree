#prima di imbattersi nel tentativo di devifrare questo codice si tiene a precisare che solo Dio e lo scrittore erano a conoscenza del pieno funzionamento di questo codice,adesso questa conoscenza appartiene solo a Dio



from scipy.sparse import random
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import math
import random
from scipy.stats import chisquare
##Pendolo singolo
print('___PENDOLO SINGOLO___')

t1 , theta1, t2, theta2 =np.loadtxt(r"C:\Users\Dell\Desktop\Uni_lab\Dati oscillazioni accoppiate\PENDOLOSINGOLO.txt", unpack=True)
cunt=len(theta2)

omega2=4.5
phi2=5
A2=100
off=430
gamma2=0.005
p0=[omega2,phi2,gamma2,A2]
def sin(omega2,phi2, t2):
  return np.sin(omega2*t2+phi2)

#utili per il guess iniziale
'''
plt.figure('Pendolo s')
plt.plot(t2,theta2)
plt.plot(t2,A2*sin(omega2,phi2,t2)+off)
plt.show()'''

ofs=np.mean(theta2)
sigma_theta2=3

def om(t , omega , phi0 , gamma ,A ):
  return A*np.exp(-gamma*t)*np.sin(phi0+omega*t)

popt,pcov= curve_fit(om, t2, theta2,p0=p0,absolute_sigma=True,sigma=np.full(len(theta2),sigma_theta2))
omega1,phi1,gamma1,A1=popt
#print(popt)

fig=plt.figure('Pendolo singolo')
fig.add_axes((0.1, 0.37, 0.8, 0.6))

t2=t2[200:400]
theta2=theta2[200:400]


x=np.linspace(10,20.3,10000)
plt.plot(x, om(x,omega1, phi1,gamma1,A1))
plt.grid(which='both',ls='dashed',color='gray')
plt.errorbar(t2[::],theta2[::]-ofs,sigma_theta2,fmt='.')
plt.plot(t2[::],theta2[::]-ofs,'.')

fig.add_axes((0.1, 0.1, 0.8, 0.2))
res = (theta2 - om(t2,omega1, phi1,gamma1,A1)-ofs)/sigma_theta2
plt.errorbar(t2[::], res[::], sigma_theta2,fmt=".")
plt.grid(which='both', ls='dashed', color='gray')
plt.xlabel('tempo')
plt.ylabel('posizione')
plt.ylim(-20.0, 20.0)

plt.savefig('Pendolo singolo.pdf')
plt.show()
print("omega1=",omega1)
print("phi1=",phi1)
print("gamma1=",gamma1)
print("A1=",A1)
print("tau=",1/gamma1)
chiq=np.sum((((theta2-om(t2,omega1, phi1,gamma1,A1)-ofs)**2)/sigma_theta2**2))
print("chi^2=",chiq/(cunt-5),'sigma_chi^2=',np.sqrt(2/(cunt-5)))
##Pendolo smorzato
print('___PENDOLO SMORZATO___')
#loading
t1 , theta1, t2, theta2 =np.loadtxt(r"C:\Users\Dell\Desktop\Uni_lab\Dati oscillazioni accoppiate\PENDOLOSMORZATO.txt", unpack=True)
cunt=len(theta1)
#plot del guess
omega1=4
phi1=5
A1=120
off=np.mean(theta1)
gamma1=1
p0=[omega1,phi1,gamma1,A1]
def sin(omega1,phi1, t1):
  return np.sin(omega1*t1+phi1)
#utili per il guess iniziale
'''plt.figure('Pendolo s')
plt.plot(t1,theta1,"b")
plt.plot(t1,A1*sin(omega1,phi1,t1)+off,"r")'''

#plot dell'pendolo


ofs=np.mean(theta1)
sigma_theta1=3

def om(t , omega , phi0 , gamma ,A ):
  return A*np.exp(-gamma*t)*np.sin(phi0+omega*t)

popt,pcov= curve_fit(om, t1, theta1,p0=p0,absolute_sigma=True,sigma=np.full(len(theta1),sigma_theta1))
omega1,phi1,gamma1,A1=popt


fig=plt.figure('Pendolo smorzato')
fig.add_axes((0.1, 0.37, 0.8, 0.6))

t1=t1[200:]
theta1=theta1[200:]


x=np.linspace(10,41,10000)
plt.plot(x, om(x,omega1, phi1,gamma1,A1),color="r")
plt.grid(which='both',ls='dashed',color='gray')
plt.errorbar(t1[::],theta1[::]-ofs,sigma_theta1,fmt='.')
plt.plot(t1[::],theta1[::]-ofs,'.')


fig.add_axes((0.1, 0.1, 0.8, 0.2))
res = (theta1 - om(t1,omega1, phi1,gamma1,A1)-ofs)/sigma_theta1
plt.errorbar(t1[::3], res[::3], sigma_theta1,fmt=".")
plt.grid(which='both', ls='dashed', color='gray')
plt.xlabel('tempo')
plt.ylabel('posizione')
plt.ylim(-20.0, 20.0)


plt.savefig('Pendolo smorzato.pdf')
plt.show()
print("omega1=",omega1)
print("phi1=",phi1)
print("gamma1=",gamma1)
print("A1=",A1)
print("tau=",1/gamma1)
chiq=np.sum((((theta1-om(t1,omega1, phi1,gamma1,A1)-ofs)**2)/sigma_theta1**2))
print("chi^2=",chiq/(cunt-5),'sigma_chi^2=',np.sqrt(2/(cunt-5)))
##Pendolo contro fase (1)
print('___PENDOLO CONTRO FASE 1___')
t1,theta1,t2,theta2=np.loadtxt(r"C:\Users\Dell\Desktop\Uni_lab\Dati oscillazioni accoppiate\PENDOLOCONTRO.txt", unpack=True)
cunt=len(theta1)
sigma_theta1=3
off=np.mean(theta1)

p0=[180,100,0.03,0.04,5,6,5,5.5]


def om(t,A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2):
    return A1*np.exp(-gamma1*t)*np.sin(omega1*t+phi1)+A2*np.exp(-gamma2*t)*np.sin(omega2*t+phi2)

#plot principale
popt,pcov=curve_fit(om,t1,theta1,p0=p0,absolute_sigma=True,sigma=np.full(len(theta1),sigma_theta1))
A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2=popt

fig=plt.figure('Pendolo contro1')

x=np.linspace(0,41,10000)
fig.add_axes((0.1, 0.37, 0.8, 0.6))
plt.errorbar(t1[5::1],theta1[5::1]-off,sigma_theta1,fmt='.')
plt.plot(x, om(x,A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2)-off)
plt.plot(t1[5::5],theta1[5::5] -off,'.')
plt.grid(which='both',ls='dashed',color='gray')



#grafico residui

fig.add_axes((0.1, 0.1, 0.8, 0.2))
res = (theta1 -  om(t1,A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2))/sigma_theta1
plt.errorbar(t1[5::5], res[5::5], sigma_theta1,fmt=".")
plt.grid(which='both', ls='dashed', color='gray')
plt.xlabel('tempo')
plt.ylabel('posizione')
plt.ylim(-10.0, 10.0)

#stima errori
chiq=np.sum((((theta1-om(t1,A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2))**2)/sigma_theta1**2))
print("omega1=",omega1)
print("phi1=",phi1)
print("gamma1=",gamma1)
print("A1=",A1)
print("tau=",1/gamma1)
print("chi^2=",chiq/(cunt-5),'sigma_chi^2=',np.sqrt(2/(cunt-5)))

plt.savefig('Pendolo cf1.pdf')
plt.show()
##Pendolo contro fase (2)
print('___PENDOLO CONTRO FASE 2___')
t1,theta1,t2,theta2=np.loadtxt(r"C:\Users\Dell\Desktop\Uni_lab\Dati oscillazioni accoppiate\PENDOLOCONTRO.txt", unpack=True)
cunt=len(theta1)
off=np.mean(theta2)

p0=[180,180,0.01,0.04,5,-5,5,-5]

sigma_theta1=3

def om(t,A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2):
    return A1*np.exp(-gamma1*t)*np.sin(omega1*t+phi1)+A2*np.exp(-gamma2*t)*np.sin(omega2*t+phi2)

#plot principale
popt,pcov=curve_fit(om,t2,theta2,p0=p0,absolute_sigma=True,sigma=np.full(len(theta1),sigma_theta1))
A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2=popt

fig=plt.figure('Pendolo contro2')

x=np.linspace(0,20.2,10000)
fig.add_axes((0.1, 0.37, 0.8, 0.6))
plt.errorbar(t2[:400:],theta2[:400:]-off,sigma_theta1,fmt='.')
plt.plot(x, om(x,A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2)-off)
plt.plot(t2[10:400:],theta2[10:400:]-off,'.')
plt.grid(which='both',ls='dashed',color='gray')

#grafico residui
fig.add_axes((0.1, 0.1, 0.8, 0.2))
res = (theta2 -  om(t2,A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2))/sigma_theta1
plt.errorbar(t2[10:400:], res[10:400:], sigma_theta1,fmt=".")
plt.grid(which='both', ls='dashed', color='gray')
plt.xlabel('tempo')
plt.ylabel('posizione')
plt.ylim(-10.0, 10.0)

#stima errori
chiq=np.sum((((theta2-om(t2,A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2))**2)/sigma_theta1**2))

print("omega2=",omega1)
print("phi2=",phi1)
print("gamma2=",gamma1)
print("A2=",A1)
print("tau=",1/gamma1)
print("chi^2=",chiq/(cunt-5),'sigma_chi^2=',np.sqrt(2/(cunt-5)))

plt.savefig('Pendolo cf2.pdf')
plt.show()
##Pendolo fase(1)
print('___PENDOLO FASE 1___')

t1,theta1,t2,theta2=np.loadtxt(r"C:\Users\Dell\Desktop\Uni_lab\Dati oscillazioni accoppiate\PENDOLOFASE.txt",unpack=True)


sigma_theta1=3
cunt=len(theta1)
off=np.mean(theta1)

p0=[150,150,0.02,0.01,7,5,4,5]


def om(t,A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2):
    return A1*np.exp(-gamma1*t)*np.sin(omega1*t+phi1)+A2*np.exp(-gamma2*t)*np.sin(omega2*t+phi2)
#plot principale

popt,pcov=curve_fit(om,t1[50::],theta1[50::],p0=p0,absolute_sigma=True,sigma=np.full(len(theta1),sigma_theta1)[50::], maxfev=10000)
A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2=popt

fig=plt.figure('Pendolo fase1')

x=np.linspace(5,15.5,10000)
fig.add_axes((0.1, 0.37, 0.8, 0.6))


plt.plot(x, om(x,A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2)-off)
plt.plot(t1[100:300:3],theta1[100:300:3]-off,'.')
plt.errorbar(t1[100:300:3],theta1[100:300:3]-off,sigma_theta1,fmt='.')
plt.grid(which='both',ls='dashed',color='gray')


#grafico residui

fig.add_axes((0.1, 0.1, 0.8, 0.2))
res = (theta1 -  om(t2,A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2))
plt.errorbar(t1[100:300:3], res[100:300:3], yerr=sigma_theta1,fmt=".")
plt.grid(which='both', ls='dashed', color='gray')
plt.xlabel('tempo')
plt.ylabel('posizione')
plt.ylim(-30.0, 30.0)


#stima errori
chiq=np.sum((((theta1-om(t1,A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2))**2)/sigma_theta1**2))
print("omega1=",omega1)
print("phi1=",phi1)
print("gamma1=",gamma1)
print("A1=",A1)
print("tau=",1/gamma1)
print("chi^2=",chiq/(cunt-4),'sigma_chi^2=',np.sqrt(2/(cunt-4)))


plt.savefig('Pendolo f1.pdf')
plt.show()

##Pendolo fase(1)
print('___PENDOLO FASE 2___')

t1,theta1,t2,theta2=np.loadtxt(r"C:\Users\Dell\Desktop\Uni_lab\Dati oscillazioni accoppiate\PENDOLOFASE.txt",unpack=True)

cunt=len(theta2)
sigma_theta1=3
off=np.mean(theta2)

p0=[150,140,0.01,0.02,5,7,5,4]


def om(t,A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2):
    return A1*np.exp(-gamma1*t)*np.sin(omega1*t+phi1)+A2*np.exp(-gamma2*t)*np.sin(omega2*t+phi2)

#plot principale
popt,pcov=curve_fit(om,t2,theta2,p0=p0,absolute_sigma=True)
A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2=popt


'''
print("A=",A1," ",A2)
print("gamma=",gamma1," ",gamma2)
print("phi=",phi1," ",phi2)
print("omega=",omega1," ",omega2)
'''




fig=plt.figure('Pendolo fase2')


x=np.linspace(5,15.5,10000)
fig.add_axes((0.1, 0.37, 0.8, 0.6))

plt.plot(x, om(x,A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2)-off)
plt.errorbar(t2[100:300:3],theta2[100:300:3]-off,sigma_theta1,fmt='.')
plt.plot(t2[100:300:3],theta2[100:300:3]-off,'.')
plt.grid(which='both',ls='dashed',color='gray')

#grafico residui

fig.add_axes((0.1, 0.1, 0.8, 0.2))
res = (theta2 -  om(t2,A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2))
plt.errorbar(t2[100:300:3], res[100:300:3], sigma_theta1,fmt=".")
plt.grid(which='both', ls='dashed', color='gray')
plt.xlabel('tempo')
plt.ylabel('posizione')
plt.ylim(-20.0, 20.0)


#stima errori


chiq=np.sum((((theta2-om(t1,A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2))**2)/sigma_theta1**2))
print("omega2=",omega1)
print("phi2=",phi1)
print("gamma2=",gamma1)
print("A2=",A1)
print("tau=",1/gamma1)
print("chi^2=",chiq/(cunt-4),'sigma_chi^2=',np.sqrt(2/(cunt-4)))



plt.savefig('Pendolo f2.pdf')

plt.show()
##Battimenti(1)
print('___BATTIMENTI 1___')

t1,theta1,t2,theta2=np.loadtxt(r"C:\Users\Dell\Desktop\Uni_lab\Dati oscillazioni accoppiate\BATTIMENTI.txt", unpack=True)
cunt=len(theta1)
#stima dei dati
p0=[140,140,0.01,0.02,7,7,4,5]
sigma_theta1=3
off=np.mean(theta1)
def om(t,A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2):
    return A1*np.exp(-gamma1*t)*np.sin(omega1*t+phi1)+A2*np.exp(-gamma2*t)*np.sin(omega2*t+phi2)


popt,pcov=curve_fit(om,t1,theta1,p0=p0,absolute_sigma=True,sigma=np.full(cunt,sigma_theta1))
A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2=popt


#plot principale
fig=plt.figure('Battimenti1')
fig.add_axes((0.1, 0.37, 0.8, 0.6))
x=np.linspace(0,max(t1),10000)
plt.plot(x, om(x,A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2),"g")
plt.plot(t1[::5],theta1[::5]-off,'.')
plt.errorbar(t1[::5],theta1[::5]-off,sigma_theta1,fmt='.')
plt.grid(which='both',ls='dashed',color='gray')

#stima degi errori
chiq=np.sum((((theta1-om(t1,A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2)-off)**2)/(sigma_theta1)**2))

print("omega1=",omega1)
print("phi1=",phi1)
print("gamma1=",gamma1)
print("A1=",A1)
print("tau=",1/gamma1)
print("chi^2=",chiq/(cunt-8),'sigma_chi^2=',np.sqrt(2/(cunt-8)))

fig.add_axes((0.1, 0.1, 0.8, 0.2))
res = (theta1 - om(t1,A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2)-off)
plt.errorbar(t1[::5], res[::5], sigma_theta1,fmt=".")
plt.grid(which='both', ls='dashed', color='gray')
plt.xlabel('tempo')
plt.ylabel('posizione')
plt.ylim(-20.0, 20.0)

plt.savefig('Pendolo B1.pdf')
plt.show()

##Battimenti(2)
print('___BATTIMENTI 2___')


t1,theta1,t2,theta2=np.loadtxt(r"C:\Users\Dell\Desktop\Uni_lab\Dati oscillazioni accoppiate\BATTIMENTI.txt", unpack=True)
cunt=len(theta1)
#plot principale


p0=[140,140,0.01,0.02,7,-7,5,5]

off=np.mean(theta2)
def om(t,A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2):
    return A1*np.exp(-gamma1*t)*np.sin(omega1*t+phi1)+A2*np.exp(-gamma2*t)*np.sin(omega2*t+phi2)
c=0
sigma_theta1=3

while c<=10:
  popt,pcov=curve_fit(om,t2,theta2,p0=p0,absolute_sigma=True,sigma=np.full(cunt,sigma_theta1),maxfev=50000)

  A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2=popt
  p0=[A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2]
  c+=1



fig=plt.figure('Battimenti2')
x=np.linspace(0,43,10000)
fig.add_axes((0.1, 0.37, 0.8, 0.6))
plt.plot(x, om(x,A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2))
plt.errorbar(t2[::5],theta2[::5]-off,sigma_theta1,fmt='.')
#plt.plot(t2[::15],theta2[::15]-off,'.')
plt.grid(which='both',ls='dashed',color='gray')

#stima errori

chiq=np.sum((((theta2-om(t1,A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2)-off)**2)/sigma_theta1**2))

print("omega1=",omega1)
print("phi1=",phi1)
print("gamma1=",gamma1)
print("A1=",A1)
print("tau=",1/gamma1)
print("chi^2=",chiq/(cunt-8),'sigma_chi^2=',np.sqrt(2/(cunt-8)))

#plot residui
fig.add_axes((0.1, 0.1, 0.8, 0.2))
res = (theta2 - om(t2,A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2)-off)
plt.errorbar(t2[::15], res[::15], sigma_theta1,fmt=".")
plt.grid(which='both', ls='dashed', color='gray')
plt.xlabel('tempo')
plt.ylabel('posizione')
plt.ylim(-20.0, 20.0)


plt.savefig('Pendolo B2.pdf')
plt.show()
