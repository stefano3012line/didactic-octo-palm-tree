import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.optimize import least_squares

### ANDREA GAY, AVETE PERSO AL GIOCO
### ATTENZIONE!!! PER QUALCHE MOTIVO CHE NON SO, SE PASSO GLI ERRORI AI FIT DELLE 4 CURVE NON MI CONVERGONO PIÙ
### NON ESCLUDO POSSA ESSERCI UN ERRORE NEL CODICE.

#import dati corrente oscura
_, V_o,_ ,I_o = np.genfromtxt(fname ='/home/francesco/Scrivania/Corrente oscura giusta forse.txt', usecols=(0,1,2,3), skip_header=2,skip_footer=0, unpack=True)

# import dati della al variare della lunghezza d'onda se non seguite il mio ordine si sminchia tutto quindi fatelo
_, V_1,_ ,I_1 = np.genfromtxt(fname ='/home/francesco/Scrivania/577nm.txt', usecols=(0,1,2,3), skip_header=2,skip_footer=0, unpack=True ) #577nm
_, V_2 ,_ ,I_2 = np.genfromtxt(fname ='/home/francesco/Scrivania/546nm.txt', usecols=(0,1,2,3), skip_header=2,skip_footer=0, unpack=True ) #546nm
_, V_3,_ ,I_3 = np.genfromtxt(fname ='/home/francesco/Scrivania/450nm.txt', usecols=(0,1,2,3), skip_header=2,skip_footer=0, unpack=True ) #450nm
_, V_4,_,I_4 = np.genfromtxt(fname ='/home/francesco/Scrivania/499nm.txt', usecols=(0,1,2,3), skip_header=2,skip_footer=0, unpack=True ) #499nm

#valori dei guess, non chiedetemi come li so (sono i risultati dei miei fit)
p_guess1 = np.array([0.63743414, 1.44883801, 1.85908893])
p_guess2 = np.array([0.71104553, 0.95795131, 1.65549093])
p_guess3 = np.array([1.16684689, 0.57435911, 1.89669453])
p_guess4 = np.array([0.924205,   0.97379914, 1.79611145])

# calcolo degli errori (fatto da Sara chiedete a lei, mai fidarsi di un gay)
sigma_Io = I_o*np.sqrt((3e-4)**2 + (4e-3)**2)
sigma_I1 = I_1*np.sqrt((3e-4)**2 + (4e-3)**2)
sigma_I2 = I_2*np.sqrt((3e-4)**2 + (4e-3)**2)
sigma_I3 = I_3*np.sqrt((3e-4)**2 + (4e-3)**2)
sigma_I4 = I_4*np.sqrt((3e-4)**2 + (4e-3)**2)

#funzione corrente oscura
def F(V,b,I_0):
	y = b*V + I_0
	return y
# fitting corrente oscura
popt,pcov = curve_fit(F,V_o,I_o, sigma=sigma_Io)
err = np.sqrt(pcov.diagonal())
res = (I_o - F(V_o,*popt))/sigma_Io

#print risultati fit onda oscura ì
print(f'onda oscura: I_0 = {popt[0]} +- {err[0]}, b = {popt[1]}+-{err[1]}')

# funzione da fittare, quella con la theta
def fot(V,V_0,a,alpha):
	I = np.where(V_0 - V  >0 ,a*(np.abs((V_0-V))**alpha) + popt[0]*V + popt[1], popt[0]*V + popt[1] )
	return I

# fitting e residui dei dati delle quattro curve
popt_1 , pcov_1 = curve_fit(fot,V_1,I_1,p0=p_guess1)
err_1 = np.sqrt(pcov_1.diagonal())
res_1 = (I_1 - fot(V_1,*popt_1))/sigma_I1

popt_2 , pcov_2 = curve_fit(fot,V_2,I_2,p0=p_guess2)
err_2 = np.sqrt(pcov_2.diagonal())
res_2 = (I_2 - fot(V_2,*popt_2))/sigma_I2

popt_3 , pcov_3 = curve_fit(fot,V_3,I_3,p0=p_guess3)
err_3 = np.sqrt(pcov_3.diagonal())
res_3 = (I_3 - fot(V_3,*popt_3))/sigma_I3

popt_4 , pcov_4 = curve_fit(fot,V_4,I_4,p0=p_guess4)
err_4 = np.sqrt(pcov_4.diagonal())
res_4 = (I_4 - fot(V_4,*popt_4))/sigma_I4

# bello sto chi quadro normalizzato di 7000
R = np.concatenate([res_1**2,res_2**2,res_3**2, res_4**2])
chi2 = np.sum(R)/(len(V_1)+ len(V_2)+ len(V_3) + len(V_4))


#printing dei dati delle 4 curve, # se non importate le cose con le stesse lunghezze donda mie cambiatele se no sminchiate
print(f'577nm, V_0 = {popt_1[0]}+-{err_1[0]}, a = {popt_1[1]}+-{err_1[1]}, alpha = {popt_1[2]}+-{err_1[2]}')
print(f'546nm, V_0 = {popt_2[0]}+-{err_2[0]}, a = {popt_2[1]}+-{err_2[1]}, alpha = {popt_2[2]}+-{err_2[2]}')
print(f'450nm, V_0 = {popt_3[0]}+-{err_3[0]}, a = {popt_3[1]}+-{err_3[1]}, alpha = {popt_3[2]}+-{err_3[2]}')
print(f'599nm, V_0 = {popt_4[0]}+-{err_4[0]}, a = {popt_4[1]}+-{err_4[1]}, alpha = {popt_4[2]}+-{err_4[2]}')
print(f'chi2 = {chi2}')

X = np.linspace(0,2,500)   #linspace 4 fit (non l'ho automatizzato dovete aggiustarlo a mano)
XX= np.linspace(min(V_o) , max(V_o)) #linspace corente oscura
#plot della corrente oscura
fig_1 = plt.figure('fit corrente oscura')
ax1 = fig_1.add_subplot(2,1,1)
ax2 = fig_1.add_subplot(2,1,2)
ax1.plot(V_o,I_o, marker='.', linestyle='none', color='coral')
ax1.plot(XX, F(XX,*popt), color='royalblue')
ax1.grid(linestyle = '--')
ax1.set_ylabel('I [nA]', fontsize=15)
#residui
ax2.errorbar(V_o,res, fmt='.', color='coral')
ax2.set_ylabel('residui normalizzati', fontsize=15)
ax2.set_xlabel('V [V]', fontsize=15)
ax2.grid(linestyle = '--')

#plot dei 4 fit
fig_2 = plt.figure('fit indipendenti')
ax1 = fig_2.add_subplot(2,1,1)
ax2 = fig_2.add_subplot(2,1,2)
ax1.errorbar(V_1[::35], I_1[::35], fmt='.', color='coral', label='577nm')
ax1.errorbar(V_2[::35], I_2[::35], fmt='.', color='mediumseagreen',label='546nm')  # sto plottando un punto ogni 35
ax1.errorbar(V_3[::35], I_3[::35], fmt='.', color='mediumorchid', label='450nm')
ax1.errorbar(V_4[::35], I_4[::35], fmt='.', color='royalblue',label='499nm')
ax1.plot(X,fot(X,*popt_1),color='coral')
ax1.plot(X,fot(X,*popt_2),color='mediumseagreen')
ax1.plot(X,fot(X,*popt_3),color='mediumorchid')
ax1.plot(X,fot(X,*popt_4),color='royalblue')
ax1.grid(which='both', color='gray', linestyle='--')
ax1.set_ylabel('I [nA]', fontsize=15)
ax1.legend(fontsize ='13')
#residui
ax2.errorbar(V_1[::35], res_1[::35], fmt='.', color='coral')
ax2.errorbar(V_2[::35], res_2[::35], fmt='.', color='mediumseagreen')
ax2.errorbar(V_3[::35], res_3[::35], fmt='.', color='mediumorchid')
ax2.errorbar(V_4[::35], res_4[::35], fmt='.', color='royalblue')
ax2.grid(which='both', color='gray', linestyle='--')
ax2.set_ylabel('residui normalizzati', fontsize=15)
ax2.set_xlabel('V [V]', fontsize=15)
plt.show()

# dati per il fit di h/e
c = 3e17  # c in nm/s
V0 = np.array([popt_1[0],popt_2[0],popt_3[0], popt_4[0]])
sigma_V0 = np.array([err_1[0], err_2[0], err_3[0], err_4[0]])
nu = np.array([c/577, c/546, c/450, c/499])

#funzione per il fit di h/e
def line(x,a,b):
	y = a*x + b
	return y
#fitting
popt_d,pcov_d = curve_fit(line,nu, V0, sigma=sigma_V0)
err_d = np.sqrt(pcov_d.diagonal())
res_d = (V0 - line(nu,*popt_d))/sigma_V0

#print dei dati
print(f'h/e = {popt_d[0]} +- {err_d[0]}')
print(f'W_0/e = {popt_d[1]} +- {err_d[1]}')
#plot dei dati
XXX= np.linspace(min(nu)- 0.5, max(nu) + 0.5)
fig_3 = plt.figure('fit di h/e')
ax1 = fig_3.add_subplot(2,1,1)
ax2 = fig_3.add_subplot(2,1,2)
ax1.errorbar(nu,V0,fmt='.', yerr= sigma_V0, color='royalblue')
ax1.plot(XXX, line(XXX,*popt_d), color='coral')
ax1.grid(which='both', color='gray', linestyle='--')
ax1.set_ylabel('V_0[V]', fontsize=15)
ax2.errorbar(nu,res_d, fmt='.', color='royalblue')
ax2.grid(which='both', color='gray', linestyle='--')
ax2.set_ylabel('residui normalizzati', fontsize=15)
ax2.set_xlabel('nu [Hz]', fontsize='15')
plt.show()

#print(popt_1, popt_2, popt_3, popt_4)






