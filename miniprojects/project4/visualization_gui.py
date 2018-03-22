import numpy as np
import tkinter
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter

EMOTION_OPTIONS = [
    "0 - angry",
    "1 - disgust",
    "2 - fear",
    "3 - happy",
    "4 - sad",
    "5 - surprise",
    "6 - neutral",
]
emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']


def plot_emotion_prediction(pred):
    """
    Plots the prediction for each emotion on a bar chart
    :param pred: the predictions for each emotions
    """
    labels = np.arange(len(emotions))
    plt.bar(labels, pred, align='center', alpha=0.5)
    plt.xticks(labels, emotions)
    plt.ylabel('prediction')
    plt.title('emotion')
    plt.show()


class VisualizationGUI:

    def __init__(self, master, samples):
        # Create a container for the UI
        frame = tkinter.Frame(master)
        master.title('6.835 Face Recognition')

        # Create drop down menus for selecting gesture and sequence
        self.emotion_variable = tkinter.StringVar(master)
        self.sample_variable = tkinter.StringVar(master)
        self.emotion_variable.set(EMOTION_OPTIONS[0])  # default value, first emotion
        self.sample_variable.set(0)  # default value, first sample

        sample_label = tkinter.Label(master, text="Sequence:",)
        sample_label.pack()
        sample_options = tkinter.OptionMenu(master, self.sample_variable, *samples.keys(), command=self.sample)
        sample_options.pack()

        emotion_label = tkinter.Label(master, text="Emotion:",)
        emotion_label.pack()
        emotion_options = tkinter.OptionMenu(master, self.emotion_variable, *EMOTION_OPTIONS, command=self.emotion)
        emotion_options.config(width=15)
        emotion_options.pack()

        self.samples = samples

        # Create a matplotlib figure for showing the skeleton
        self.fig = plt.figure(figsize=(8,8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side='top', fill='both')
        self.ax = self.fig.add_subplot(111, projection='3d')

        # Store the current emotion and sample numbers on display
        self.e = 0
        self.s = "A 18:48:11"
        self.draw_sample()

        frame.pack()

    def emotion(self, option):
        self.e = int(option[0])
        self.draw_sample()
        self.canvas.draw()

    def sample(self, option):
        self.s = option
        self.draw_sample()
        self.canvas.draw()

    def draw_sample(self):
        plt.cla()
        sample = self.samples[self.s][emotions[self.e]]
        self.ax.scatter(sample['x'], sample['y'], sample['z'])
