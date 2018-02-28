import tkinter
import matplotlib.pyplot as plt
from load_gestures import load_gestures
from visualization_gui import VisualizationGUI
from normalize_frames import normalize_frames
num_frames = 30
gesture_sets = load_gestures()
gesture_sets = normalize_frames(gesture_sets, num_frames) #UNCOMMENT to visualize normalized frames


def on_closing():
    plt.close()

root = tkinter.Tk()
app = VisualizationGUI(root, gesture_sets)
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()

