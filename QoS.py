import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def qos(N, C, fct):

	SRU= 256000 *8	#en bits

	TempsReelViaSimulation = fct
	TempsTheoriqueSansCongestion=N*SRU/C
	diff = np.abs(TempsReelViaSimulation - TempsTheoriqueSansCongestion )	
	PourcentageDeTempsTheorique = diff*100/TempsTheoriqueSansCongestion
	MultiplicateurDeTemps = 1 + PourcentageDeTempsTheorique/100

	if(MultiplicateurDeTemps<1.5):
		print("EXCELLENT")

	elif(MultiplicateurDeTemps<2.5):
		print("TRES BON")

	elif(MultiplicateurDeTemps<5):
		print("BON")

	elif(MultiplicateurDeTemps<10):
		print("MOYEN")

	elif(MultiplicateurDeTemps<20):
		print("MAUVAIS")

	elif(MultiplicateurDeTemps<30):
		print("TRES MAUVAIS")
	else :
		print("MEDIOCRE")



data = pd.read_csv('incast_all.csv')

C = 1e6 * data.iloc[:, 5]
N = data.iloc[:,9]
fct_simu = 1e-3 * data.iloc[:,11]
 
for k in range(8):
	qos(N[k],C[k],fct_simu[k])

