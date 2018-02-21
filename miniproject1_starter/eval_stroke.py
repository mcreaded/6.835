import sys

import matplotlib.pyplot as plt

from stroke_segmentation import segment_stroke
from plot_segmentation import plot_segmentation
from Stroke import Stroke
from stroke_data import strokes

if len(sys.argv) != 2:
    raise ValueError('Error! Give stroke number after filename in command. \n e.g. python eval_stroke.py 2')

i = int(sys.argv[1])

if i < len(strokes) and i > 0 or i == -1:
    cs = strokes[i]
    strk = Stroke(x=cs['x'], y=cs['y'], time=cs['time'])
    clean_segment_indices, segtypes = segment_stroke(strk)
    plot_segmentation(strk, clean_segment_indices, segtypes)
    plt.figure(1).canvas.set_window_title('MIT 6.835: Stroke Segmentation')
    plt.show()
else:
    msg = 'Stroke index out of range. Give a number between 1 and ' + str(strokes.size)
    raise ValueError(msg)
