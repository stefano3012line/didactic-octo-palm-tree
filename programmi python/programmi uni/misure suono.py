import math
v=   0.56736
r=10*v/(1-v)

T=((1/(298.15))+ math.log(r/10)/(3950))**(-1) -273.15
print(T)




c=331.5+0.6*T
print(c)

t=1.684*10**(-3)
V=0.58/t
print(V)