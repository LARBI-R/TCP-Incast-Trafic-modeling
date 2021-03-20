import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

# @retval 0 si mediocre
#		  1 si TRES MAUVAIS
#		  2 si MAUVAIS
#		  3 si MOYEN
#		  4 si BON
#		  5 si TRES BON
#		  6 si EXCELLENT

def Modele3(N, C, RTT, RTO, B):
	S = 1446 * 8 # bits
	SRU= 256000 *8	#en bits

	vit_trait_seg = S/C
	repetition = (RTO)//vit_trait_seg
	som = 0

	test = int((int( ( (SRU)/(S) )+1 )//((repetition) + B)))

	for k in range(test) :
		som = som + (( ( int ( (SRU)/(S) ) + 1 ) - repetition *(k) - repetition - B ))

	res = int((SRU)/S)+1 + som
	res = res*(N*S/C) + 2*RTT
	return res

def qos(N, C, RTT, RTO, B, fct):

	S = 1446 * 8 # bits
	SRU= 256000 *8	#en bits

	#res = Modele3(N, C, RTT, RTO, B)

	TempsReelViaSimulation = fct
	
	#TempsReelViaSimulation = res

	TempsTheoriqueSansCongestion= N*SRU/C + 2* RTT
	
	#TempsTheoriqueSansCongestion = res

	#diff = np.abs(TempsReelViaSimulation - TempsTheoriqueSansCongestion )	
	diff = (TempsReelViaSimulation - TempsTheoriqueSansCongestion )	

	#PourcentageDeTempsTheorique = diff*100/TempsTheoriqueSansCongestion

	#MultiplicateurDeTemps = 1 + PourcentageDeTempsTheorique/100
	MultiplicateurDeTemps = diff

	if(MultiplicateurDeTemps<0.002):
		return 6

	elif(MultiplicateurDeTemps<0.02):
		return 5

	elif(MultiplicateurDeTemps<0.2):
		return 4

	elif(MultiplicateurDeTemps<1):
		return 3

	elif(MultiplicateurDeTemps<3):
		return 2
	else :
		return 0


#test1 = read_ods("tableur_projet.ods",4)

#read tableur
data = pd.read_csv('simus.csv')

#donnees pour FIFO

RTT = 1e-3 * data.iloc[0:15492, 6]
C = 1e6 * data.iloc[0:15492, 5]
N = data.iloc[0:15492,9]
RTO = 1e-3*data.iloc[0:15492, 4]
fct_simu = 1e-3 * data.iloc[0:15492,11]
B =  data.iloc[0:15492,8]

nbmediocre = 0
nbTRESMAUVAIS = 0
nbMAUVAIS = 0
nbMOYEN = 0
nbBON = 0
nbTRESBON = 0
nbexcellent	= 0
 
for k in range(15492):

	a = qos(N[k],C[k],RTT[k], RTO[k], B[k], fct_simu[k])
	
	if a == 6:
		nbexcellent += 1
	elif a == 5:
		nbTRESBON += 1
	elif a == 4:
		nbBON += 1
	elif a == 3:
		nbMOYEN += 1
	elif a == 2:
		nbMAUVAIS += 1
	#elif a == 1:
	#	nbTRESMAUVAIS += 1
	elif a == 0:
		nbmediocre += 1

print('nbexcellent = ' + str(nbexcellent))
print('nbTRESBON = ' + str(nbTRESBON))
print('nbBON = ' + str(nbBON))
print('nbMOYEN = ' + str(nbMOYEN))
print('nbMauvais = ' + str(nbMAUVAIS))
#print('nbTRESMAUVAIS = ' + str(nbTRESMAUVAIS))
print('nbmediocre = ' + str(nbmediocre))

