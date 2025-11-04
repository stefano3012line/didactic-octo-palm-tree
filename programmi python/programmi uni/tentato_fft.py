import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

t,x=np.loadtxt("C:/Users/Dell/Downloads/drive-download-20240514T132226Z-001/vd nesi 9 single sweep.txt",unpack=True)

w=0.001
def func(x,t,w):
    x=x*np.sin(w*t)
    return x
plt.figure('plot')
plt.plot(t,func(x,t,w),'.')
plt.ylabel("V[a.u.]")
plt.xlabel("t[mus]")



plt.show()

def FFT(t,x):
    x1 = x - np.mean(x)
    T = t[-1]#*1e-6   #se non si vogliono convertire i tempi mettere 1e-6 per avere le frequenze in Hertz
    sp = abs(np.fft.rfft(x1))
    freq = np.fft.rfftfreq(len(x1),T/len(x1))
    return  freq, sp


def F(t,w,phi,off,tau,A):
    return off+A*np.sin(w*t+phi)*np.exp(-t/tau)

popt,pcov=curve_fit(F,t,x,p0=(3/5000,0,np.mean(x),100,max(x)-np.mean(x)))

T=np.linspace(0,max(t),5000)
plt.figure('fit')
plt.plot(T,F(T,*popt),'-')
plt.plot(t,x,'.')
plt.ylabel("V[a.u.]")
plt.xlabel("t[mus]")



plt.figure('fft')
FREQ , SP = FFT(t,x)
plt.plot(*FFT(t,x))
plt.ylabel("[a.u.]")
plt.xlabel("freq[herz]")
plt.yscale('log')



plt.show()
