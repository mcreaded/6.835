from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter


GESTURE_OPTIONS = [
    "0 - pan left",
    "1 - pan right",
    "2 - pan up",
    "3 - pan down",
    "4 - zoom in",
    "5 - zoom out",
    "6 - rotate clockwise",
    "7 - rotate counterclockwise",
    "8 - point",
]


class VisualizationGUI:

    def __init__(self, master, gesture_sets):
        # Create a container for the UI
        frame = tkinter.Frame(master)
        master.title('6.835 Gesture Visualizer')

        # Create 2 buttons for navigating between frames
        self.button_left = tkinter.Button(frame, text="< Previous Frame", command=self.previous_frame)
        self.button_left.pack(side="left")
        self.frame_label = tkinter.Label(frame, text="Frame: 0",)
        self.frame_label.pack(side='left')
        self.button_right = tkinter.Button(frame, text="Next Frame >", command=self.next_frame)
        self.button_right.pack(side="left")

        # Create drop down menus for selecting gesture and sequence
        self.gesture_variable = tkinter.StringVar(master)
        self.sequence_variable = tkinter.StringVar(master)
        self.gesture_variable.set(GESTURE_OPTIONS[0])  # default value, first gesture
        self.sequence_variable.set(0)  # default value, first sequence

        gesture_label = tkinter.Label(master, text="Gesture:",)
        gesture_label.pack()
        gesture_options = tkinter.OptionMenu(master, self.gesture_variable, *GESTURE_OPTIONS, command=self.gesture)
        gesture_options.config(width=15)
        gesture_options.pack()

        sequence_label = tkinter.Label(master, text="Sequence:",)
        sequence_label.pack()
        sequence_options = tkinter.OptionMenu(master, self.sequence_variable, *range(30), command=self.sequence)
        sequence_options.pack()

        self.gesture_sets = gesture_sets

        # Create a matplotlib figure for showing the skeleton
        self.fig = plt.figure()
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        self.ax = self.fig.add_subplot(111, projection='3d')

        # Store the current gesture, sequence and frame numbers on display
        self.g = 0
        self.m = 0
        self.f = 0

        self.draw_frame()

        frame.pack()

    def previous_frame(self):
        self.f = max(0, self.f-1)
        self.draw_frame()
        self.canvas.draw()

    def next_frame(self):
        self.f = min(len(self.gesture_sets[self.g].sequences[self.m].frames)-1, self.f+1)
        self.draw_frame()
        self.canvas.draw()

    def gesture(self, option):
        self.f = 0
        self.m = 0
        self.sequence_variable = 0
        self.g = int(option[0])
        self.draw_frame()
        self.canvas.draw()

    def sequence(self, option):
        self.f = 0
        self.m = option
        self.draw_frame()
        self.canvas.draw()

    def draw_frame(self):
        plt.cla()

        frames = self.gesture_sets[self.g].sequences[self.m].frames
        frame = frames[self.f]
        label_text = "Frame: " + str(self.f) + "/" + str(len(frames)-1)
        self.frame_label.config(text=label_text)

        self.ax.plot([frame.head()[0], frame.neck()[0],],[frame.head()[2], frame.neck()[2],], zs=[-frame.head()[1], -frame.neck()[1],])

        self.ax.plot([frame.neck()[0], frame.left_shoulder()[0],],[frame.neck()[2], frame.left_shoulder()[2],], zs=[-frame.neck()[1], -frame.left_shoulder()[1],])
        self.ax.plot([frame.left_elbow()[0], frame.left_shoulder()[0],],[frame.left_elbow()[2], frame.left_shoulder()[2],], zs=[-frame.left_elbow()[1], -frame.left_shoulder()[1],])
        self.ax.plot([frame.left_elbow()[0], frame.left_hand()[0],],[frame.left_elbow()[2], frame.left_hand()[2],], zs=[-frame.left_elbow()[1], -frame.left_hand()[1],])

        self.ax.plot([frame.neck()[0], frame.right_shoulder()[0],],[frame.neck()[2], frame.right_shoulder()[2],], zs=[-frame.neck()[1], -frame.right_shoulder()[1],])
        self.ax.plot([frame.right_elbow()[0], frame.right_shoulder()[0],],[frame.right_elbow()[2], frame.right_shoulder()[2],], zs=[-frame.right_elbow()[1], -frame.right_shoulder()[1],])
        self.ax.plot([frame.right_elbow()[0], frame.right_hand()[0],],[frame.right_elbow()[2], frame.right_hand()[2],], zs=[-frame.right_elbow()[1], -frame.right_hand()[1],])

        self.ax.plot([frame.torso()[0], frame.left_shoulder()[0],],[frame.torso()[2], frame.left_shoulder()[2],], zs=[-frame.torso()[1], -frame.left_shoulder()[1],])
        self.ax.plot([frame.torso()[0], frame.right_shoulder()[0],],[frame.torso()[2], frame.right_shoulder()[2],], zs=[-frame.torso()[1], -frame.right_shoulder()[1],])

        self.ax.plot([frame.torso()[0], frame.left_hip()[0],],[frame.torso()[2], frame.left_hip()[2],], zs=[-frame.torso()[1], -frame.left_hip()[1],])
        self.ax.plot([frame.torso()[0], frame.right_hip()[0],],[frame.torso()[2], frame.right_hip()[2],], zs=[-frame.torso()[1], -frame.right_hip()[1],])
        self.ax.plot([frame.left_hip()[0], frame.right_hip()[0],],[frame.left_hip()[2], frame.right_hip()[2],], zs=[-frame.left_hip()[1], -frame.right_hip()[1],])

