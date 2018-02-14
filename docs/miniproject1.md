# Project1
## Early Sketch Understanding - Stroke Segmentation
### Introduction
#### Provided
1. A paper - by Stahovich
2. Python Starter Code 
3. Real Pen Stroke data
#### Notes
1. Probably takes a long time
2. Use Piazza or email wcaruso.mit.edu for help
3. Expected is what is being outlined here
4. Collections of issues becuase of a real pen input
5. *Uses Python 3.6*
#### Getting Started 
1. Create a vertual env?
2. Install dependencies
3. The Strokes Object contains arrays of x,y, time
4. You can visualize the strokes with eval_all_strokes.py
  - Creates stroke objects
  - sends them for segmentation
  - And then graphs the raw objects and segments
  - Stroke segmentation not implemented
  - Hence you will see all the strokes appear on the graph
#### Segmenting the strokes
1. Identify corners
2. Classify the segments as lines or arcs
3. Free to create your own structure
4. Provide sement_stroke(stroke)
  - returns segmentpoints, segment types
  - stroke -> stroke objects
  - Segmentpoints -> Array of indices indicating the points of segmentation including the end points
  - Segment types -> Array of the sypes of the segmentpoints
5. You stroke segmentation should follow the steps outlined in the paper
 - Construct an array of the cumulative arc lengths between each pair of consecutive sampled points.
 - Construct an array of smoothed pen speeds at each pont. The size of the window over which smoothing occurs is on eof the parameters you willl need to adjust.
 - Construct an array of tangents 
 - Define curvature - change in orientation over change in position along the arc length.
    - Convert the slopes to angles with the arc tangent function.
    - To see a problem by the arc tangent, plot the arctangent of the slopes that you obtained for strokes 
    - Write and test a method called correct_angle_curve.
6. Indentify corners. Two creterio.
  - Use speed alone to threshold local minima
  - Threshold local curviture maxima
7. Combine the two solutions
8. Classify the segment points as arcs or lines
  - For each segment, fit a line using linear reggression, and fit a circle using the provided fit_circle.py
  - Calculate the residual errors for the line and the circle 
  - Using the residual errors, classify the lines as arcs or lines
9. eval_all_strokes and eval_stroke will help you visualize your shapes
#### Parameters 
- Size of window for smoothing: Uses five tap smoothing filter
- Size of window for computing tangents: 11
- Speed threshold: 25%
- Curvature threshold: .75degree/pixel
- Speed threshold 2: 80% of average
- Mini distance between two corners: You decide
- Minimum arc angle: 36 degrees
#### Merge adjacent segments


