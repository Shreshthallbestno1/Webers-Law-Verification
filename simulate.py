import random
import time
import numpy as np
from math import *
import matplotlib.pyplot as plt


R_L = []

stim = 0
participant = 'simulation'
H = [0]
V = 1

def sigmoid(diff,S):
    m = log(3)/(0.03*S)
    return 1/(1+np.exp(-m*(diff)))

bs = [1+i/7 for i in range(7)]+[2+i/3 for i in range(1,4)]
differences = [-10**(-1*(i)) for i in bs]+[10**(-1*(i)) for i in bs[::-1]]
S = [0.1,0.3,0.5,0.7,0.9]

for i in S:
    plt.plot(differences, [sigmoid(j,i) for j in differences])

plt.show()

def show_stim(H1, S1, V1, H2, S2, V2):
    global stim
    stim = [S1,S2]
    # show stimulus
    # wait for response
    # return response

def get_response():
    global stim
    S = (stim[0]+stim[1])/2
    diff = stim[0]-stim[1]
    print(stim, S,sigmoid(diff,S))
    #Probability of 1 is sigmoid(diff,S)
    if random.random() > sigmoid(diff,S):
        return 1
    else:
        return 0

def get_JND(H, S, V):
        print("H: ", H, "S: ", S, "V: ", V)
        bs = [1+i/10 for i in range(10)]+[2+i/10 for i in range(1,11)]
        print(bs)
        S_values = [S - 10**(-1*(i)) for i in bs]+[S + 10**(-1*(i)) for i in bs[::-1]] 
        print(S_values)
        response_counts = [0 for i in range(len(S_values))]
        initial_dir = [random.randint(0, 1) for i in range(len(S_values))]
        #for i in range(5): # test trials
        for i in range(100):
            S_shuffle = S_values.copy()
            random.shuffle(S_shuffle)
            for s in S_shuffle:
                direction = initial_dir[S_values.index(s)]
                initial_dir[S_values.index(s)] = 1-direction
                if direction == 0:
                    show_stim(H, s, V, H, S, V)
                else:
                    show_stim(H, S, V, H, s, V)
                response = get_response()
                button_disabled = True
                R_L.append(response)
                if response == direction:
                    response_counts[S_values.index(s)] += 1
                elif response != direction:
                    response_counts[S_values.index(s)] += 0
        return response_counts, S_values

def one_sat(  H, S, V):
        try:
            response_counts, S_values =  get_JND(H, S, V)
        except Exception:
            response_counts = []
            S_values = []
        return response_counts, S_values

def one_hue(  H, V):
    response_count_hue = []
    S_value_hue = []
    for s in range(1, 10, 2):
    #for s in range(4, 5): # test saturation values
        S = s / 10
        try:
            response_counts, S_values =  one_sat(H, S, V)
        except Exception:
            response_counts = []
            S_values = []
        response_count_hue.append(response_counts)
        S_value_hue.append(S_values)
    return response_count_hue, S_value_hue

def start_stimulus(self):
    global participant, H
    responses = []
    S_values = []
    try:
        responses = []
        for h in  H:
            try:
                response_count_hue, S_value_hue =  one_hue(h,  V)
            except Exception:
                response_count_hue = []
                S_value_hue = []
            responses.append(response_count_hue)
            S_values.append(S_value_hue)
    except Exception:
            participant = "test"
    filename = "./Input/"+participant + "_data.txt"
    with open(filename, "w") as f:
        f.write(str(responses))
        f.write("\n")
        f.write(str(S_values))
        f.write("\n")
        f.write(str(R_L))
        f.write("\n")

start_stimulus(1)