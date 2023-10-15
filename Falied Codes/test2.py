import random

R_L = []

def get_JND(H, S, V, d):
    St = S + 0.1 * d * S # TODO: change this to a random number
    trial = 0
    S_values = [St]
    while(trial < 20):
        trial += 1
        direction = random.randint(0,1)
        if direction == 0:
            print(St, S)
            #show_stim(H, St, V, H, S, V)
        else:
            print(S, St)
            #show_stim(H, S, V, H, St, V)
        response = get_response()
        R_L.append(response)
        if (response == 0 and direction == 0) or (response == 1 and direction == 1):
            St = St - 0.2 * d * (St-S)
        elif (response == 0 and direction == 1) or (response == 1 and direction == 0):
            St = St + 0.2 * d * (St-S)
        else:
            St = St
            trial -= 1
        S_values.append(St)
    return St-S, S_values

def get_response():
    response = input("Which side is more saturated? (0/1) ")
    return int(response)

get_JND(0, 0.5, 1, -1)