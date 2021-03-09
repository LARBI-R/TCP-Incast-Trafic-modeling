import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandas_ods_reader import read_ods

# close all figure
plt.close("all")

SRU = 256000 * 8 # bits
S = 1446 * 8 # bits

# vecteur temporel
nb_iteration = 35 #total lignes calc = 15493
offset = 0 # first line of read
t = np.arange(nb_iteration)

# getData -> CSV
data = pd.read_csv('simus.csv')

#test1 = read_ods("tableur_projet.ods",4)


#donnees pour FIFO
start_line = 0 + offset
if ( start_line+nb_iteration > 15491):
    print('youve exceeded number of lines')
RTT = 1e-3 * data.iloc[start_line:start_line+nb_iteration, 6]
C = 1e6 * data.iloc[start_line:start_line+nb_iteration, 5]
N = data.iloc[start_line:start_line+nb_iteration,9]
RTO = data.iloc[start_line:start_line+nb_iteration, 4]
fct_simu = 1e-3 * data.iloc[start_line:start_line+nb_iteration,11]

#donnees pour FQ
start_line_FQ = 15492 + offset
if ( start_line_FQ+nb_iteration > 30993):
    print('youve exceeded number of lines')
RTT_FQ = 1e-3 * data.iloc[start_line_FQ:start_line_FQ+nb_iteration, 6]
C_FQ = 1e6 * data.iloc[start_line_FQ:start_line_FQ+nb_iteration, 5]
N_FQ = data.iloc[start_line_FQ:start_line_FQ+nb_iteration,9]
fct_simu_FQ = 1e-3 * data.iloc[start_line_FQ:start_line_FQ+nb_iteration,11]
RTO_FQ = data.iloc[start_line_FQ:start_line_FQ+nb_iteration, 4]

#donnees DCTCP-RED-ECN
start_line_DCTCP = 30994 + offset
if ( start_line_DCTCP+nb_iteration > 46580):
    print('youve exceeded number of lines')
RTT_DCTCP = 1e-3 * data.iloc[start_line_DCTCP:start_line_DCTCP+nb_iteration, 6]
C_DCTCP = 1e6 * data.iloc[start_line_DCTCP:start_line_DCTCP+nb_iteration, 5]
N_DCTCP = data.iloc[start_line_DCTCP:start_line_DCTCP+nb_iteration,9]
fct_simu_DCTCP = 1e-3 * data.iloc[start_line_DCTCP:start_line_DCTCP+nb_iteration,11]
RTO_DCTCP = data.iloc[start_line_DCTCP:start_line_DCTCP+nb_iteration, 4]


# ------------------------ Reno - FIFO ------------------------ #

# calculs modele optimisé et modele 3
test3 = []
mod1op = []
B1 = 305.5451
B2 = 1.1590e+04

res = 0
som = 0
test1_cal = []
res1 = 0

err3 = []
err1op = []

for i in range(start_line, start_line + nb_iteration): #35
    res1 = ( int( (N[i] * SRU) / S) + 1 ) * (S/C)
    test1_cal.append(res1)
    mod1op.append((B1 * N[i] ) * B2 / C[i])
#    
#    for k in range(int( ( (N[i]*SRU)/(S) ) // (86) )) :
#        som = som + ( ( int ( (N[i]*SRU)/(S) ) + 1 ) - 86 *(k-1) - 86*k - B[i] ) * ( S/C ) 
#        print(( ( int ( (N[i]*SRU)/(S) ) + 1 ) - 86 *(k-1) - 86*k - B[i] ) * ( S/C ) ).
    
    repetition = (RTO[i])//(115.68*10**-6)
    
    som = 0
    for k in range(int( ( (SRU)/(S) ) // (repetition))) :
        #print(( int ( (SRU)/(S) ) + 1 ) - 86 *(k) - 86 - B[i] )
        som = som + (( ( int ( (SRU)/(S) ) + 1 ) - repetition *(k) - repetition - B[i] )) 
    
    res = (N[i]*SRU)//S + som + N[i]*178
    res = res*(S/C[i]) + 2*RTT[i]
    test3.append(res)
    err1op.append(abs(mod1op[i-start_line]-fct_simu[i]))
    err3.append(abs(test3[i-start_line] - fct_simu[i]))

plotFIFO_mod3, = plt.plot(t, test3)
plotsimuFIFO, = plt.plot(t, fct_simu)
plt.legend([plotFIFO_mod3, plotsimuFIFO],["Modele 3 FIFO", 
                                                      "Modele de simulation FIFO"])


plt.xlim(nb_iteration - 35,nb_iteration)
plt.show()

# ------------------------ Reno - FQ ------------------------ #


RTT = RTT_FQ
C = C_FQ
N = N_FQ
RTO = RTO_FQ
fct_simu = fct_simu_FQ


# calculs modele optimisé et modele 3
test3 = []
mod1op = []
B1 = 305.5451
B2 = 1.1590e+04

res = 0
som = 0
test1_cal = []
res1 = 0

err3 = []
err1op = []

for i in range(start_line_FQ, start_line_FQ + nb_iteration): #35
    res1 = ( int( (N[i] * SRU) / S) + 1 ) * (S/C)
    test1_cal.append(res1)
    mod1op.append((B1 * N[i] ) * B2 / C[i])
#    
#    for k in range(int( ( (N[i]*SRU)/(S) ) // (86) )) :
#        som = som + ( ( int ( (N[i]*SRU)/(S) ) + 1 ) - 86 *(k-1) - 86*k - B[i] ) * ( S/C ) 
#        print(( ( int ( (N[i]*SRU)/(S) ) + 1 ) - 86 *(k-1) - 86*k - B[i] ) * ( S/C ) ).
    
    repetition = (RTO[i])//(115.68*10**-6)
    
    som = 0
    for k in range(int( ( (SRU)/(S) ) // (repetition))) :
        #print(( int ( (SRU)/(S) ) + 1 ) - 86 *(k) - 86 - B[i] )
        som = som + (( ( int ( (SRU)/(S) ) + 1 ) - repetition *(k) - repetition - B[i] )) 
    
    res = (N[i]*SRU)//S + som + N[i]*178
    res = res*(S/C[i]) + 2*RTT[i]
    test3.append(res)
    err1op.append(abs(mod1op[i-start_line_FQ]-fct_simu[i]))
    err3.append(abs(test3[i-start_line_FQ] - fct_simu[i]))


plotFQ_mod3, = plt.plot(t, test3)
plotsimuFQ, = plt.plot(t, fct_simu)
plt.legend([plotFQ_mod3, plotsimuFQ],["Modele 3 FQ ", 
                                                    "Modele de simulation FQ"])


plt.xlim(nb_iteration - 35,nb_iteration)
plt.show()
# ------------------------ DCTCP ------------------------ #


RTT = RTT_DCTCP
C = C_DCTCP
N = N_DCTCP
RTO = RTO_DCTCP
fct_simu = fct_simu_DCTCP

# calculs modele optimisé et modele 3
test3 = []
mod1op = []
B1 = 305.5451
B2 = 1.1590e+04

res = 0
som = 0
test1_cal = []
res1 = 0

err3 = []
err1op = []

for i in range(start_line_DCTCP, start_line_DCTCP + nb_iteration): #35
    res1 = ( int( (N[i] * SRU) / S) + 1 ) * (S/C)
    test1_cal.append(res1)
    mod1op.append((B1 * N[i] ) * B2 / C[i])
#    
#    for k in range(int( ( (N[i]*SRU)/(S) ) // (86) )) :
#        som = som + ( ( int ( (N[i]*SRU)/(S) ) + 1 ) - 86 *(k-1) - 86*k - B[i] ) * ( S/C ) 
#        print(( ( int ( (N[i]*SRU)/(S) ) + 1 ) - 86 *(k-1) - 86*k - B[i] ) * ( S/C ) ).
    
    repetition = (RTO[i])//(115.68*10**-6)
    
    som = 0
    for k in range(int( ( (SRU)/(S) ) // (repetition))) :
        #print(( int ( (SRU)/(S) ) + 1 ) - 86 *(k) - 86 - B[i] )
        som = som + (( ( int ( (SRU)/(S) ) + 1 ) - repetition *(k) - repetition - B[i] )) 
    
    res = (N[i]*SRU)//S + som + N[i]*178
    res = res*(S/C[i]) + 2*RTT[i]
    test3.append(res)
    err1op.append(abs(mod1op[i-start_line_DCTCP]-fct_simu[i]))
    err3.append(abs(test3[i-start_line_DCTCP] - fct_simu[i]))

plotDCTCP_mod3, = plt.plot(t, test3)
plotsimuDCTCP, = plt.plot(t, fct_simu)
plt.legend([plotDCTCP_mod3, plotsimuDCTCP],["Modele 3 DCTCP", 
                                                      "Modele de simulation DCTCP"])


plt.xlim(nb_iteration - 35,nb_iteration)
plt.show()


# plot modeles, erreur

#plt.plot(t, test1_cal)
#plot1, = plt.plot(t, err3)
#plot2, = plt.plot(t, err1op)


#plt.legend([plot1,], ["erreur modele 1 optimisé"])

#plt.legend([plot1,plot2],["Erreur Modele 2", "Erreur Modele 1 optimisé"])



plt.show()