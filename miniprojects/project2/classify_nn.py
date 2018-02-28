import operator
import math
import numpy as np
class SeqNorm:
	def __init__(self,_id,_norm,_class):
		self._id = _id;
		self._norm = _norm
		self._class  = _class
def comp_fr_norm(tr_fr,tst_fr):
	tst_frm = np.array(tst_fr.frame)
	trn_frm = np.array(tr_fr.frame)
	diff_frm = np.sum(np.square(trn_frm-tst_frm))
	return diff_frm
def compute_norm(train_seq,test_seq):
	norm_fnc = np.vectorize(comp_fr_norm)
	return np.sqrt(sum(norm_fnc(train_seq.frames,test_seq.frames)))




def classify_nn(test_sequence, training_gesture_sets):
    """
    Classify test_sequence using nearest neighbors
    :param test_gesture: Sequence to classify
    :param training_gesture_sets: training set of labeled gestures
    :return: a classification label (an integer between 0 and 8)
    """
    sets = []
    for gs in training_gesture_sets:
    	norm_max = min([(compute_norm(test_sequence,seq),seq.label) for seq in gs.sequences], key = lambda t: t[0])
    	sets.append(norm_max)

    return min(sets,key = lambda t: t[0])[1]
    #raise NotImplementedError("Your Code Here")