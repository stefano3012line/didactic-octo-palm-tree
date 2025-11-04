import numpy as np
from matplotlib import pyplot as plt
import math

n0 =300
#"numero di lanci"
k0 = 145
#"numero di successi"

#calcolo della verosomiglianza di una moneta a 2 esiti
def L(p,x,y):
    if y == 1 or y == x:
        div= 1
    elif y > x:
        div= 0
    else:
        a = math.factorial(x)
        b = math.factorial(y)
        div = a // (b*math.factorial(x-y))
    Div=div*(p**y)*((1-p)**(x-y))
    return Div

#plot della verosomiglianza in funzione della probabilità di avere testa
p=np.linspace(0,1,10000)

plt.plot(p,L(p,n0,k0))
plt.show()
#probabilità con massimo valore della verosomiglianza
x=0

print(L(0.49,n0,k0))
print(L(0.51,n0,k0))
#estendere a verosomiglianze composite