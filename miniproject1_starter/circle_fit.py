import math
import numpy as np


def circle_fit(xs, ys):
    """
    Fits (x, y) points to a circle
    :param xs: x-corrdinates
    :param ys: y-coordinates
    :return:center x, center y and radius of the circle
    """
    a = np.matrix([[x, y, 1.] for x, y in zip(xs, ys)])
    b = np.matrix([[-(x*x + y*y)] for x, y in zip(xs, ys)])
    res = np.linalg.lstsq(a, b)[0]
    xc = -0.5 * res[0]
    yc = -0.5 * res[1]

    r = math.sqrt((xc*xc + yc*yc - res[2]))
    return np.array(xc)[0][0], np.array(yc)[0][0], r