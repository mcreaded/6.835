import matplotlib.pyplot as plt

from stroke_segmentation import segment_stroke
from plot_segmentation import plot_segmentation
from Stroke import Stroke
from stroke_data import strokes

custom_strokes = strokes
plt.figure(1, figsize=(12, 8))
for cs in custom_strokes:
    strk = Stroke(x=cs['x'], y=cs['y'], time=cs['time'])
    clean_segment_indices, segtypes = segment_stroke(strk)
    plot_segmentation(strk, clean_segment_indices, segtypes, all=True)


plt.figure(1).canvas.set_window_title('MIT 6.835: Stroke Segmentation')
plt.tight_layout()
plt.show()

