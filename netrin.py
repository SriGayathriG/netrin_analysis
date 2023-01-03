import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from preprocessing import remove_outliers,remove_ectopic_beats,interpolate_nan_values, get_nn_intervals
from extract_features import get_time_domain_features, get_geometrical_features, get_frequency_domain_features, get_poincare_plot_features, get_csi_cvi_features, get_sampen,DFA, _get_freq_psd_from_nn_intervals
import pdb
# all_files = ['BLEData_Navin_2022_12_19.json','BLEData_Ajay_2022_12_20.json','BLEData_Soundarraj_Mani_2022_12_20.json','BLEData_athul_2022_12_21.json','BLEData_aswath_2022_12_21.json']
# for file in all_files:
#     with open(file) as json_file:
#       main_file = json.load(json_file)

json_file = open('BLEData_Navin_2022_12_19.json')
main_file = json.load(json_file)

rr_in_ms = main_file['captured_data']['hr']['RR in ms']

rr_outliers = remove_outliers(rr_in_ms)
print(rr_outliers)
plt.plot(rr_outliers, marker='.')
# plt.show()

rr_ectopic = remove_ectopic_beats(rr_in_ms)
# print(rr_ectopic)

rr_in_ms_arr = np.array(rr_in_ms)
x = np.logical_and(~np.isnan(rr_in_ms_arr),rr_in_ms_arr>0.0)
rr_nan = rr_in_ms_arr[x]

interpolate = interpolate_nan_values(rr_in_ms)
print(interpolate)

nn_int = get_nn_intervals(rr_in_ms)
print(nn_int)

psd = _get_freq_psd_from_nn_intervals(rr_in_ms)
print(psd)

nn_interval = get_nn_intervals(rr_in_ms, 300,2000,"linear", "acar")
print(nn_interval)
# plt.plot(nn_interval, marker='.')
# plt.show()

    # TO CONVERT RR_IN_MS TO HR  (HR = 60,000/RR_IN_MS)
# hr = 60000./np.array(nn_interval)
# plt.plot(hr,marker ='.')
# plt.show()

hr_in_bpm=main_file['captured_data']['hr']['HR in BPM']
rr_in_ms = main_file['captured_data']['hr']['RR in ms']
heart_rate = np.array(main_file['captured_data']['hr']['HR in BPM'])
cum_arr = np.array(rr_in_ms).cumsum()
print(len(cum_arr))
plt.plot(cum_arr,marker='.')
# plt.show()

# print(cum_arr[:-1]/60)
# import pdb;pdb.set_trace()
cum_sec = (cum_arr)/1000
print(type(cum_sec))
# print(cum_sec) 

    #TO CONVERT SECS TO MINUTES
# print(cum_sec[-1]/60) 

print(len(nn_interval))
nn_arr = np.array(nn_interval)
print(len(cum_sec))

# TO OBTAIN SUBLIST FOR EVERY 300 SECONDS AND PRINT DFA VALUES
for i in range(0,7):   
    vr = nn_arr[(cum_sec >= i*300) & (cum_sec <= (i+1)*301)]
    # print(vr)
    dfa= DFA(vr,4,16)
    print(dfa)


# FIRST METHOD TO OBTAIN SUBLIST FOR EVERY 300 SECONDS (5 MINUTES)
for i in range(0,7):   
    vr = cum_sec[(cum_sec >= i*300) & (cum_sec <= (i+1)*301)]
    print(vr)

# SECOND METHOD TO OBTAIN SUBLIST FOR EVERY 300 SECONDS (5 MINUTES)
for i in range(0,7):   
    vr = np.where((cum_sec >= i*300) & (cum_sec <= (i+1)*301))
    print(vr)

# THIRD METHOD TO OBTAIN SUBLIST FOR EVERY 300 SECONDS (5 MINUTES)
sec = []
for i in range(0,7):
    # pdb.set_trace()
    if (len(cum_sec)>0):
        mysec = []
        for each_sec in cum_sec:
            if (each_sec >= i*300 and each_sec <= (i+1)*301):
                mysec.append(each_sec)
    sec.append(mysec)
print(sec)

# WRONG METHOD -- error -> conditional statement gives array[TRUE,FALSE] as output and not original values
sec = []
for i in range(0,7):
# import pdb;pdb.set_trace()
    x = (cum_sec >= i*300) & (cum_sec <= (i+1)*301)
    sec.append(x)
print(sec)
# plt.plot((cum_sec > i*300) & (cum_sec <= (i+1)*300))
# plt.show()


time_domain = get_time_domain_features(rr_nan)
print(time_domain)

freq_domain = get_frequency_domain_features(rr_nan)
print(freq_domain)

geo_domain = get_geometrical_features(rr_nan)
print(geo_domain)

poincare = get_poincare_plot_features(rr_nan)
print(poincare)

csi_cvi = get_csi_cvi_features(rr_nan)
print(csi_cvi)

sampen = get_sampen(rr_nan)
print(sampen)

dfa = DFA(nn_interval,4,16)
print(dfa)