import utility_functions as uf 
import stroke_data as sd 
import Stroke as st
import matplotlib.pyplot as plt 
import numpy as np
def plot_each(ind):
	stroke = st.Stroke(sd.strokes[ind]['x'],sd.strokes[ind]['y'],sd.strokes[ind]['time'])
	tangets = [uf.compute_tangent(stroke,index=i).slope for i in range(len(stroke.x))]
	atans = [np.arctan(tan) for tan in tangets]
	plt.plot(stroke.x,stroke.y,label='stoke coordinates')
	plt.show()
	plt.plot(stroke.x, tangets, label="slopes")
	plt.show()
	plt.plot(stroke.x,atans, label='tanget angles')
	plt.show()
for i in range(len(sd.strokes)):
	plot_each(i)
