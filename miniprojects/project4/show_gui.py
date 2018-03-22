import tkinter
import matplotlib.pyplot as plt
from visualization_gui import VisualizationGUI
from data.iPhoneX.faces import face_samples

def on_closing():
    plt.close()

root = tkinter.Tk()
app = VisualizationGUI(root, face_samples)
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
