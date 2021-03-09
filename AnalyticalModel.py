import pandas as pd
from scipy.optimize import curve_fit
import numpy as np
import math
import matplotlib.pyplot as plt


def analytical_model(RTT, N, SRU, C):    
    k = math.ceil(math.log((N*SRU/S)+1,2))
    tStall = 0
    for k in range(1, k):
        tStall = tStall + max((S/C +RTT - (2**(k-1)*S/C)), 0)
    return (2*RTT + N*SRU/C + tStall) 

'''
def fctf(X, a, b, c, d):
    x,y,z = X
    SRU = 256000*8
    S = 1446*8

    som = 0
    tau = []
    for k in range(35):
        f = int (math.log( (y[k] * SRU)/S +1, 2))
        for h in range((f-1)):
            if h == 0:
                continue
            som = som + ( ( c/z[k] )  + x[k] - ( (2**(f-1) * d) / z[k] ) ) 
            if som < 0:
                som = 0
        tau.append( a*x[k] + ( b * (y[k] /z[k] ) + som ) )
        som = 0
    return tau
'''


SRU = 256000 * 8 # bits
S = 1446 * 8 # bits

# vecteur temporel
Nbr_echantillons = 35
offset = 1200 # first line of read
t = np.arange(Nbr_echantillons)

#lecture CSV
data = pd.read_csv('simus.csv')

#donnees pour FIFO
start_line = 0 + offset
if ( start_line+Nbr_echantillons > 15491):
    print('youve exceeded number of lines')
RTT = 1e-3 * data.iloc[start_line:start_line+Nbr_echantillons, 6]
C = 1e6 * data.iloc[start_line:start_line+Nbr_echantillons, 5]
N = data.iloc[start_line:start_line+Nbr_echantillons,9]
fct_simu = 1e-3 * data.iloc[start_line:start_line+Nbr_echantillons,11]

#donnees pour FQ
start_line_FQ = 15492 + offset
if ( start_line_FQ+Nbr_echantillons > 30993):
    print('youve exceeded number of lines')
RTT_FQ = 1e-3 * data.iloc[start_line_FQ:start_line_FQ+Nbr_echantillons, 6]
C_FQ = 1e6 * data.iloc[start_line_FQ:start_line_FQ+Nbr_echantillons, 5]
N_FQ = data.iloc[start_line_FQ:start_line_FQ+Nbr_echantillons,9]
fct_simu_FQ = 1e-3 * data.iloc[start_line_FQ:start_line_FQ+Nbr_echantillons,11]

#donnees DCTCP-RED-ECN
start_line_DCTCP = 30994 + offset
if ( start_line_DCTCP+Nbr_echantillons > 46580):
    print('youve exceeded number of lines')
RTT_DCTCP = 1e-3 * data.iloc[start_line_DCTCP:start_line_DCTCP+Nbr_echantillons, 6]
C_DCTCP = 1e6 * data.iloc[start_line_DCTCP:start_line_DCTCP+Nbr_echantillons, 5]
N_DCTCP = data.iloc[start_line_DCTCP:start_line_DCTCP+Nbr_echantillons,9]
fct_simu_DCTCP = 1e-3 * data.iloc[start_line_DCTCP:start_line_DCTCP+Nbr_echantillons,11]


'''
# Optimisation 

#initial guess for a et b
a = 2
b = SRU
c = S
d = S
abcd = 2, SRU, S, S

sol,cov = curve_fit(fctf, (RTT,N,C), fct_simu, abcd) 
print(sol)
'''

# plot analytical model FIFO

RTT = RTT.tolist()
N = N.tolist()
C = C.tolist()

test =[]
for l in range(35):
    test.append(analytical_model(RTT[l],N[l],SRU, C[l]))

plotFIFO, = plt.plot(t, test)


# plot analytical model FQ

RTT_FQ = RTT_FQ.tolist()
N_FQ = N_FQ.tolist()
C_FQ = C_FQ.tolist()

test =[]
for l in range(35):
    test.append(analytical_model(RTT_FQ[l],N_FQ[l],SRU, C_FQ[l]))

plotFQ, = plt.plot(t, test)



# plot analytical model DCTCP

RTT_DCTCP = RTT_DCTCP.tolist()
N_DCTCP = N_DCTCP.tolist()
C_DCTCP = C_DCTCP.tolist()
test =[]
for l in range(35):
    test.append(analytical_model(RTT_DCTCP[l],N_DCTCP[l],SRU, C_DCTCP[l]))

plotDCTCP, = plt.plot(t, test)

plt.legend([plotFIFO,plotFQ, plotDCTCP],["analytique FIFO", "Analytique FQ", "Analytique DCTCP"])

plt.show()