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

