import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandas_ods_reader import read_ods


plt.close("all")

nb_iteration = 5200 #total lignes calc = 15493

SRU = 256000 * 8 # bits
S = 1446 * 8 # bits

t = np.arange(nb_iteration)

data = pd.read_csv('incast_all.csv')

#test1 = read_ods("tableur_projet.ods",4)


#test1_fct = test1.iloc[0:35,17]


N = data.iloc[0:nb_iteration,9]
C = 1e6 * data.iloc[0:nb_iteration, 5]
B = data.iloc[0:nb_iteration, 8]
RTT = 1e-3 * data.iloc[0:nb_iteration, 6]
RTO = 1e-3 * data.iloc[0:nb_iteration, 4]

fct_simu = 1e-3 * data.iloc[0:nb_iteration,11]

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

fo = open("test3.txt", "w")



for i in range(nb_iteration) : #35
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
    err1op.append(abs(mod1op[i]-fct_simu[i]))
    err3.append(abs(test3[i] - fct_simu[i]))
    fo.write(str(res)+"\n")

fo.close()

#plt.plot(t, test1_cal)
#plot1, = plt.plot(t, err3)
#plot2, = plt.plot(t, err1op)

plot1, = plt.plot(t, mod1op)
plot2, = plt.plot(t, fct_simu)

#plt.legend([plot1,], ["erreur modele 1 optimisé"])

#plt.legend([plot1,plot2],["Erreur Modele 2", "Erreur Modele 1 optimisé"])

plt.legend([plot1,plot2],["Modele 1 optimisé", "Modele de simulation"])


plt.xlim(5100,5200)

plt.show()