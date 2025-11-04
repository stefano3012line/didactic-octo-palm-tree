import matplotlib.pyplot as plt
c=0
x=10
giorni=3
#iniziato il 16/10/2023

while c<giorni:
    x=x*1.01

    plt.errorbar(c,x,color="b",fmt=".")
    c=c+1
plt.grid(which="both", ls="dashed", color="gray")
print(x/100)

plt.show()