import Stroke
import utility_functions as uf
import numpy as np
x = [1.2,2.3,4.5,3.4,2.6,2.0]
y = [5.2,4.5,3.8,3.0,2.3,1.9]
times = [1,2,3,4,5,6]

stroke = Stroke.Stroke(x,y,times)
###########
#######testing compute arcleangh
###########
def output_contr():
	arc_lengths = [0.0]
	sq = 0.0
	for i in range(1,len(x)):
		sq+=np.sqrt((x[i]-x[i-1])**2+(y[i]-y[i-1])**2)
		arc_lengths.append(sq)
	return arc_lengths
def arc_len_tester():
	arc_lengths = output_contr()
	for i in range(len(x)-1):
		print np.isclose(uf.arcLength(stroke, index=i),arc_lengths[i])
		assert uf.arcLength(stroke, index=i)==arc_lengths[i]
arc_len_tester()
######################
#####Testing compute speed 
######################
def test_speed():
	return None
