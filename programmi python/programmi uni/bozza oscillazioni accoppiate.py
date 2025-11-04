import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import math
#prima parte
g=9.81
m=1
l=1
I=1

W_0=math.sqrt(m*g*l/I)
print("W_0=")
print(W_0)
#seconda parte

def theta_0(t):

    theta_0=2*math.e**(-t/1)
    return theta_0
print("theta_0=")
print(theta_0(10))



def tau(theta_t,t,theta_start):
    tau=- (t/(np.log(theta_t/theta_start)))
    return tau


print(tau(5,5,6))
#misurare w in fase ed in controfase
#misurare pulsazione modulante(battimenti) e portante e vedere che si rispettino i risultati dati da w_f e w_c
w_f=np.array([1,3,2,4,5])
w_c=np.array([2,4,6,8,10])
def w_p(w_f,w_c):
    "pulsazione portante"
    return (w_c+w_f)/2
def w_b(w_f,w_c):
    "pulsazione modulante"
    return (w_c-w_f)/2
print("w_p=")
print(w_p(w_f,w_c))
print("w_b=")
print(w_b(w_f,w_c))

