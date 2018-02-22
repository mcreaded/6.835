import numpy as np
from scipy import stats
import Stroke
#####
### Compute the arc length of a given index and stroke
#####
def arcLength(stroke, index=0):
	i = 1
	length = 0.0
	
	while i<=index:
		j = np.array([stroke.x[i],stroke.y[i]])
		j_1=np.array([stroke.x[i-1],stroke.y[i-1]])
		norm = np.linalg.norm(np.subtract(j,j_1))
		length+=norm
		i+=1
	return length
def speed(stroke,index):
	dd = arcLength(stroke,index=index+1)-arcLength(stroke,index=index-1);
	dt = stroke.time[index+1]-stroke.index[index-1]
	return dd/dt
######
##compute speed according to the specifications 
#######
def comp_speed(stroke,index=0):
	n=len(stroke.x)
	if index==0:
		return speed(stroke,1);
	elif index==n-1:
		return speed(stroke,n-1);
	return speed(stroke,index)
#########
####smoother
#########
def dotter(padded_speed,index,filt,offset=2):
	speeds = padded_speed[index-offset:index+offset+1];
	speed=1/float(len(filt))*np.dot(speeds,filt)
	return speed


#######
##Speed smoothing filter
#######
def smoother(speeds,filt=[1,1,1,1,1]):
	l_f = len(filt)/2
	padded_speed  = [0.0]*l_f+speeds[0:]+[0.0]*l_f
	offset = l_f
	smoothed = [dotter(padded_speed,i,filt,offset) for i in range(len(speeds))]
	return smoothed
#########
###compute tangent
#########
def begin_match(stroke,_w=11):
	x = stroke.x[0:_w+1]
	y = stroke.y[0:_w+1]
	return stats.linregress(x, y)
def end_match(stroke,_w=11):
	u = _w/2+1
	x = stroke.x[u:]
	y = stroke.y[u:]
	return stats.linregress(x, y)
def regress(stroke,index=4,_w=11):
	u = _w/2+1
	v = _w/2
	x = stroke.x[index-v:index+u]
	y = stroke.y[index-v:index+u]
	return stats.linregress(x,y)

def compute_tangent(stroke, index=4,w=11):
	n = len(stroke.x)
	half_wind = w/2
	if index<half_wind:
		return begin_match(stroke,_w=half_wind);
	elif index>n-half_wind:
		return end_match(stroke,_w=half_wind);
	return regress(stroke,index=index,_w=w)
#########
####Compute curvature
###########
def begin_derv(d,theta,_w=5):
	u = _w/2+1
	x = d[0:u]
	y = theta[0:u]
	return stats.linregress(x,y)
def end_derv(d,theta,_w=5):
	u = _w/2+1
	x = d[-u:]
	y = theta[-u:]
	return stats.linregress(x,y)
def derv(d,theta,index=5,_w=5):
	u = _w/2+1
	v = _w/2
	x = d[index-v:index+u]
	y = theta[index-v:index+u]
	return stats.linregress(x,y)

def compute_curvature(d,theta,index=0,w=11):
	if index<=w/2:
		return begin_derv(d,theta,_w=w)
	elif index>=len(d)-w/2:
		return end_derv(d,theta,_w=w)
	return derv(d,theta,index=index,_w=w)
#######
###Detect corners
########


