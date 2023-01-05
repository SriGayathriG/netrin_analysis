import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from preprocessing import remove_outliers,remove_ectopic_beats,interpolate_nan_values, get_nn_intervals
from extract_features import get_time_domain_features, get_geometrical_features, get_frequency_domain_features, get_poincare_plot_features, get_csi_cvi_features, get_sampen,DFA, _get_freq_psd_from_nn_intervals
import pdb
all_files = ['BLEData_Navin_2022_12_19.json','BLEData_Ajay_2022_12_20.json','BLEData_Soundarraj_Mani_2022_12_20.json','BLEData_athul_2022_12_21.json','BLEData_aswath_2022_12_21.json']
for file in all_files:
    with open(file) as json_file:
      main_file = json.load(json_file)
    rr_in_ms = main_file['captured_data']['hr']['RR in ms']
    nn_interval = get_nn_intervals(rr_in_ms, 300,2000,"linear", "acar")
    hr = 60000./np.array(nn_interval)
    plt.plot(hr,marker ='.')
    plt.show()
    cum_arr = np.array(rr_in_ms).cumsum()
    print(len(cum_arr))
    cum_sec = (cum_arr)/1000
    print(type(cum_sec))
    cum_min=(cum_sec[-1]/60)
    print(len(nn_interval))
    nn_arr = np.array(nn_interval)
    print(len(cum_sec))
    duration = 32
    process = 5
    sliding = 5/60
    iter = int(((duration-process)/sliding)+1)
    print(iter)
    val = []
    dfa_val = []
    for i in range(0,iter):
        var = nn_arr[(cum_sec >= (i*sliding*60)) & (cum_sec <= (i*sliding*60)+(process*60))]
        time_1=cum_sec[(cum_sec >= (i*sliding*60)) & (cum_sec <= (i*sliding*60)+(process*60))]
        val.append(time_1[-1]/60)
        # print(vr[0], vr[-1])
        # print(vr)
        dfa=DFA(var,4,16)
        dfa_val.append(dfa)
        plt.plot(val,dfa_val,marker='.')
        plt.xlabel('Time')
        plt.ylabel('DFA')
    plt.show()