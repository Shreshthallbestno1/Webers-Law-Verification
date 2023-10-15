import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import IntVar
import time
import random

participant = "test"
class StimulusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stimulus Display")
        #resize the window
        self.root.geometry("1000x1000")
        
        self.S1 = 0.8
        self.S2_initial = 0.2
        self.duration = 0.25
        self.button_disabled = True
        self.R_L = []
        self.button_response = IntVar()

        self.create_widgets()
        self.H = [1/3] #[0, 1/3, 2/3] 
        self.V = 1
        self.root.bind('z', lambda event: self.on_left_press())  # 'z' for left
        self.root.bind('x', lambda event: self.on_right_press())
    
    def on_left_press(self):
        if self.button_disabled:
            return
        self.button_response.set(0)
    
    def on_right_press(self):
        if self.button_disabled:
            return
        self.button_response.set(1)

    def create_widgets(self):
        # Set the background of the main frame to black
        self.frame = tk.Frame(self.root, bg='black')
        #self.frame.grid(row=0, column=0, sticky="nsew")  # Use sticky to expand with window size
        self.frame.pack(expand=True, fill=tk.BOTH)
        self.frame.columnconfigure(0, weight=1)  # Column 0 expands horizontally
        self.frame.rowconfigure(0, weight=1)  # Row 0 expands vertically
        self.figure, self.ax = plt.subplots(figsize=(4, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame)
        self.figure.tight_layout(pad=0)
        self.ax.set_axis_off()  # Remove axis # Set background to black
        #self.ax.set_facecolor('black') 
        self.canvas_widget = self.canvas.get_tk_widget()
        #self.canvas_widget.configure(background='black')
        self.canvas_widget.grid(row=0, column=0, sticky="nsew")  # Use sticky to expand with window size

        self.button_frame = tk.Frame(self.frame, bg='black')
        self.button_frame.grid(row=1, column=0, sticky="ew")  # Expand horizontally

        self.button_start = ttk.Button(self.button_frame, text="Start Stimulus", command=self.start_stimulus)
        self.button_start.grid(row=0, column=1)

        self.button_left = ttk.Button(self.button_frame, text="Left", command=lambda: self.button_response.set(0))
        self.button_left.grid(row=1, column=0)

        #self.button_same = ttk.Button(self.button_frame, text="Can't tell", command=lambda: self.button_response.set(2))
        #self.button_same.grid(row=1, column=1)

        self.button_right = ttk.Button(self.button_frame, text="Right", command=lambda: self.button_response.set(1))
        self.button_right.grid(row=1, column=2)

    def show_stim(self, H1, S1, V1, H2, S2, V2):
        print(H1, S1,'\n', H2, S2,)
        self.ax.clear()
        self.ax.set_axis_off()  # Remove axis
        self.ax.set_facecolor('black')
        self.figure.set_facecolor('black')
        # Add distance between the blocks
        left_block = plt.Rectangle((0.05, 0.2), 0.4, 0.6, color=(colors.hsv_to_rgb((H1, max(min(S1,1),0), V1))))
        right_block = plt.Rectangle((0.55, 0.2), 0.4, 0.6, color=(colors.hsv_to_rgb((H2, max(min(S2,1),0), V2))))

        self.ax.add_patch(left_block)
        self.ax.add_patch(right_block)

        self.canvas.draw()

        # Disable the Start Stimulus button while the color is displayed
        self.button_start.config(state=tk.DISABLED)

        # Enable the Left and Right buttons for response
        self.button_left.config(state=tk.DISABLED)
        self.button_right.config(state=tk.DISABLED)
        #self.button_same.config(state=tk.DISABLED)


        self.root.update()

        # Schedule re-enabling of the Start Stimulus button and color reset after the specified duration
        self.root.after(int(self.duration * 1000), self.enable_start_button_and_reset_color)

    def enable_start_button_and_reset_color(self):
        # Re-enable the Start Stimulus button and reset the stimulus
        self.button_start.config(state=tk.DISABLED)
        self.button_left.config(state=tk.NORMAL)
        self.button_right.config(state=tk.NORMAL)
        #self.button_same.config(state=tk.NORMAL)
        self.button_disabled = False
        self.ax.clear()
        self.ax.set_axis_off() 
        self.canvas.draw()
        self.root.update()

    def get_JND(self, H, S, V, d):
        print("H: ", H, "S: ", S, "V: ", V, "d: ", d)
        St = S + 0.2 * d * S
        trial = 0
        dx = 0.01
        S_values = [St]
        ntrials = 40
        #ntrials = 5 # test trials
        while trial <= ntrials: #number of trials
            trial += 1
            direction = random.randint(0, 1)
            try:
                if direction == 0:
                    self.show_stim(H, St, V, H, S, V)
                else:
                    self.show_stim(H, S, V, H, St, V)
                response = self.get_response()
                self.button_disabled = True
                self.R_L.append(response)
                real_dir = direction if (St-S)>0 else 1-direction
                if (response == real_dir):
                    St = St - dx * (St - S)/(abs(St - S))*abs(S)
                elif (response != real_dir):
                    St = St + dx * (St - S)/(abs(St - S))*abs(S)
                elif response == 2:
                    print("Can't tell", St)
                    St = St + dx * d * (St-S)
                    trial -= 1
            except Exception:
                St = St
            S_values.append(St)
            #if(trial > 4 and abs(St-S_values[-4])<=abs(dx*S)):
             #   dx = dx/2
        print(S_values)
        return abs(sum(S_values[-5:])/len(S_values[-5:]) - S), S_values

    def get_response(self):
        print("get_response")

        self.root.wait_variable(self.button_response)
        # Disable the Left and Right buttons after response
        self.button_left.config(state=tk.DISABLED)
        self.button_right.config(state=tk.DISABLED)
        #self.button_same.config(state=tk.DISABLED)

        # Wait for the user's response (1 or 0) through button clicks

        response = self.button_response.get()
        return int(response)

    def one_sat(self, H, S, V):
        try:
            d = 1
            JND_a, S_values_a = self.get_JND(H, S, V, d)
            d = -1
            JND_b, S_values_b = self.get_JND(H, S, V, d)
            #JND_b, S_values_b = 0, []
        except Exception:
            JND_a, JND_b, S_values_a, S_values_b = 0,0,[],[]
        return JND_a, JND_b, S_values_a, S_values_b

    def one_hue(self, H, V):
        JNDs = []
        S_values = []
        for s in range(1, 10):
        #for s in range(4, 6): # test saturation values
            S = s / 10
            try:
                JND_a, JND_b, S_values_a, S_values_b = self.one_sat(H, S, V)
            except Exception:
                JND_a, JND_b, S_values_a, S_values_b = [], [], [], []
            JNDs.append([JND_a, JND_b])
            S_values.append([S_values_a, S_values_b])
        return JNDs, S_values

    def start_stimulus(self):
        global participant
        JNDs = []
        S_values = []
        try:
            self.button_start.config(state=tk.DISABLED)

            JNDs = []
            S_values = []
            for h in self.H:
                try:
                    JNDs_h, S_values_h = self.one_hue(h, self.V)
                except Exception:
                    JNDs_h, S_values_h = [], []
                JNDs.append(JNDs_h)
                S_values.append(S_values_h)
        
            self.button_start.config(state=tk.NORMAL)
        
            self.root.quit()

        # Save JNDs, S_values, and R_L to a file

        except Exception:
            participant = "test"
        filename = "/Users/ShreshthsLaptop/Documents/programs/Python/NS201/"+participant + "_data.txt"
        with open(filename, "w") as f:
            f.write(str(JNDs))
            f.write("\n")
            f.write(str(S_values))
            f.write("\n")
            f.write(str(self.R_L))


def main():
    global participant 
    participant = input("Enter participant name: ")
    root = tk.Tk()
    app = StimulusApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
