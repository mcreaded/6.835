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
#####
###testing the ligression
#######
# def x_you(x,y):
# 	print stats.linregress(x,y)
# x = [1,2,3,4,5,6,7]
# y= [(_x**2)/8.0 for _x in x]
# x_you(x,y)
# y = [2*_x+1.0 for _x in x]
# x = [1.01,1.99,3.1,3.9,5.03,5.89,7.11]
# x_you(x,y)
# x = [1,2,3,4,5,6,7]
# y = [2*_x+1.0 for _x in x]
# x_you(x,y)
# x = [-2,-1,0,1,2,3,4]
# y= [(_x**2)/8.0 for _x in x]
# x_you(x,y)
##########
###end of testing
#########
