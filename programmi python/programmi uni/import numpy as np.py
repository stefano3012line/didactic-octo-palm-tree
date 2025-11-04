import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from matplotlib import colors

V_in = np.array([99.20,149.05,198.72,248.52,298.20,348.02,397.71])

sigma_vin = np.full(len(V_in),0.3)

V_out = np.array([0.8118,1.2172,1.6235,2.0300,2.4361,2.8446,3.2492])

V_out=V_out*1000
#sigma_vout = np.array([0.0001,0.0001,0.0001,0.0001,0.0001,0.01e-03,0.0001])
#sigma_vout = sigma_vout*1000

sigma_vout = np.full(5,0.3e-3)
sigma_vout = np.append(sigma_vout,np.full(2,3e-3))
sigma_vout = np.sqrt(sigma_vout**2+(8*sigma_vin)**2)
#sigma_vout = sigma_vout*1000
def guadagno(x, A_v):
    return x*A_v


p_guess = np.array([8])
p_opt, p_cov = curve_fit(guadagno,V_in,V_out,*p_guess, sigma = sigma_vout, absolute_sigma= True)
sigma = np.sqrt(p_cov.diagonal())

x = np.linspace(min(V_in),max(V_in),int(1e04))
#residui
res = (V_out - guadagno(V_in, p_opt))/sigma_vout
chi = np.sum(((V_out - guadagno(V_in, p_opt))**2)/sigma_vout)
dof = len(V_in)-len(p_guess)
fig = plt.figure("grafico del guadagno")
frame1 = fig.add_axes((0.1,0.37,0.8,0.6))
plt.grid(which='both',ls='dashed',color='lightslategrey')
plt.errorbar(V_in,V_out,sigma_vout,fmt='.',color = 'cornflowerblue')
plt.plot(x,guadagno(x,*p_opt),color = 'coral')
frame2 = fig.add_axes((0.1,0.07,0.8,0.2))
plt.grid(which='both',ls='dashed',color='lightslategrey')
plt.errorbar(V_in,res,fmt='.',color = 'cornflowerblue')
frame1.set_ylabel('V_out [mv]')
frame2.set_xlabel('V_in [mv]')
frame2.set_ylabel('residui normalizzati')
plt.show()

print(p_opt,sigma)
print (chi/dof)
