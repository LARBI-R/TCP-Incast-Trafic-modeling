t_line:start_line+Nbr_echantillons, 6]
C = 1e6 * data.iloc[start_line:start_line+Nbr_echantillons, 5]
N = data.iloc[start_line:start_line+Nbr_echantillons,9]
fct_simu = 1e-3 * data.iloc[start_line:start_line+Nbr_echantillons,11]

#donnees pour FQ
start_line_FQ = 15492
if ( start_line_FQ+Nbr_echantillons > 30993):
    print('youve exceeded number of lines')
RTT_FQ = 1e-3 * data.iloc[start_line_FQ:start_line_FQ+Nbr_echantillons, 6]
print('length =  ' + str(len(RTT_FQ)))
C_FQ = 1e6 * data.iloc[start_line_FQ:start_line_FQ+Nbr_echantillons, 5]
N_FQ = data.iloc[start_line_FQ:start_line_FQ+Nbr_echantillons,9]
fct_simu_FQ = 1e-3 * data.iloc[start_line_FQ:start_line_FQ+Nbr_echantillons,11]

#donnees DCTCP-RED-ECN
start_line_DCTCP = 30994
if ( start_line_DCTCP+Nbr_e