import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
##MATERIALE1
# Misure dirette delle distanze e delle temperature (mettete i vostri numeri).
# Qui potete anche leggere i dati da file, usando il metodo np.loadtxt(),
# se lo trovate comodo.
x = np.array([5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0])
sigma_x = np.full(x.shape, 0.1)
T = np.array([28.6, 27.8, 26.9, 25.9, 25.0, 24.0, 23.1])
sigma_T = np.full(T.shape, 0.2)

def line(x, m, q):
    """Modello di fit lineare."""
    return m * x + q

fig=plt.figure("Grafico posizione-temperatura-materiale1")
fig.add_axes((0.1, 0.37, 0.8, 0.6))
# Grafico dei punti sperimentali.
plt.errorbar(x, T, sigma_T, sigma_x, fmt=".")
# Fit con una retta.
popt, pcov = curve_fit(line, x, T, sigma=sigma_T)
m_hat, q_hat = popt
sigma_m, sigma_q = np.sqrt(pcov.diagonal())
print(m_hat, sigma_m, q_hat, sigma_q)
# Grafico del modello di best fit.
c = np.linspace(0., 40., 100)
plt.plot(c, line(c, m_hat, q_hat))
# Formattazione del grafico.
plt.xlabel("Posizione [cm]")
plt.ylabel("Temperatura [$^\\circ$C]")
plt.grid(which="both", ls="dashed", color="gray")


# A questo punto potete usare i risultati del fit per stimare la
# conducibilita‘ vera e propria...

#grafico dei residui
fig.add_axes((0.1, 0.07, 0.8, 0.2))
plt.grid(which='both', ls='dashed', color='gray')
plt.errorbar(x,T-line(x, m_hat, q_hat),yerr=0.2,fmt='.')
plt.savefig("posizione_temperatura_materiale1.pdf")
plt.show()


##MATERIALE2
# Misure dirette delle distanze e delle temperature (mettete i vostri numeri).
# Qui potete anche leggere i dati da file, usando il metodo np.loadtxt(),
# se lo trovate comodo.
x = np.array([5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0])
sigma_x = np.full(x.shape, 0.1)
T = np.array([28.6, 27.8, 26.9, 25.9, 25.0, 24.0, 23.1])
sigma_T = np.full(T.shape, 0.2)

def line(x, m, q):
    """Modello di fit lineare."""
    return m * x + q

fig=plt.figure("Grafico posizione-temperatura-materiale2")
fig.add_axes((0.1, 0.37, 0.8, 0.6))
# Grafico dei punti sperimentali.
plt.errorbar(x, T, sigma_T, sigma_x, fmt=".")
# Fit con una retta.
popt, pcov = curve_fit(line, x, T, sigma=sigma_T)
m_hat, q_hat = popt
sigma_m, sigma_q = np.sqrt(pcov.diagonal())
print(m_hat, sigma_m, q_hat, sigma_q)
# Grafico del modello di best fit.
c = np.linspace(0., 40., 100)
plt.plot(c, line(c, m_hat, q_hat))
# Formattazione del grafico.
plt.xlabel("Posizione [cm]")
plt.ylabel("Temperatura [$^\\circ$C]")
plt.grid(which="both", ls="dashed", color="gray")


#grafico dei residui
fig.add_axes((0.1, 0.07, 0.8, 0.2))
plt.grid(which='both', ls='dashed', color='gray')
plt.errorbar(x,T-line(x, m_hat, q_hat),yerr=0.2,fmt='.')

plt.savefig("posizione_temperatura_materiale2.pdf")

# A questo punto potete usare i risultati del fit per stimare la
# conducibilita‘ vera e propria...

plt.show()

