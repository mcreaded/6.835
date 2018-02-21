import math
import numpy as np
import scipy.io
import matplotlib.pyplot as plt
from matplotlib import patches

from detect_peaks import detect_peaks
from circle_fit import circle_fit

# If matplotlib is not working on OSX follow directions in the link below
# https://stackoverflow.com/questions/21784641/installation-issue-with-matplotlib-python


def correct_angle_curve():
    raise NotImplementedError('YOUR CODE HERE')


def segment_stroke(stroke):

    # YOUR CODE HERE

    segpoints, segtypes = [], []

    # 1. CUMULATIVE ARC LENGTHS

    # 2. SMOOTHED PEN SPEEDS

    # 3. TANGENTS

    # 4. CURVATURE

    # 5. IDENTIFY CORNERS

    # 6. COMBINE AND FILTER POINTS

    # 7. CLASSIFY SEGMENTS

    # 8. MERGE SEGMENTS

    return segpoints, segtypes
