import cnn
import numpy as np 
from keras.preprocessing import image
from keras.models import Model, load_model
x = cnn.x_test
y = np.array(cnn.y_test)
#print x.shape
#print np.array(y).shape
model = load_model('model_2.h5');
test_score = model.evaluate(x,y)
print test_score;