import matplotlib.pyplot as plt

r2_result = []

JND_result = []

R_avgs = []
# create a list of numbers
def plot_rc(file_path):
    S = [0.1, 0.3, 0.5, 0.7, 0.9]
    delta = [-0.1, -0.07196856730011521, -0.05179474679231213, -0.0372759372031494, -0.02682695795279726, -0.019306977288832496, -0.013894954943731374, -0.004641588833612777, -0.0021544346900318843, -0.001, 0.001, 0.0021544346900318843, 0.004641588833612777, 0.013894954943731374, 0.019306977288832496, 0.02682695795279726, 0.0372759372031494, 0.05179474679231213, 0.07196856730011521, 0.1]
    s = []
    with open(file_path,'r') as f:
        s = f.readlines()
        f.close()
    
    import ast
    responses = []
    responses = ast.literal_eval(s[0].strip())[0]

    R_L = []
    R_L = ast.literal_eval(s[2].strip())

    #Plotting histogram of R_L
    plt.hist(R_L, bins=2)
    plt.xlabel('R_L')
    plt.xticks([0,1])
    plt.ylabel('Frequency')
    plt.savefig('./Outputs/R_L_'+file_path.split('/')[-1].split('.')[0]+'.png')
    plt.clf()

    #Plotting the R_L across trials
    plt.plot(range(400,600),R_L[400:600])
    plt.xlabel('Trials')
    plt.ylabel('R_L')
    plt.savefig('./Outputs/R_L_time_'+file_path.split('/')[-1].split('.')[0]+'.png')
    plt.clf()

    #R = (right-wrong)/(right+wrong)
    R = []
    for i in range(len(responses)):
        r = []
        for j in range(len(responses[i])):
            if delta[j] < 0:
                right = 10 - responses[i][j]
                wrong = responses[i][j]
                r.append((right-wrong)/(right+wrong))
            else:
                right = responses[i][j]
                wrong = 10 - responses[i][j]
                r.append((right-wrong)/(right+wrong))
        R.append(r)
    #print(R)

    #average R for each abs(delta)
    R_avg = []
    for i in range(len(responses)):
        r = []
        for j in range(len(delta[10:])):
            r.append([R[i][j],R[i][-1*j]])
        R_avg.append(r)
    #print(R_avg)

    # plot R for each S
    for i in range(len(R)):
        plt.plot(delta, R[i], label=str(i))
    plt.legend()
    # show the plot
    plt.savefig('./Outputs/R_'+file_path.split('/')[-1].split('.')[0]+'.png')
    plt.clf()

    #plot R_avg for each S
    for i in range(len(R)):
        plt.plot(delta[10:], [sum(j)/2 for j in R_avg[i]], label=str(S[i]))
    plt.legend()
    plt.savefig('./Outputs/R_avg_'+file_path.split('/')[-1].split('.')[0]+'.png')
    plt.clf()

    for i in range(len(responses)):
        for j in range(len(responses[i])):
            responses[i][j] = responses[i][j]/10

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

    # r2 score for the fit:
    from sklearn.metrics import r2_score
    r2s = []
    r2s.append(r2_score(responses[0], [sigmoid(i, *popt0) for i in delta]))
    r2s.append(r2_score(responses[1],  [sigmoid(i, *popt1) for i in delta]))
    r2s.append(r2_score(responses[2],  [sigmoid(i, *popt2) for i in delta]))
    r2s.append(r2_score(responses[3],  [sigmoid(i, *popt3) for i in delta]))
    r2s.append(r2_score(responses[4],  [sigmoid(i, *popt4) for i in delta]))

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
    plt.savefig('./Outputs/sigmoid_'+file_path.split('/')[-1].split('.')[0]+'.png')
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
        
        return ((inv_sigmoid(0.75) - inv_sigmoid(0.5))+(inv_sigmoid(0.5) - inv_sigmoid(0.25)))/2

    JNDs = []
    JNDs.append(JND(popt0))
    JNDs.append(JND(popt1))
    JNDs.append(JND(popt2))
    JNDs.append(JND(popt3))
    JNDs.append(JND(popt4))

    print(JNDs)
    #plot JND v/s S and fit for linear regression
    def linear(x, m, c):
        return m*x + c
    popt, pcov = curve_fit(linear, S[:-1], JNDs[:-1])
    print(popt)
    x = np.linspace(0.1, 0.9, 1000)
    y = linear(x, *popt)
    plt.plot(x,y, label=f"linear fit with m={popt[0]:.4f} and c={popt[1]:.4f}")
    plt.scatter(S, JNDs)
    plt.xlabel('Saturation')
    plt.ylabel('JND')
    plt.legend()
    plt.savefig('./Outputs/JND_'+file_path.split('/')[-1].split('.')[0]+'.png')
    plt.clf()
    
    JND_result.append(JNDs)
    r2_result.append(r2s)
    R_avgs.append(R_avg)

file_paths = []

with open('./Collected_data_red.txt','r') as f:#change for hue
    file_paths = f.readlines()
    f.close()

for file_path in file_paths:
    plot_rc(file_path.strip())

with open('./Outputs/JND_red.txt','w') as f:#change for hue
    for i in range(len(JND_result)):
        f.write(str(JND_result[i])+'\n')
    f.close()
with open('./Outputs/R2_red.txt','w') as f:#change for hue
    for i in range(len(JND_result)):
        f.write(str(r2_result[i])+'\n')
    f.close()
with open('./Outputs/R_avg_red.txt','w') as f:#change for hue
    for i in range(len(JND_result)):
        f.write(str(R_avgs[i])+'\n')
    f.close()
