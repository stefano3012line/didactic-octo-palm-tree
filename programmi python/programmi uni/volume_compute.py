import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import math





def Cilindro(h,d,sig_h,sig_d):
    Volume=((d/2)**2)*math.pi*h
    sigmaV=math.sqrt((((math.pi*d**2)/4)*sig_h)+(((math.pi*h*d)/2)*sig_d))
    return Volume,sigmaV
print('cilindro1all')
print(Cilindro(19.64,5.97,0.02,0.01))
print('cilindro2all')
print(Cilindro(11.86,11.96,0.02,0.01))
print('cilindro1ott')
print(Cilindro(16.96,9.95,0.02,0.01))
print('cilindro2ottonel')
print(Cilindro(37.48,9.96,0.02,0.01))


def sigmaC(h,d):
    sigma=math.sqrt



def paral(h,d,s,sig_h,sig_d,sig_s):
    V=h*d*s
    sigmaV= V*math.sqrt(((sig_h/h)**2)+((sig_s/s)**2)+((sig_d/d)**2))

    return V,sigmaV




print('parall alluminio')
print(paral(8.13,18.24,20.07,0.01,0.02,0.02))
print('paral2alluminio semi cubo')
print(paral(10.05,10.06,17.93,0.01,0.01,0.01))
print('paral3ottone semicubo')
print(paral(9.94,10.10,41.62,0.01,0.01,0.02))

def sigmaparal(h,d,s,sig_h,sig_d,sig_s):
    V= h*d*s*math.sqrt(((sig_h/h)**2)+((sig_s/s)**2)+((sig_d/d)**2))

    return V

print(sigmaparal(8.13,18.24,20.07,0.01,0.02,0.02) )


def esagono(a,h,sig_a,sig_h):
    V=h*(a**2)*math.sqrt(3)/2
    sigmaV:math.sqrt((a*math.sqrt(3)*sig_a)**2+(sig_h/h)**2)
    return V

print(esagono(9.92,22.66,0.02,0.02))




def sfera(d,sigma_d):
    V=(4/3)*math.pi*(d/2)**3
    sigmaV=(math.pi/2)*(d**2)*sigma_d
    return V

print('sfera1')
print(sfera(14.28,0.01))
print('sfera2')
print(sfera(16.66,0.01))
print('sfera3')
print(sfera(18.24,0.01))
print('sfera4')
print(sfera(22.12,0.02))

