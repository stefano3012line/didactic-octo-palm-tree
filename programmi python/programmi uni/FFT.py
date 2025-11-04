import numpy as np 
from matplotlib import pyplot as plt 
import os
from scipy.optimize import curve_fit 
from scipy import signal
from scipy.optimize import least_squares
import math 

# TUTTE LE FUNZIONI DI FIT


#funzione sisnusoide
def SENO(t,A,omega,phi,O):
    
    return A*np.sin(omega*t + phi) + O

#funzione sinusoidale smorzata
def SMORZATO(t,A,omega,phi,tau,O):
    
    return A*np.exp(-t*tau)*np.sin(omega*t + phi) + O

#funzione pinna di squalo
def SQUALO(t,A,omega,omega_t,O):
    D = np.zeros(len(t))
    n = 500                    # NUMERO DI ARMONICHE 
    for i in range(n):
        k = 2*i + 1
        b_k = 2/(k*np.pi)
        omega_k = k*omega
        f_k = np.arctan(-omega_k/omega_t)
        D = D +  A*(1/np.sqrt(1 + (omega_k/omega_t)**2))*b_k*np.sin(omega_k*t + f_k)
    return D + O    

#funzione onda quadra
def QUADRA(t, A, omega, phi, O):
    return O + A * np.sign(np.sin( omega * t + phi ))
    
def soft_wave( t , A, omega, phi, O, s=1 ):
    return O + A * np.tanh( s * np.sin( omega * t + phi ) )

#funzione triangolare
def TRIANGOLARE(t,A,omega,phi,O):

    return A*signal.sawtooth(omega* t + phi,width=0.5) + O
    
    
# funzioni necessarie per fittare l'onda quadra    # funzioni necessarie per fittare l'onda quadra    # funzioni necessarie per fittare l'onda quadra 

def residuals( params, xdata, ydata, s ):
    #A , omega, phi, O = params
    yt = soft_wave( xdata,*params, s=s )
    return yt - ydata    

def fit_quadra(t,x,p_guess):

    soldict = dict()
    previous = p_guess  # parametri iniziali
    for mys in range( 2, 8050, 16 ):
        res = least_squares( residuals, x0=previous, args=( t, x, mys ) )
    
        previous = res.x
        soldict[mys] = np.append( res.x, mys )
    covarianza = np.linalg.inv( np.dot( np.transpose( res.jac ), res.jac ) ) 
    return soldict[8034][:4] , covarianza


# funzione che calcola il guess del tempo di smorzamento 
def TAU(t,x):
    x1 = x - np.mean(x)
    A_01 = (np.max(x1) - np.min(x1))/2
    A_m = A_01/np.e


    tau = 1/t[x>A_m][-1]
    print(tau)
    return tau 
#funzione che calcola le x degli n picchi più alti delle y 
def n_picchi(x, y, n):
    i_peek , _ = signal.find_peaks(y)             # SINTASSI DI FIND_PEAKS MOLTO UTILE
    array_picchi = y[i_peek]
    indeces1 = np.arange(len(array_picchi))
    indeces2= sorted(indeces1, key=lambda i: array_picchi[i], reverse=True)[:n]
    indeces_peeks = i_peek[indeces2]
    return x[indeces_peeks] , y[indeces_peeks]

# funzione che fa la fft 
def FFT(t,x):
    x1 = x - np.mean(x) 
    T = t[len(t) - 1]#*1e-6   #se non si vogliono convertire i tempi mettere 1e-6 per avere le frequenze in Hertz
    sp = abs(np.fft.rfft(x1))
    
    freq = np.fft.rfftfreq(len(x1),T/len(x1))
    return freq , sp 


#FUNZIONE CHE FA I FIT
def FIT(t,x,f):

    M = max(x) 
    m = min(x) 
    A_0 = (M - m)/2                     # guess ampiezza
    O_0 = np.mean(x)                    # guess offset 
    
    

    
    omega_0 = 2*np.pi*n_picchi(*FFT(t,x), 1)[0][0]  # guess frequenza      #se non si vogliono convertire i tempi mettere 1e-6 per avere le frequenze in Hertz e+6
    
    if f == SMORZATO:                           # condizioni inziali
        phi_0 = np.arcsin((x[0]-O_0)/A_0)       #fase inizale  
        tau_0 = TAU(t,x)
        p_0 = np.array([-A_0,omega_0,phi_0,tau_0,O_0])
        #print(p_0[3])
        p_opt , p_cov = curve_fit(f,t,x,p_0, maxfev=5000)
        
    elif f == SQUALO:
        omegat_0 = 0.0002*1e6                                           # INSERIRE MANUALMENTE IL VALORE DELLA FREQUENZA DI TAGLIO
        A_02 = A_0*np.sqrt(1+(omega_0/omegat_0)**2)*np.pi/2
        p_0 = np.arrayp_0 = np.array([-A_02,omega_0,omegat_0,O_0])
        p_opt , p_cov = curve_fit(f,t,x,p_0, maxfev=5000)
    elif f == QUADRA:
        p_0 = np.array([A_0,omega_0,np.pi/2,O_0])                      # INSERIRE MANUALMENTE IL VALORE DELLA FASE 
        p_opt , p_cov = fit_quadra(t,x,p_0)                                                 
    else:
        phi_0 = np.arcsin((x[0]-O_0)/A_0)       #fase inizale 
        p_0 = np.arrayp_0 = np.array([A_0,omega_0,phi_0,O_0])
        p_opt , p_cov = curve_fit(f,t,x,p_0, maxfev=5000)

    err = np.sqrt(p_cov.diagonal())
    return p_0 , p_opt , err

#FUNZIONE CHE FA LA FFT DEL FIT

def FFT_FIT(p_opt,t1,f):

    x2 = f(t1,*p_opt) - p_opt[-1] 
    T2 = t1[- 1]#*1e-6      #se non si vogliono convertire i tempi mettere 1e-6 per avere le frequenze in Hertz
    sp2 = abs(np.fft.rfft(x2))
    freq2 = np.fft.rfftfreq(len(x2),T2/len(x2))
    return freq2 , sp2
    
#FUNZIONE CHE METTE TUTTO INSIEME   # N = numero di picchi della FFT che si vogliono visualizzare

def F(folder,F):
    if  F == 'SENO SMORZATO':
        f = SMORZATO
        cp = 'teal'              # colore punto
        cl = 'lightseagreen'     # colore linea
        N = 1
    if F == 'SINUSOIDE':
        f = SENO
        cp = 'mediumvioletred'  
        cl = 'palevioletred'
        N = 1
    if F == 'PINNA DI SQUALO':
        f = SQUALO
        cp = 'forestgreen'
        cl = 'mediumseagreen'
        N = 4
    if F == 'ONDA QUADRA':    
        f = QUADRA 
        N = 5                    
        cp = 'steelblue'
        cl = 'lightsteelblue'
    if F == 'ONDA TRIANGOLARE':
        f = TRIANGOLARE
        cp ='royalblue'
        cl = 'mediumpurple'
        N = 4
    with os.scandir(folder) as path:
        for p in path:
            t,x = np.loadtxt(folder + '/' + p.name, unpack = True)
            t = t*1e-6                                                     #conversione da microsecondi a secondi 
            t3 = np.linspace(0, max(t), 10000)                             #linspace per il fit
            t4 = np.linspace(0,150*max(t), 2**19)                          #linspace per la fft del fit 
            
            P_0 , P_OPT , ERR = FIT(t,x,f)
            nn = math.ceil(abs(np.log10(abs(ERR[1])))) 
            FREQ , SP = FFT(t,x)
            FREQ_FIT , SP_FIT = FFT_FIT(P_OPT,t4,f)
            
            f_p , s_p = n_picchi(FREQ, SP, N)
            f_p_fit, s_p_fit = n_picchi(FREQ_FIT, SP_FIT, N)
            
            fig = plt.figure(p.name)
            ax1 = fig.add_subplot(3,1,1)
            ax2 = fig.add_subplot(3,1,2)
            ax3 = fig.add_subplot(3,1,3)
            
            ax1.plot(t3,f(t3,*P_OPT), color= cl, label= f'f={round(P_OPT[1]/2/np.pi,nn)} +- {round(ERR[1],nn)} [Hz] ')
            #ax1.plot(t3,f(t3,*P_0), color= 'black' )          # plot delle condizioni inizali
            ax1.set_xlabel('tempo[s]', fontsize= 12 , labelpad = 10)
            ax1.set_ylabel('ampiezza[Au]',fontsize= 12,labelpad = 25)
            ax1.legend(handlelength=0,handletextpad=0,fancybox=True,loc='upper right',labelcolor='black')
            ax1.plot(t[::6],x[::6],color= cp,marker = '.', linestyle ='None' )                                 # modificare il numero di punti che si vuole plottare
            
            ax2.title.set_text('FFT del fit')
            ax2.plot(FREQ_FIT,SP_FIT, color = cl)
            for  i , (F , S) in enumerate(zip(f_p_fit,s_p_fit)):
                ax2.plot(F,S, marker = 'x', linestyle = 'None', label = f'f{i+1}={round(F,3)} [Hz]')
                ax2.legend(handletextpad=0,fancybox=True,loc='upper right',labelcolor='black')
            
            ax2.set_xlim(FREQ_FIT[0],FREQ_FIT[-1]/4)
            
            ax3.title.set_text('FFT dei dati')
            ax3.plot(FREQ, SP, color = cl)
            for  i , (F , S) in enumerate(zip(f_p,s_p)):
                ax3.plot(F,S, marker = 'x', linestyle = 'None', label = f'f{i+1}={round(F,3)} [Hz]')
                ax3.legend(handletextpad=0,fancybox=True,loc='upper right',labelcolor='black')
            
            ax3.set_xlabel('frequenza[Hz]', fontsize= 12,labelpad = 10)
            ax3.set_xlim(FREQ[0],FREQ[-1]/4)
            
            #plt.tight_layout(h_pad =-2,rect = (-0.1,0,1,1))
           
#path_C = "/Users/Dell/Pictures/Esperienze lab/Dati_exp_aprile/pinne di squelli-20240403T162144Z-001/pinne di squelli"     # pinna di squalo          
path_C = "/Users/Dell/Desktop/EXP131"      # oscillatori smorzati 
#path_C =  "/Users/Dell/Desktop/exp 12 plus"        # quadre 
#path_C = "/Users/Dell/Pictures/Esperienze lab/Dati_exp_aprile/drive-download-20240403T162133Z-001"    # sinusoidi
# funzioni presenti: 'SINUSOIDE' 'ONDA TRIANGOLARE' ' PINNA DI SQUALO' 'SENO SMORZATO'  'ONDA QUADRA'

F(path_C,'SENO SMORZATO')
plt.show()

