import matplotlib.pyplot as plt
import time
import random

R_L = []
def show_stim(H1, S1, V1, H2, S2, V2):
    # Plot the left polygon with S1
    plt.fill([0, 0.5, 0.5, 0], [0, 0, 1, 1], color=(H1, S1, V1))

    # Plot the right polygon with S2 with a slight offset and distance between the two
    plt.fill([0.5, 1, 1, 0.5], [0, 0, 1, 1], color=(H2, S2, V2))

    plt.xlim(0, 1)
    plt.ylim(0, 1)
    #remove axis
    plt.axis('off')
    #make background black
    plt.gca().set_facecolor((0,0,0))


    plt.show()
    time.sleep(5)
    # Close the plot window after the specified duration
    plt.clf()

def get_JND(H, S, V, d):
    St = S + 0.1 * d * S # TODO: change this to a random number
    trial = 0
    S_values = [St]
    dx = 0.2
    while(trial < 20):
        trial += 1
        direction = random.randint(0,1)
        if direction == 0:
            #print(St, S)
            show_stim(H, St, V, H, S, V)
        else:
            #print(S, St)
            show_stim(H, S, V, H, St, V)
        response = get_response()
        R_L.append(response)
        if (response == 0 and direction == 0) or (response == 1 and direction == 1):
            St = St - dx * (St-S)
        elif (response == 0 and direction == 1) or (response == 1 and direction == 0):
            St = St + dx * (St-S)
        elif response == 2:
            dx = 0.5 * dx
            St = St + dx * (St-S)
            trial -= 1
        S_values.append(St)
    return St-S, S_values

def get_response():
    response = input("Which side is more saturated? (L/R) ")
    return response

def one_sat(H,S,V):
    d = 1
    JND_a, S_values_a = get_JND(H,S,V,d)
    d = -1
    JND_b, S_values_b = get_JND(H,S,V,d)
    return JND_a, JND_b, S_values_a, S_values_b

def one_hue(H,V):
    JNDs = []
    S_values = []
    for s in range(1,10):
        S = s/10
        JND_a, JND_b, S_values_a, S_values_b = one_sat(H,S,V)
        JNDs.append([JND_a, JND_b])
        S_values.append([S_values_a, S_values_b])
    return JNDs, S_values

def main():
    #input participant name
    participant = input("Enter participant name: ")
    #three values of Hue: red blue and green
    H = [0, 1/3, 2/3]
    V = 1
    JNDs = []
    S_values = []
    for h in H:
        JNDs_h, S_values_h = one_hue(h,V)
        JNDs.append(JNDs_h)
        S_values.append(S_values_h)
    print(JNDs)
    print(S_values)
    #save JNDs, S_values, and R_L to a file
    f = open(participant + "_data.txt", "w")
    f.write(str(JNDs))
    f.write("\n")
    f.write(str(S_values))
    f.write("\n")
    f.write(str(R_L))
    f.close()
    #print(R_L)

main()


