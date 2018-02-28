import sys
from sklearn.model_selection import train_test_split

from Gesture import GestureSet, Sequence, Frame
from classify_nn import classify_nn
from normalize_frames import normalize_frames
from load_gestures import load_gestures
from copy import deepcopy as dc
import random as rd
def split(gesture_sets,ratio):
    _gs_sets = dc(gesture_sets)
    test_data = []
    num_tests = 30-int(round(ratio*30))
    for gs in _gs_sets:
        for i in range(num_tests):
            n = len(gs.sequences)
            ind = rd.randint(0,n-1)
            seq = gs.sequences.pop(ind)
            test_data.append(seq)
    return _gs_sets,test_data

def test_classify_nn(num_frames, ratio):
    """
    Tests classify_nn function. 
    Splits gesture data into training and testing sets and computes the accuracy of classify_nn()
    :param num_frames: the number of frames to normalize to
    :param ratio: percentage to be used for training
    :return: the accuracy of classify_nn()
    """

    gesture_sets = load_gestures()
    norm_gesture_sets = normalize_frames(gesture_sets, num_frames)
    trn,tst = split(norm_gesture_sets,ratio)
    data = [classify_nn(t,trn)==t.label for t in tst]
    
    return float(sum(data))/len(data)



if len(sys.argv) != 3:
    raise ValueError('Error! Give normalized frame number and test/training ratio after filename in command. \n'
                     'e.g. python test_nn.py 20 0.4')

num_frames = int(sys.argv[1])
ratio = float(sys.argv[2])

accuracy = test_classify_nn(num_frames, ratio)
print("Accuracy: ", accuracy)