_map = ["left_hand_to_left_shoulder","right_hand_to_shoulder","right_hip_to_right_elbow","left_hip_to_left_elbow"]
from scipy.spatial.distance import euclidean 
from copy import deepcopy as dc
import numpy as np
def compute_dist(p1,p2,p3):
	total = euclidean(p1,p2)+euclidean(p2,p3)
	inters_d = euclidean(p1,p3)
	return inters_d/total

def extend_frame(frame):
	_frame = dc(frame.frame)
	point_map = [(frame.left_hand(),frame.left_elbow(),frame.left_shoulder()),(frame.right_hand(),frame.right_elbow(),frame.right_shoulder()),
		(frame.right_hip(),frame.right_shoulder(),frame.right_elbow()),(frame.left_hip(),frame.left_shoulder(),frame.left_elbow())]
	#print np.array(point_map).shape
	for i in point_map:
		dist = 130.0*compute_dist(i[0],i[1],i[2])
		_frame.append(dist)
	return frame
def extend_seq(seq):
	_seq  = dc(seq)
	for f in range(len(_seq.frames)):
		_seq.frames[f]=extend_frame(_seq.frames[f])
	return _seq

def extend_all(gest_set):
	_gest_set = dc(gest_set)
	for gs in _gest_set:
		seqs = [extend_seq(seq) for seq in gs.sequences]
		gs.sequences=seqs

	#[[[extend_frame(fr) for fr in seq.frames] for seq in gs.sequences]for gs in _gest_set]
	return _gest_set
	 