import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
def skill(k,d,a,dmg,heal,blk,t):
     return (k-(d/2)+a+(dmg/500)+(heal/300)+(blk/600))/t

c=0
k,d,a,dmg,heal,blk,t=np.loadtxt(r"C:\Users\Dell\Desktop\skill andrea.txt", unpack=True)


round=np.full(len(k),0)
while c<len(k):
    round[c]=c+1
    c=c+1


skill=skill(k,d,a,dmg,heal,blk,t)
skillM=np.full(len(round),np.mean(skill))
print(skillM)
plt.figure("skill ghera")
plt.errorbar(round,skill,color="r")
plt.plot(round,skillM)
plt.ylabel('skill[azioni per minuto]')
plt.xlabel('round')
plt.show()
