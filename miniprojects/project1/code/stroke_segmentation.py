import math
import numpy as np
import scipy.io
import matplotlib.pyplot as plt
from matplotlib import patches

from detect_peaks import detect_peaks
from circle_fit import circle_fit
##
import utility_functions as uf

# If matplotlib is not working on OSX follow directions in the link below
# https://stackoverflow.com/questions/21784641/installation-issue-with-matplotlib-python


def correct_angle_curve(slopes):
    return uf.comp_arctan(slopes)


def segment_stroke(stroke):

    # YOUR CODE HERE

    segpoints, segtypes = [], []
    n = len(stroke.x)
    # 1. CUMULATIVE ARC LENGTHS
    arc_lengths = [uf.arcLength(stroke, index=i) for i in range(n)]

    # 2. SMOOTHED PEN SPEEDS
    speeds = [uf.comp_speed(stroke,index=i) for i in range(n)]
    sm_speeds = uf.smoother(speeds)
    # 3. TANGENTS
    tangents = [uf.compute_tangent(stroke, index=i,w=11) for i in range(n)]
    thetas = correct_angle_curve(tangents)

    # 4. CURVATURE
    curvs = [uf.compute_curvature(arc_lengths,thetas,index=i,w=11).slope for i in range(n)]

    # 5. IDENTIFY CORNERS
    speed_based = uf.speed_based_candidate(np.array(sm_speeds))
    curv_based = uf.detect_edges(np.array(curvs),np.array(sm_speeds))
    corner_based = uf.corners(stroke,np.array(sm_speeds))

    # 6. COMBINE AND FILTER POINTS
    points = uf.combine_corners(sm_speeds,speed_based,curv_based,corner_based)
    # 7. CLASSIFY SEGMENTS
    _segpoints,_segtypes = uf.classify_segments(stroke,points)
    # 8. MERGE SEGMENTS
    print "segpoints:",_segpoints
    segpoints,segtypes = uf.merge(stroke,_segpoints, _segtypes)

    return segpoints, segtypes
# import Stroke as _st 
# import stroke_data as _std
# ind = 4
# stroke = _st.Stroke(_std.strokes[ind]['x'],_std.strokes[ind]['y'],_std.strokes[ind]['time'])
# segment_stroke(stroke)
