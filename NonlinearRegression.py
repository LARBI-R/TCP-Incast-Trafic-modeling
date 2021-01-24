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



SRU = 256000 * 8 # bits
S = 1446 * 8 # bits

t = np.arange(35)

data = pd.read_csv('incast_all.csv')

#donnees
RTT = 1e-3 * data.iloc[0:35, 7]
C = 1e6 * data.iloc[0:35, 5]
N = data.iloc[0:35,9]
 
RTT = RTT.tolist()
N = N.tolist()
C = C.tolist()
fct_simu = 1e-3 * data.iloc[0:35,11]
fct_simu = fct_simu.tolist()

#initial guess for a et b
a = 2
b = SRU
c = S
d = S
abcd = 2, SRU, S, S

test =[]
for l in range(35):
    test.append(analytical_model(RTT[l],N[l],SRU, C[l]))

plt.plot(t, test)
plt.show()

test = []
sol,cov = curve_fit(fctf, (RTT,N,C), fct_simu, abcd) 
print(sol)