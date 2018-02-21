import math
import matplotlib.pyplot as plt
from matplotlib import patches
from circle_fit import circle_fit

import numpy as np

plot_number = 1

def plot_segmentation(stroke, segpoints, segtypes, all=False):
    """
    Graphs the stroke along with segmented lines and curves
    :param stroke: the stroke as a Stroke object
    :param segpoints: segmentation points - not including start and end points
    :param segtypes: segmentation types (0 for line, 1 for curve)
    :param all: if we are plotting all strokes on the same figure
    """
    global plot_number
    plt.figure(1)
    if all:
        plt.subplot(3, 4, plot_number)
        title = "Stroke " + str(plot_number)
        plt.title(title)
    plt.plot(stroke.x, stroke.y, 'b.', zorder=2)

    for i in segpoints:
        plt.plot(stroke.x[i], stroke.y[i], 'kX',  zorder=4)

    for i in range(len(segtypes)):
        start_x = stroke.x[segpoints[i]]
        start_y = stroke.y[segpoints[i]]
        end_x = stroke.x[segpoints[i+1]]
        end_y = stroke.y[segpoints[i+1]]
        if segtypes[i] == 0:
            # Plot a line
            plt.plot([start_x, end_x], [start_y, end_y], 'r-', linewidth=6, alpha=0.7)
        else:
            # Plot a curve
            midpoint = int((segpoints[i+1] - segpoints[i])/2)
            y_coords = stroke.y[segpoints[i]: segpoints[i+1]]
            x_coords = stroke.x[segpoints[i]: segpoints[i+1]]
            if type(x_coords) is not list:
                x_coords = [arr[0] for arr in x_coords.tolist()]
            if type(y_coords) is not list:
                y_coords = [arr[0] for arr in y_coords.tolist()]
            xc, yc, R = circle_fit(x_coords, y_coords)

            center = (xc.item(0), yc.item(0))
            start_angle = math.degrees(math.atan2(float(y_coords[-1] - yc), float(x_coords[-1] - xc)))
            end_angle = math.degrees(math.atan2(float(y_coords[0] - yc), float(x_coords[0] - xc)))
            mid_angle = math.degrees(math.atan2(float(y_coords[midpoint] - yc), float(x_coords[midpoint] - xc)))

            if start_angle < 0:
                start_angle += 360
            if end_angle < 0:
                end_angle += 360
            if mid_angle < 0:
                mid_angle += 360

            if start_angle < mid_angle < end_angle or end_angle < start_angle < mid_angle or start_angle > end_angle > mid_angle:
                circ = patches.Wedge(center, R, start_angle, end_angle, color='g', width=20, alpha=0.7, zorder=3)
            else:
                circ = patches.Wedge(center, R, end_angle, start_angle, color='g', width=20, alpha=0.7, zorder=3)
            fig = plt.gcf()
            ax = fig.gca()
            ax.add_patch(circ)
    plot_number += 1
