import numpy as np
import numpy.linalg as la
def ang(v1, v2):
    cosang = np.dot(v1, v2)
    sinang = la.norm(np.cross(v1, v2))
    return np.arctan2(sinang, cosang)
print ang([1,2,3],[2,3,4])


def compute_dist(p1,p2,p3):
	angles = [ang(p1, p2),ang(p1, p3),ang(p1, p3)]
	return angles
def extend_frame(frame):
	_frame = dc(frame.frame)
	#point_map = [(frame.left_hand(),frame.left_elbow(),frame.left_shoulder()),(frame.right_hand(),frame.right_elbow(),frame.right_shoulder()),
		#(frame.right_hip(),frame.right_shoulder(),frame.right_elbow()),(frame.left_hip(),frame.left_shoulder(),frame.left_elbow())]
	#print np.array(point_map).shape
	point_map = [(frame.left_hand(),frame.left_elbow(),frame.left_shoulder()),(frame.right_hand(),frame.right_elbow(),frame.right_shoulder())]
	for i in point_map:
		angles = compute_dist(i[0],i[1],i[2])
		_frame.extend(angles)
	return frame
def extend_seq(seq):
	_seq  = dc(seq)
	for f in range(len(_seq.frames)):
		_seq.frames[f]=extend_frame(_seq.frames[f])
	return _seq

def extend_angles(gest_set):
	_gest_set = dc(gest_set)
	for gs in _gest_set:
		seqs = [extend_seq(seq) for seq in gs.sequences]
		gs.sequences=seqs

	#[[[extend_frame(fr) for fr in seq.frames] for seq in gs.sequences]for gs in _gest_set]
	return _gest_set