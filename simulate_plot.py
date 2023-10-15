import matplotlib.pyplot as plt

# create a list of numbers
S = [0.1, 0.3, 0.5, 0.7, 0.9]
delta = [-0.1, -0.07943282347242814, -0.06309573444801933, -0.05011872336272722, -0.039810717055349734, -0.03162277660168379, -0.025118864315095794, -0.0199526231496888, -0.015848931924611134, -0.012589254117941675, -0.007943282347242814, -0.00630957344480193, -0.005011872336272725, -0.003981071705534973, -0.0031622776601683794, -0.0025118864315095794, -0.001995262314968879, -0.001584893192461114, -0.0012589254117941675, -0.001, 0.001, 0.0012589254117941675, 0.001584893192461114, 0.001995262314968879, 0.0025118864315095794, 0.0031622776601683794, 0.003981071705534973, 0.005011872336272725, 0.00630957344480193, 0.007943282347242814, 0.012589254117941675, 0.015848931924611134, 0.0199526231496888, 0.025118864315095794, 0.03162277660168379, 0.039810717055349734, 0.05011872336272722, 0.06309573444801933, 0.07943282347242814, 0.1]

responses = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 3, 4, 11, 20, 16, 33, 34, 37, 44, 46, 58, 64, 69, 68, 69, 70, 77, 85, 93, 96, 95, 99, 100, 100, 100, 100, 100, 100, 100, 100], [0, 0, 0, 0, 1, 2, 5, 7, 11, 21, 23, 23, 36, 41, 38, 41, 42, 37, 48, 45, 54, 52, 58, 55, 51, 62, 70, 66, 61, 72, 72, 82, 91, 94, 99, 100, 100, 100, 100, 100], [0, 0, 0, 0, 6, 10, 10, 19, 25, 30, 30, 41, 45, 45, 44, 47, 46, 45, 41, 45, 52, 55, 53, 57, 54, 58, 54, 66, 58, 62, 77, 73, 77, 92, 84, 96, 97, 99, 99, 100], [0, 1, 0, 4, 10, 21, 19, 25, 27, 33, 35, 44, 48, 40, 40, 57, 49, 54, 52, 49, 49, 50, 60, 57, 64, 44, 54, 69, 49, 65, 73, 73, 76, 82, 86, 87, 95, 95, 97, 100], [1, 3, 5, 10, 15, 22, 25, 28, 38, 28, 36, 48, 39, 44, 52, 45, 43, 44, 47, 56, 54, 56, 61, 49, 58, 53, 57, 53, 50, 56, 65, 69, 71, 65, 83, 91, 90, 97, 98, 98]]

#R = (right-wrong)/(right+wrong)
R = []
for i in range(len(responses)):
    r = []
    for j in range(len(responses[i])):
        if delta[j] < 0:
            right = 100 - responses[i][j]
            wrong = responses[i][j]
            r.append((right-wrong)/(right+wrong))
        else:
            right = responses[i][j]
            wrong = 100 - responses[i][j]
            r.append((right-wrong)/(right+wrong))
    R.append(r)
#print(R)

#average R for each abs(delta)
R_avg = []
for i in range(len(responses)):
    r = []
    for j in range(len(delta[100:])):
        r.append([R[i][j],R[i][-1*j]])
    R_avg.append(r)
#print(R_avg)

# plot R for each S
for i in range(len(R)):
    plt.plot(delta, R[i], label=str(i))
plt.legend()
# show the plot
plt.show()
plt.clf()

#plot R_avg for each S
for i in range(len(R)):
    plt.plot(delta[100:], [sum(j)/2 for j in R_avg[i]], label=str(S[i]))
plt.legend()
plt.show()
plt.clf()

for i in range(len(responses)):
    for j in range(len(responses[i])):
        responses[i][j] = responses[i][j]/100

#plot response v/s delta for each S
colours = ['b', 'g', 'r', 'c', 'm']
for i in range(len(R)):
    plt.scatter(delta, responses[i], color=colours[i])
plt.legend()

#fit a sigmoid to delta and responses
#necessarly passes through 0.5 at 0
import numpy as np
from scipy.optimize import curve_fit

def sigmoid(x ,x0, k):
    y = 1 / (1 + np.exp(-k*(x)))
    return (y)

p0 = [0.5,1] # this is an mandatory initial guess
p1 = [0.5,1] # this is an mandatory initial guess
p2 = [0.5,1] # this is an mandatory initial guess
p3 = [0.5,1] # this is an mandatory initial guess
p4 = [0.5,1] # this is an mandatory initial guess
popt0, pcov0 = curve_fit(sigmoid, delta, responses[0], p0)
popt1, pcov1 = curve_fit(sigmoid, delta, responses[1], p1)
popt2, pcov2 = curve_fit(sigmoid, delta, responses[2], p2)
popt3, pcov3 = curve_fit(sigmoid, delta, responses[3], p3)
popt4, pcov4 = curve_fit(sigmoid, delta, responses[4], p4, maxfev=10000)
print(popt0, popt1, popt2, popt3, popt4)
x = np.linspace(-0.1, 0.1, 1000)
y0 = sigmoid(x, *popt0)
y1 = sigmoid(x, *popt1)
y2 = sigmoid(x, *popt2)
y3 = sigmoid(x, *popt3)
y4 = sigmoid(x, *popt4)
plt.plot(x,y0, label=str(S[0]), color=colours[0])
plt.plot(x,y1, label=str(S[1]), color=colours[1])
plt.plot(x,y2, label=str(S[2]), color=colours[2])
plt.plot(x,y3, label=str(S[3]), color=colours[3])
plt.plot(x,y4, label=str(S[4]), color=colours[4])
plt.legend()
plt.show()
plt.clf()

def JND(popt):
    #difference between points where sigmoid is 0.5 and 0.75 of maximum
    #L = popt[0]
    x0 = popt[0]
    k = popt[1]
    #y = L / (1 + np.exp(-k*(x-x0)))
    def inv_sigmoid(y):
        return (np.log(1/y - 1)/(-k) + x0)
    #finding maximum in the range of [-0.1,0.1]
    min = sigmoid(-0.1,x0,k)
    max = sigmoid(0.1,x0,k)
    return inv_sigmoid(min + 0.75*(max - min)) - inv_sigmoid(min + 0.5*(max-min))

JNDs = []
JNDs.append(JND(popt0))
JNDs.append(JND(popt1))
JNDs.append(JND(popt2))
JNDs.append(JND(popt3))
JNDs.append(JND(popt4))

print(JNDs)
#plot JND v/s S
plt.scatter(S, JNDs)
plt.show()
plt.clf()
