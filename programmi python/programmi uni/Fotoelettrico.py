import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.optimize import least_squares



#import dati corrente oscura
_, V_o,_ ,I_o = np.genfromtxt(fname ="C:/Users/Dell/Desktop/fotoelettrico e7/correnteoscura_copertina.txt", usecols=(0,1,2,3), skip_header=2,skip_footer=0, unpack=True)

# import dati della al variare della lunghezza d'onda se non seguite il mio ordine si sminchia tutto quindi fatelo
_, V_1,_ ,I_1 = np.genfromtxt(fname ="C:/Users/Dell/Desktop/fotoelettrico e7/577giallo_copertina_2.txt", usecols=(0,1,2,3), skip_header=2,skip_footer=0, unpack=True ) #577nm
_, V_2 ,_ ,I_2 = np.genfromtxt(fname ="C:/Users/Dell/Desktop/fotoelettrico e7/546verde_copertina.txt", usecols=(0,1,2,3), skip_header=2,skip_footer=0, unpack=True ) #546nm
_, V_3,_ ,I_3 = np.genfromtxt(fname ="C:/Users/Dell/Desktop/fotoelettrico e7/450blu_copertina.txt", usecols=(0,1,2,3), skip_header=2,skip_footer=0, unpack=True ) #450nm
_, V_4,_,I_4 = np.genfromtxt(fname ="C:/Users/Dell/Desktop/fotoelettrico e7/499verde_copertina.txt", usecols=(0,1,2,3), skip_header=2,skip_footer=0, unpack=True ) #499nm


plt.ylabel('$I$ [nA]')
plt.xlabel('$V_{bias}$ [V]')
plt.plot(V_o[::50],I_o[::50], marker='.',linestyle ='None', color = 'black')

plt.plot(V_1[::50],I_1[::50], marker='.',linestyle ='None', color = 'orange')

plt.plot(V_2[::50],I_2[::50], marker='.',linestyle ='None', color = 'green')

plt.plot(V_4[::50],I_4[::50], marker='.',linestyle ='None', color = 'olive')

plt.plot(V_3[::50],I_3[::50], marker='.',linestyle ='None', color = 'blue')

plt.legend(['Corrente oscura', 'Filtro 577nm','Filtro 546nm', 'Filtro 499nm', 'Filtro 450nm'])

plt.show()
# calcolo degli errori (fatto da Sara chiedete a lei, mai fidarsi di un gay)
sigma_Io = np.sqrt((3e-4)**2 + (I_o*4e-3)**2)
sigma_I1 = np.sqrt((3e-4)**2 + (I_o*4e-3)**2)
sigma_I2 = np.sqrt((3e-4)**2 + (I_o*4e-3)**2)
sigma_I3 = np.sqrt((3e-4)**2 + (I_o*4e-3)**2)
sigma_I4 = np.sqrt((3e-4)**2 + (I_o*4e-3)**2)
##
#funzione corrente oscura

def F(V,b,I_o):
    y = b*V + I_o
    return y


# fitting corrente oscura
popt,pcov = curve_fit(F,V_o,I_o, sigma=sigma_Io)
err = np.sqrt(pcov.diagonal())
res = (I_o - F(V_o,*popt))/sigma_Io



#print risultati fit onda oscura
print(f'corrente oscura: I_0 = {popt[0]} +- {err[0]}, b = {popt[1]} +- {err[1]}')

I_0 = popt[0]
b = popt[1]

def fot(V,V_0,a):
    I= np.where(V_0 - V>0,a*np.abs(V_0-V)**(2.5) +b*V + I_0, b*V + I_0)
    return I





#selezione punti interessanti
S_1=1200
F_1=5300

S_2=1350
F_2=6000

S_3=1400
F_3=6000

S_4=1800
F_4=6000



# fitting e residui dei dati delle quattro curve
popt_1 , pcov_1 = curve_fit(fot,V_1[S_1:F_1:],I_1[S_1:F_1:],sigma=sigma_I1[S_1:F_1:])
err_1 = np.sqrt(pcov_1.diagonal())
res_1 = (I_1 - fot(V_1,*popt_1))/sigma_I1

popt_2 , pcov_2 = curve_fit(fot,V_2[S_2:F_2:],I_2[S_2:F_2:],sigma=sigma_I2[S_2:F_2:])
err_2 = np.sqrt(pcov_2.diagonal())
res_2 = (I_2 - fot(V_2,*popt_2))/sigma_I2

popt_4 , pcov_4 = curve_fit(fot,V_4[S_4:F_4:],I_4[S_4:F_4:],sigma=sigma_I4[S_4:F_4:])
err_4 = np.sqrt(pcov_4.diagonal())
res_4 = (I_4 - fot(V_4,*popt_4))/sigma_I4

popt_3 , pcov_3 = curve_fit(fot,V_3[S_3:F_3:],I_3[S_3:F_3:],sigma=sigma_I3[S_3:F_3:])
err_3 = np.sqrt(pcov_3.diagonal())
res_3 = (I_3 - fot(V_3,*popt_3))/sigma_I3

print(f'V_0 a 577nm: V_0 = {popt_1[0]} +- {err_1[0]}, a = {popt_1[1]} +- {err_1[1]}')
print(f'V_0 a 546nm: V_0 = {popt_2[0]} +- {err_2[0]}, a = {popt_2[1]} +- {err_2[1]}')
print(f'V_0 a 450nm: V_0 = {popt_3[0]} +- {err_3[0]}, a = {popt_3[1]} +- {err_3[1]}')
print(f'V_0 a 499nm: V_0 = {popt_4[0]} +- {err_4[0]}, a = {popt_4[1]} +- {err_4[1]}')



#plot dei 4 fit
X1 = np.linspace(min(V_1),max(V_1),1000)
X2 = np.linspace(min(V_2),max(V_2),1000)
X3 = np.linspace(min(V_3),max(V_3),1000)
X4 = np.linspace(min(V_4),max(V_4),1000)


plt.ylabel('$I$ [nA]')
plt.xlabel('$V_{bias}$ [V]')



plt.plot(X1,fot(X1,*popt_1),color='orange')
plt.plot(X2,fot(X2,*popt_2),color='green')
plt.plot(X3,fot(X3,*popt_3),color='blue')
plt.plot(X4,fot(X4,*popt_4),color='olive')


plt.plot(V_1[::50],I_1[::50], marker='.',linestyle ='None', color = 'orange')

plt.plot(V_2[::50],I_2[::50], marker='.',linestyle ='None', color = 'green')

plt.plot(V_4[::50],I_4[::50], marker='.',linestyle ='None', color = 'olive')

plt.plot(V_3[::50],I_3[::50], marker='.',linestyle ='None', color = 'blue')


#fra rompe il cazzo
'''plt.plot(V_1[S_1:F_1:],I_1[S_1:F_1:],color = 'black')

plt.plot(V_2[S_2:F_2:],I_2[S_2:F_2:],color = 'black')

plt.plot(V_3[S_3:F_3:],I_3[S_3:F_3:],color = 'black')

plt.plot(V_4[S_4:F_4:],I_4[S_4:F_4:],color = 'black')
'''
plt.legend([ 'Filtro 577nm','Filtro 546nm', 'Filtro 450nm','Filtro 499nm' ])

plt.show()

## grafico delle frequenze

# dati per il fit di h/e
c = 3e17  # c in nm/s
nu=np.array([c/450,c/499,c/546,c/577])
V0=np.array([popt_3[0],popt_4[0],popt_2[0],popt_1[0]])
sigma_V0 = np.array([err_3[0], err_4[0], err_2[0], err_1[0]])



def f(nu,a,b):
    V = a*nu + b
    return V


popt_d,pcov_d = curve_fit(f,nu, V0, sigma=sigma_V0)
err_d = np.sqrt(pcov_d.diagonal())
res_d = (V0 - f(nu,*popt_d))/sigma_V0



#print dei dati
print(f'h/e = {popt_d[0]} +- {err_d[0]}')
print(f'W_0/e = {popt_d[1]} +- {err_d[1]}')
#plot dei dati
XXX= np.linspace(min(nu)- 0.5, max(nu) + 0.5)
fig_3 = plt.figure('fit di h/e')
ax1 = fig_3.add_subplot(2,1,1)
ax2 = fig_3.add_subplot(2,1,2)
ax1.errorbar(nu,V0,fmt='.', yerr= sigma_V0, color='royalblue')
ax1.plot(XXX, f(XXX,*popt_d), color='coral')
ax1.grid(which='both', color='gray', linestyle='--')
ax1.set_ylabel('V_0[V]', fontsize=15)
ax2.errorbar(nu,res_d, fmt='.', color='royalblue')
ax2.grid(which='both', color='gray', linestyle='--')
ax2.set_ylabel('residui normalizzati', fontsize=15)
ax2.set_xlabel('nu [Hz]', fontsize='15')
plt.show()







