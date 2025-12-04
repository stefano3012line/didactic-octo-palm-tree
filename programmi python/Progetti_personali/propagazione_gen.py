import numpy as np
import sympy as sp

##Generale
var_holder={}
#caricamento delle misure e degli errori sulle misure
var=[983,1971]
err=[1,1]


#crea i simboli
for i in range(len(var)):
    var_holder['x'+str(i)] =sp.symbols('x'+str(i))
locals().update(var_holder)

#definire la funzione dove xi corrisponde alla i-esima misura
f1=x1/x0


def Prop(f1, var,err):
    Sigma=0
    for i in range(len(var)):
#calcolo delle incertezze con metodo delle derivate
        Sigma+=((sp.diff(f1,'x'+ str(i)))*err[i])**2


#sostituzione dei valori nella formula
    for i in range(len(var)):
        f1=f1.subs('x'+str(i),var[i])
        Sigma=Sigma.subs('x'+str(i),var[i])

#esplicitazione variabili
    Sigma=float(sp.sqrt(Sigma))
    f1=float(f1)
    return f1,Sigma

if __name__ == '__main__':
    P=Prop(f1, var,err)
    print('il risultato è ',P[0],'\pm',P[1])
