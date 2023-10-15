import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import ast

with open('./Outputs/JND_green.txt', 'r') as f: #change for hue
    s = f.readlines()
    f.close()

for i in range(len(s)):
    s[i] = ast.literal_eval(s[i].strip())


#Average of the 7 runs for each S value

s_avg = [0,0,0,0,0]
for i in range(len(s)):
    for j in range(5):
        s_avg[j] += s[i][j]
for i in range(5):
    s_avg[i] /= 7

s_std = [0,0,0,0,0]

for i in range(len(s)):
    for j in range(5):
        s_std[j] += (s[i][j] - s_avg[j])**2
for i in range(5):
    s_std[i] /= 7
    s_std[i] = s_std[i]**0.5

def linear(x, m, c):
    return m*x + c

popt, pcov = curve_fit(linear, [0.1,0.3,0.5,0.7], s_avg[:-1])
print(popt)

#r2 for linear fit
residuals = [s_avg[:-1][i] - [linear(i, *popt) for i in [0.1,0.3,0.5,0.7]][i] for i in range(4)]
ss_res = np.sum(np.array(residuals)**2)
ss_tot = np.sum((s_avg[:-1]-np.mean(s_avg[:-1]))**2)
r_squared = 1 - (ss_res / ss_tot)
print(r_squared)

#Plotting the graph with error bars
S_values = [0.1,0.3,0.5,0.7,0.9]
plt.errorbar(S_values, s_avg, yerr=s_std, fmt='o')
plt.plot(S_values, [linear(i, *popt)for i in S_values], 'r-', label='m = '+str(round(popt[0], 3))+', c = '+str(round(popt[1], 3)))
plt.legend()
plt.xlabel('Saturation')
plt.ylabel('JND')
plt.savefig('./Outputs/JND_green.png') #change for hue
plt.clf()
