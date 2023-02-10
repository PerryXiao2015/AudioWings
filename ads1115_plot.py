# https://python-heart-rate-analysis-toolkit.readthedocs.io/en/latest/quickstart.html
# https://github.com/paulvangentcom/heartrate_analysis_python/tree/master/examples/1_regular_PPG
# 
import pandas as pd
import matplotlib.pyplot as plt
import heartpy as hp

# https://docs.scipy.org/doc/scipy-1.1.0/reference/generated/scipy.signal.find_peaks.html
# https://plotly.com/python/peak-finding/
from scipy.signal import find_peaks

import math
import numpy as np

#df = pd.read_csv('test20221031b.csv')
df = pd.read_csv('test20221122.csv')
#df = pd.read_csv('test20221116.csv')
#print(df.head())
x = df['t']/1000.0
y = df[' Chan3(PPG)']

x = x[0:800]
y = y[0:800]


x_derivative = x[1:]
y_derivative = np.diff(y)/np.diff(x)
#print(y_derivative)

x_derivative2 = x[2:]
y_derivative2 = np.diff(y_derivative)/np.diff(x_derivative)
# Find peaks
indices = find_peaks(y, height = 1.67)[0]
#print(indices)

x_peaks = x[indices]
y_peaks = y[indices]
RR_interval = x_peaks.diff()
RR_interval0= [item for item in RR_interval if not(math.isnan(item)) == True]
#print(RR_interval0)

Heart_rate = int(1.0/np.mean(RR_interval0)*60)
RR_interval_diff = RR_interval.diff()
RR_interval_diff0= [item for item in RR_interval_diff if not(math.isnan(item)) == True]
#RR_interval_diff.dropna()
#print(RR_interval_diff)

res = sum(i[0] * i[1] for i in zip(RR_interval_diff0 , RR_interval_diff0 ))
N = len(RR_interval_diff0 )
RMSSD = int(math.sqrt(res/N)*1000)

# Plot the PPG Signal ==================================================================
plt.figure()
plt.subplot(311)
plt.xlabel ('Time [s]')
plt.ylabel ('PPG Singal [a.u.]')
title = 'Heart Rate [BPM]: ' + str(Heart_rate) + " HRV (RMSSD [ms]):" + str(RMSSD)
plt.title(title)
plt.plot(x,y,label="PPG",color="blue")
plt.scatter(x_peaks,y_peaks,label="Peaks",color="red")
plt.legend()

# Plot the first derivative of the PPG Signal ===========================================
plt.subplot(312)
plt.xlabel ('Time [s]')
plt.ylabel ('dPPG Singal [a.u.]')
plt.title ('First Derivative of PPG Singal')
plt.plot(x_derivative,y_derivative,label="dPPG",color="blue")
plt.legend()
# Plot the Second derivative of the PPG Signal ===========================================
plt.subplot(313)
plt.xlabel ('Time [s]')
plt.ylabel ('ddPPG Singal [a.u.]')
plt.title ('Second Derivative of PPG Singal')
plt.plot(x_derivative2,y_derivative2,label="ddPPG",color="blue")
plt.legend()
plt.show()

#print(type(np.array(y.tolist())))
# =======================================================================================
#first let's load the clean PPG signal
#data, timer = hp.load_exampledata(0)
#print(type(data))
#print(timer)
#and visualise
#plt.figure(figsize=(12,4))
#plt.plot(data)
#plt.show()

fs = 1.0/np.mean(x.diff())
print("fs",fs)
data = np.array(y.tolist())
working_data, measures = hp.process(data, sample_rate = fs)
#hp.plotter(working_data, measures)

#display computed measures
for measure in measures.keys():
    print('%s: %f' %(measure, measures[measure]))
