import numpy as np
from scipy import stats
from scipy.signal import argrelextrema
import Stroke
import circle_fit as cf
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
	dt = stroke.time[index+1]-stroke.time[index-1]
	return dd/dt
######
##compute speed according to the specifications 
#######
def comp_speed(stroke,index=0):
	##print  "compute_speed"
	n=len(stroke.x)
	if index==0:
		return speed(stroke,1);
	elif index==n-1:
		return speed(stroke,n-2);
	return speed(stroke,index)
#########
####smoother
#########
def dotter(padded_speed,index,filt,offset=2):
	speeds = padded_speed[index:index+2*offset+1];
	##print  speeds
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


#######
##compute threshold
########

def speed_based_candidate(speeds, thresh=.60):
	mean_speed = np.mean(speeds)
	minimas = argrelextrema(speeds, np.less)[0]
	##print  minimas
	cands = []
	for minn in minimas:
		if speeds[minn]<thresh*mean_speed:
			cands.append(minn)
	#print  cands
	return cands




#########
###compute tangent
#########
def begin_match(stroke,_w=11):
	x = stroke.x[0:_w+1]
	y = stroke.y[0:_w+1]
	return stats.linregress(x, y).slope
def end_match(stroke,_w=11):
	u = _w/2+1
	x = stroke.x[u:]
	y = stroke.y[u:]
	return stats.linregress(x, y).slope
def regress(stroke,index=4,_w=11):
	u = _w/2+1
	v = _w/2
	x = stroke.x[index-v:index+u]
	y = stroke.y[index-v:index+u]
	regr = stats.linregress(x, y)
	#slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
	#return regr.slope
	if regr.stderr<.05:
		return regr.slope
	else:
		data = cf.circle_fit(x,y)
		#_y = np.sqrt(data[-1]**2-(x[u]-data[0])**2)+data[1]
		slope = -(x[u]-data[0])/(y[u]-data[1])
		#print  "slope:",slope
		return slope

def compute_tangent(stroke, index=4,w=11):
	n = len(stroke.x)
	half_wind = w/2
	if index<half_wind:
		return begin_match(stroke,_w=half_wind);
	elif index>n-half_wind:
		return end_match(stroke,_w=half_wind);
	return regress(stroke,index=index,_w=w)

	
def comp_arctan(slopes):
	angles = []
	last_angle = 0.0
	angle = 0.0;
	thresh = 3.0
	start = True
	current_direct = 0
	current_offset = 0.0
	for ind,slope in enumerate(slopes):
		last_angle = angle
		angle = np.arctan(slope)
		##print  abs(angle-last_angle)
		if abs(angle-last_angle)>thresh and not start:
			##print  abs(angle-last_angle)
			if angle-last_angle>0:
				current_direct = 1
			else:
				current_direct = -1
		
			if current_direct==-1:
				current_offset+=np.pi
			if current_direct==1:
				current_offset-=np.pi
		_angle = angle+current_offset


		angles.append(_angle)
		start = False
	return angles

#########
####Compute curvature
###########
def begin_derv(d,theta,_w=5):
	u = _w
	x = d[0:u]
	y = theta[0:u]
	return stats.linregress(x,y)
def end_derv(d,theta,_w=5):
	u = _w
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

def detect_edges(curvatures,speeds,cthresh=.8,sthresh=.650):
	###
	mean_curv = np.mean(curvatures)
	maximas = argrelextrema(curvatures, np.greater)[0]
	#######
	mean_speed = np.mean(speeds)
	######
	cands= []
	for maxx in maximas:
		if curvatures[maxx]>(1+cthresh)*mean_curv:
			if speeds[maxx]<sthresh*mean_speed:
				cands.append(maxx)
	return cands
########
###combine points
#########
def corner_filter(speeds,points, min_num = 13):
	corrected = points[0:]
	dupl_det = True
	while dupl_det:
		dupl_det=False
		#print  "running"
		for i in range(len(corrected)-1):
			if i==0:
				if corrected[i+1]-corrected[i]<=min_num:
					if len(corrected)>2:
						corrected.pop(i+1)
						dupl_det=True
						break
					
			elif i==len(corrected)-2:
				if corrected[i+1]-corrected[i]<=min_num:
					corrected.pop(i)
					#print  "end"
					break
				else:
					#print  "end"
					break
			else:
				if corrected[i+1]-corrected[i]<=min_num:
					if speeds[corrected[i]]<=speeds[corrected[i+1]]:
						corrected.pop(i+1)
					else:
						corrected.pop(i)
					dupl_det = True
					break
				##print  dupl_det,
	return corrected
def corners(stroke,speeds, thresh = .95):
	mean_speed = np.mean(speeds)
	x_mins = argrelextrema(np.array(stroke.x), np.less)[0].tolist()
	y_mins = argrelextrema(np.array(stroke.y), np.less)[0].tolist()
	####
	x_maxs = argrelextrema(np.array(stroke.x), np.greater)[0].tolist()
	y_maxs = argrelextrema(np.array(stroke.y), np.greater)[0].tolist()
	extremas = x_mins+y_mins+x_maxs+y_maxs
	points = []
	for ext in extremas:
		if speeds[ext]<=thresh*mean_speed:
			points.append(ext)
	return points



def combine_corners(speeds,speed_based,curv_based,corner_based):

	points = sorted(list(set([0]+speed_based+curv_based+corner_based+[len(speeds)-1])))
	#print  "points:", points
	corrected = corner_filter(speeds,points)
	#print  "corrected:",corrected
	return corrected
#####
##classifier
####
class Segment:
	def __init__(self,strt,end):
		self.strt = strt
		self.end = end
		self._class = 0
def generate_segments(stroke,points):
	segments = []
	n = len(stroke.x)
	if points[0]>0:
		first = Segment(0,points[0])
		segments.append(first)
	_points = points[0:]
	while _points:
		point = _points.pop(0)
		if _points==[]:
			if point<n-2:
				seg = Segment(point,n-1)
				segments.append(seg)
		else:
			seg = Segment(point,_points[0])
			segments.append(seg)
	return segments
def comp_cresidual(x,y,circle):
	rc = circle[-1]
	xc = circle[0]
	yc = circle[1]
	ri = np.sqrt(np.square(np.subtract(x, xc)) + np.square(np.subtract(y, yc)))
	residual = sum(np.square(np.subtract(ri,rc)))
	return residual
def comp_red_l(x,y,regr):
	y_p = [x[i]*regr.slope+regr.intercept for i in range(len(x))]
	err = np.sum(np.sqrt(np.square(np.subtract(y,y_p))))
	return err
def classify(stroke,segment,ang_thresh = 0.1,thresh_err = .03):
	x = stroke.x[segment.strt:segment.end+1]
	y = stroke.y[segment.strt:segment.end+1]
	circle = cf.circle_fit(x,y)
	c_err = comp_cresidual(x,y,circle)
	regr = stats.linregress(x,y)
	#computing the subtended angle
	arc1 = arcLength(stroke, index=segment.strt)
	arc2 = arcLength(stroke, index=segment.end)
	c_r = 2*np.pi*circle[-1] 
	subtended_angle = (arc2-arc1)/(c_r)
	#######
	##classifying 
	######
	if subtended_angle>ang_thresh:
		segment._class = 1
	return segment._class

def classify_segments(stroke,points):
	#print  "points:",points
	segments = generate_segments(stroke,points)
	#for segment in segments:
		#print  "strt:",segment.strt
		#print  "end:",segment.end
	_class = [classify(stroke,segment) for segment in segments]
	segments = [0]+[segment.end for segment in segments]
	return segments, _class

def merger(stroke,segments,classes, fit_len=12):
	n = len(classes)
	_segments = segments[0:]

	to_merge=[]
	for i in range(n):
		if i<n-1:
			index = segments[i+1]
			#print  segments
			#print  "index:",index
			x_1 = stroke.x[index-fit_len:index]
			y_1 = stroke.y[index-fit_len:index]

			x_2 = stroke.x[index:index+fit_len]
			y_2 = stroke.y[index:index+fit_len]

			ang1 = np.arctan(stats.linregress(x_1,y_1).slope)
			ang2 = np.arctan(stats.linregress(x_2,y_2).slope)
			ang_diff = abs(ang1-ang2)
			if classes[i]==classes[i+1]:
				if classes[i] == 0:
					if len(stroke.x[segments[i]:segments[i+2]])<45:
						to_merge.append(i+1)
					
					if ang_diff<np.pi/10:
						to_merge.append(i+1)
				else:
					#######
					x_t = stroke.x[segments[i]:segments[i+2]]
					y_t = stroke.y[segments[i]:segments[i+2]]
					########
					x_1 = stroke.x[segments[i]:segments[i+1]]
					y_1 = stroke.y[segments[i]:segments[i+1]]
					####
					x_2 = stroke.x[segments[i+1]:segments[i+2]]
					y_2 = stroke.y[segments[i+1]:segments[i+2]]
					#####
					c_1 = cf.circle_fit(x_1,y_1)
					c_2 = cf.circle_fit(x_2,y_2)
					c_t = cf.circle_fit(x_t,y_t)
					#####
					r_1=comp_cresidual(x_1,y_1,c_1)
					r_2=comp_cresidual(x_2,y_2,c_2)
					r_t=comp_cresidual(x_t,y_t,c_t)
					####
					two= r_1+r_2;
					if r_t<two*(1+.52):
						to_merge.append(i+1)
					d_arc1 = arcLength(stroke,index = segments[i+1])-arcLength(stroke,index = segments[i])
					d_arc2 = arcLength(stroke,index = segments[i+2])-arcLength(stroke,index = segments[i+1])
					if d_arc2/d_arc1<.250 or d_arc2/d_arc1>2.5:
						to_merge.append(i+1)
			else:
				x_t = stroke.x[segments[i]:segments[i+2]]
				y_t = stroke.y[segments[i]:segments[i+2]]
				####3
				x_1 = stroke.x[segments[i]:segments[i+1]]
				y_1 = stroke.y[segments[i]:segments[i+1]]
				####
				x_2 = stroke.x[segments[i]+1:segments[i+2]]
				y_2 = stroke.y[segments[i]+1:segments[i+2]]

				#####
				regr = stats.linregress(x_2,y_2)
				c = cf.circle_fit(x_1,y_1)
				c_t = cf.circle_fit(x_t,y_t)
				####
				r_c = comp_cresidual(x_1,y_1,c)
				r_l = comp_red_l(x_2,y_2,regr)
				r_t=comp_cresidual(x_t,y_t,c_t)

				####
				if classes[i]==0:
					regr = stats.linregress(x_1,y_1)
					c = cf.circle_fit(x_2,y_2)
					r_c = comp_cresidual(x_2,y_2,c)
					r_l = comp_red_l(x_1,y_1,regr)
				####
				two = (1.4)*r_l+r_c
				if r_t<(r_l+r_c):
					to_merge.append(i+1)


	for i in to_merge:
		_segments[i]=0
	points = sorted(list(set(_segments)))
	_segments, _class=classify_segments(stroke,points)
	return _segments,_class
def merge(stroke,segments, classes):
	_classes = classes[0:]
	_segments = segments[0:]
	#print  "merging:",_segments
	old_segments = classes[0:]
	merging = True

	while merging:
		old_segments = _segments[0:]
		_segments,_classes = merger(stroke,_segments,_classes)
		if len(old_segments)==len(_segments):
			return _segments,_classes


				






# l= [0,2,12,23,67,69,75,80,99,123,233,239]
# s = [12,12,21,22,23,23,23,23,23,24]*89
# #print  corner_filter(s,l, min_num = 12)
