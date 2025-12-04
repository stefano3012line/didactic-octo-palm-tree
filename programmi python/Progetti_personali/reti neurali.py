import numpy as np
import matplotlib.pyplot as plt
def Loss(Yp,Y):
    m=len(Y)
    return -np.sum(Y*np.log(Yp)+(1-Y)*np.log(1-Yp))/m

#f di attivazione
g1 = np.tanh #layer nascosto
def g2(x): #layer output
    return 1/(1+np.exp(-x))

def init(n):
    #hidden layer
    W1=np.random.randn(n,2)
    b1=np.random.rand(n,1)

    #output layer
    W2 = np.random.randn(1,n)
    b2=np.random.rand(1,1)
    return W1,b1,W2,b2



def predict(X,W1,b1,W2,b2):
    #Hidden
    Z1 = W1 @ X +b1
    A1 = g1(Z1)
    #output
    Z2 = W2 @ A1 +b2
    A2 = g2(Z2)
    return A1,A2

def backpropagation(X,Y,lr,A1,A2,W1,b1,W2,b2):
    #output
    m=len(Y)
    dLdZ2 = A2 - Y
    dLdW2 = dLdZ2 @ A1.T /m
    dLdb2 = np.sum(dLdZ2, axis=1)[:,None]/m
    #hidden
    dLdZ1 = W2.T @ dLdZ2 * (1-A1**2)
    dLdW1 =  dLdZ1 @ X.T /m
    dLdb1 = np.sum(dLdZ1, axis=1)[:,None]/m
    W1 -= lr*dLdW1
    b1-= lr*dLdb1
    W2 -= lr*dLdW2
    b2-= lr*dLdb2
    return W1,b1,W2,b2


def train(X,Y,n_epoch,neuro,lr):
    W1,b1,W2,b2=init(neuro)
    L_t= np.zeros(n_epoch)
    L_v= np.zeros(n_epoch)

    N=X.shape[1]
    M=N//4

    #divido in train e validation
    X_train,Y_train=X[:,:N-M],Y[:N-M]
    X_valid,Y_valid =X[:,N-M:],Y[N-M:]

    for i in range(n_epoch):
        A1,A2 = predict(X_train,W1,b1,W2,b2)
        L_t[i]=Loss(A2,Y_train)
        #validation
        _,Yp=predict(X_valid,W1,b1,W2,b2)
        L_v[i]=Loss(Yp,Y_valid)
        #update
        W1,b1,W2,b2 =backpropagation(X_train,Y_train,lr,A1,A2,W1,b1,W2,b2)

    if not i%100:
        print(f"Loss={L_t[1]:.3f},epoca={i}  \r",end='')
    print()
    result = {'parametri': (W1,b1,W2,b2),'train_loss':L_t,'valid_loss':L_v}
    return result



if__name__="__main__"
np.random.seed(69420)

N = 5000
M = 1000
X = np.random.random(size=(2,N))
Y= np.ones(N)

#creo il dataset
for x1,x2,i in zip(X[0,:],X[1,:],range(N)):
    if np.sqrt((x1-0.3)**2 +(x2-0.3)**2)<0.2:
        Y[i]=0
    if np.sqrt((x1-0.65)**2 +(x2-0.7)**2)<0.2:
        Y[i]=0

X_train,Y_train=X[:,:N-M],Y[:N-M]
X_valid,Y_valid =X[:,N-M:],Y[N-M:]

#parametri
n_epoch= 6000+1
neuro=20
mimmo=1.5

result=train(X_train,Y_train,n_epoch,neuro,mimmo)
L_t = result['train_loss']
L_v = result['valid_loss']


epoche = np.linspace(1,n_epoch,n_epoch)
plt.plot(epoche,L_t,'magenta')
plt.plot(epoche,L_v,'cyan')

plt.show()













