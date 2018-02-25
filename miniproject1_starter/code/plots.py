import utility_functions as uf 
import stroke_data as sd 
import Stroke as st
import matplotlib.pyplot as plt 
import numpy as np
def plot_each(ind):
	stroke = st.Stroke(sd.strokes[ind]['x'],sd.strokes[ind]['y'],sd.strokes[ind]['time'])
	tangets = [uf.compute_tangent(stroke,index=i) for i in range(len(stroke.x))]

	_atans = [np.arctan(tan) for tan in tangets]
	atans = uf.comp_arctan(tangets)
	# plt.plot(stroke.x,stroke.y,label='stoke coordinates')
	# plt.show()
	# plt.plot(range(len(stroke.x)),_atans, label='tanget angles')
	# plt.show()
	# plt.plot(range(len(atans)), atans)
	# plt.show()

	
	# plt.plot(stroke.x, tangets, label="slopes")
	# plt.show()
	
	speeds = [uf.comp_speed(stroke,index) for index in range(len(stroke.x))]
	#plt.plot(range(len(stroke.x)),speeds,label='speeds')
	#plt.show()
	smoothed = uf.smoother(speeds)
	ind = [stroke.x[i] for i in uf.speed_based_candidate(np.array(smoothed))]
	speed_cands = [stroke.y[i] for i in uf.speed_based_candidate(np.array(smoothed))]
	# plt.plot(range(len(stroke.x)),smoothed,label='smoothed_speeds')
	# plt.show()
	# plt.plot(stroke.x,stroke.y)
	# plt.scatter(ind,speed_cands,label='smoothed_speeds',marker = 'x',c='r')
	# plt.show()

	d = [uf.arcLength(stroke, index=i) for i in range(len(stroke.x))]
	curvs = [uf.compute_curvature(d,atans,index=i,w=11).slope for i in range(len(d))]
	#print curvs
	#plt.plot(range(len(stroke.x)),_atans, label='tanget angles')
	#plt.show()
	#plt.plot(range(len(atans)), atans)
	#plt.show()
	#ind = [stroke.x[i] for i in uf.detect_edges(np.array(curvs),np.array(smoothed))]
	#val = [stroke.y[i] for i in uf.detect_edges(np.array(curvs),np.array(smoothed))]
	curv_based= uf.detect_edges(np.array(curvs),np.array(smoothed))
	speed_based = uf.speed_based_candidate(np.array(smoothed))
	corner_based = uf.corners(stroke,smoothed)
	ind= [stroke.x[i] for i in uf.combine_corners(np.array(speeds),speed_based,curv_based,corner_based)]
	val = [stroke.y[i] for i in uf.combine_corners(np.array(speeds),speed_based,curv_based,corner_based)]



	# plt.plot(range(len(stroke.x)), curvs, c = "r")
	# plt.show()
	plt.plot(stroke.x,stroke.y,c="g")
	
	plt.scatter(ind,val,label='smoothed_speeds',marker = 'x',c='r')
	plt.show()
for i in range(len(sd.strokes)):
	plot_each(i)
#plot_each(4)
